from collections import deque
from typing import Iterable
from urllib.parse import urljoin, urlsplit

import httpx
from bs4 import BeautifulSoup

from domain import CrawlerPolicies, ExtractedContent, ExtractionStrategy, HtmlPolicies
from .contracts import CouldNotExtract
from .html_common import (
    collect_candidates,
    extract_title,
    extract_useful_links,
)


class CrawlerExtractor:
    _POLICIES = HtmlPolicies.default()
    _CRAWLER_POLICIES = CrawlerPolicies.default()

    def extract(self, url: str) -> ExtractedContent:
        if not url:
            raise CouldNotExtract("missing url")

        base = urlsplit(url)
        if not base.scheme or not base.netloc:
            raise CouldNotExtract("invalid url")

        pages = self._crawl(url, max_pages=self._CRAWLER_POLICIES.max_pages)
        if not pages:
            raise CouldNotExtract("crawler found no pages")

        home = pages[0]
        title = home["title"] or url

        sections = extract_useful_links(
            home["soup"], url, max_items=12, policies=self._POLICIES
        )

        all_candidates: list[str] = []
        for page in pages:
            all_candidates.extend(collect_candidates(page["soup"], self._POLICIES))
        sorted_candidates = sorted(all_candidates, key=len, reverse=True)
        summary = self._POLICIES.select_summary(sorted_candidates)
        info = None

        return ExtractedContent(
            source_url=url,
            extraction_strategy=ExtractionStrategy.CRAWLER,
            title=title,
            summary=summary,
            info=info,
            sections=sections,
        )

    def _crawl(self, url: str, max_pages: int) -> list[dict[str, object]]:
        visited: set[str] = set()
        queue: deque[str] = deque([url])
        results: list[dict[str, object]] = []

        while queue and len(results) < max_pages:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            response = self._fetch(current)
            if response is None:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            title = extract_title(soup)
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


    def _extract_internal_links(self, base_url: str, soup: BeautifulSoup) -> Iterable[str]:
        base = urlsplit(base_url)
        policies = self._POLICIES
        ranked: dict[str, tuple[int, int]] = {}

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
            if not policies.is_useful_link(absolute, base.netloc):
                continue

            text = a.get_text(" ", strip=True)
            score = policies.link_rank(text, absolute)
            text_len = len(text)
            current = ranked.get(absolute)
            if current is None or score > current[0] or (
                score == current[0] and text_len > current[1]
            ):
                ranked[absolute] = (score, text_len)

        ordered = sorted(
            ranked.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True
        )
        for url, _meta in ordered:
            yield url
