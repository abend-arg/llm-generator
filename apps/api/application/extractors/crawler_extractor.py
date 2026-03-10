from typing import Iterable
from urllib.parse import urljoin, urlsplit

import httpx
from bs4 import BeautifulSoup

from domain import ExtractedContent, FileSection, HtmlPolicies, LinkItem, SourceType
from .contracts import CouldNotExtract


class CrawlerExtractor:
    _POLICIES = HtmlPolicies.default()

    def extract(self, url: str) -> ExtractedContent:
        if not url:
            raise CouldNotExtract("missing url")

        base = urlsplit(url)
        if not base.scheme or not base.netloc:
            raise CouldNotExtract("invalid url")

        pages = self._crawl(url, max_pages=8)
        if not pages:
            raise CouldNotExtract("crawler found no pages")

        home = pages[0]
        title = home["title"] or url

        summary = None
        info = None
        sections = self._extract_useful_links(home["soup"], url, max_items=12)

        return ExtractedContent(
            source_url=url,
            source_type=SourceType.CRAWLER,
            title=title,
            summary=summary,
            info=info,
            sections=sections,
        )

    def _crawl(self, url: str, max_pages: int) -> list[dict[str, object]]:
        visited: set[str] = set()
        queue: list[str] = [url]
        results: list[dict[str, object]] = []

        while queue and len(results) < max_pages:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            response = self._fetch(current)
            if response is None:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            title = self._extract_title(soup)
            results.append(
                {
                    "url": current,
                    "title": title,
                    "soup": soup,
                }
            )

            for link in self._extract_internal_links(current, soup):
                if link not in visited and link not in queue:
                    queue.append(link)

        return results

    def _fetch(self, url: str) -> httpx.Response | None:
        try:
            response = httpx.get(url, timeout=5.0, follow_redirects=True)
        except httpx.RequestError:
            return None
        if response.status_code != 200:
            return None
        return response

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        if soup.title and soup.title.string:
            raw_title = soup.title.string.strip()
            if raw_title:
                return raw_title
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        return None

    def _extract_useful_links(
        self, soup: BeautifulSoup, base_url: str, max_items: int
    ) -> list[FileSection]:
        base = urlsplit(base_url)
        if not base.scheme or not base.netloc:
            return []

        raw_items: list[tuple[str, str]] = []
        seen: set[str] = set()

        for a in soup.find_all("a", href=True):
            href_val = a.get("href")
            href = href_val if isinstance(href_val, str) else ""
            href = href.strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            absolute = urljoin(base_url, href)
            if not self._POLICIES.is_useful_link(absolute, base.netloc):
                continue
            text = a.get_text(" ", strip=True)
            if not text:
                continue
            if absolute in seen:
                continue
            seen.add(absolute)
            raw_items.append((text, absolute))
            if len(raw_items) >= max_items * 3:
                break

        if not raw_items:
            return []

        ranked = self._POLICIES.select_useful_links(raw_items, max_items)
        items = [LinkItem(name=name, url=link) for name, link in ranked]
        return [FileSection(title="Useful Links", items=items)]

    def _extract_internal_links(self, base_url: str, soup: BeautifulSoup) -> Iterable[str]:
        base = urlsplit(base_url)
        for a in soup.find_all("a", href=True):
            href = a.get("href")
            if not isinstance(href, str):
                continue
            href = href.strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            absolute = urljoin(base_url, href)
            parts = urlsplit(absolute)
            if parts.netloc != base.netloc:
                continue
            yield absolute
