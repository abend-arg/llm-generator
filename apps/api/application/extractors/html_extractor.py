from dataclasses import replace
from urllib.parse import urljoin, urlsplit

import httpx
from bs4 import BeautifulSoup

from domain import ExtractedContent, FileSection, LinkItem, SourceType


class HtmlExtractor:
    _REJECT_KEYWORDS = {
        "testimonial",
        "testimonials",
        "review",
        "reviews",
        "quote",
        "quotes",
        "social-proof",
        "case-study",
        "customer",
    }
    _REJECT_LINK_KEYWORDS = {
        "/privacy",
        "/terms",
        "/login",
        "/signup",
        "/sign-up",
        "/sign-in",
        "/signin",
        "/register",
    }
    _USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"

    def extract(self, data: ExtractedContent) -> ExtractedContent:
        extracted_title: str | None = None
        extracted_summary: str | None = None
        extracted_info: str | None = None
        extracted_sections = []

        if not data.source_url:
            return data

        response = self._fetch(data.source_url)
        if response is None:
            return data

        soup = BeautifulSoup(response.text, "html.parser")
        extracted_title = self._extract_title(soup)

        if extracted_summary is None:
            extracted_summary, extracted_info = self._extract_summary_and_info(soup)
        if not extracted_sections:
            extracted_sections = self._extract_useful_links(
                soup, data.source_url, max_items=12
            )

        updates: dict[str, object] = {}

        if not data.title and extracted_title:
            updates["title"] = extracted_title
        if data.summary is None and extracted_summary is not None:
            updates["summary"] = extracted_summary
        if data.info is None and extracted_info is not None:
            updates["info"] = extracted_info
        if extracted_sections:
            updates["sections"] = [*data.sections, *extracted_sections]
        if extracted_title:
            updates["source_type"] = SourceType.HTML

        if not updates:
            return data

        return replace(data, **updates)

    def _is_rejected(self, tag) -> bool:
        classes = tag.get("class") or []
        tag_id = tag.get("id") or ""
        haystack = " ".join(classes + [tag_id]).lower()
        return any(word in haystack for word in self._REJECT_KEYWORDS)

    def _is_rejected_tree(self, tag) -> bool:
        current = tag
        while current:
            if self._is_rejected(current):
                return True
            current = current.parent
        return False

    def _has_hs(self, tag) -> bool:
        return tag.find(["h1", "h2", "h3"], recursive=False) is not None

    def _fetch(self, url: str) -> httpx.Response | None:
        try:
            response = httpx.get(
                url,
                timeout=5.0,
                follow_redirects=True,
                headers={"User-Agent": self._USER_AGENT},
            )
        except httpx.RequestError:
            return None
        if response.status_code != 200:
            return None
        return response

    def _extract_summary_and_info(
        self, soup: BeautifulSoup
    ) -> tuple[str | None, str | None]:
        candidates: list[str] = []
        containers = soup.find_all(["main", "article", "section", "div"])
        for tag in containers:
            if self._is_rejected_tree(tag) or not self._has_hs(tag):
                continue
            nodes = tag.find_all(["p", "ul", "span", "div"], recursive=False)
            if not nodes:
                continue
            text = "\n".join(
                n.get_text("\n", strip=True)
                for n in nodes
                if not self._is_rejected_tree(n)
            ).strip()
            if text:
                candidates.append(text)

        if not candidates:
            for n in soup.find_all(["p", "li", "span", "div"]):
                if self._is_rejected_tree(n):
                    continue
                text = n.get_text(" ", strip=True)
                if text:
                    candidates.append(text)

        if not candidates:
            return None, None

        best_text = max(candidates, key=len)
        if len(best_text) < 100:
            return None, None

        summary = best_text
        info_candidates = [c for c in candidates if c != best_text and len(c) >= 80]
        info = "\n\n".join(info_candidates) if info_candidates else None
        return summary, info

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

        items: list[LinkItem] = []
        seen: set[str] = set()

        for a in soup.find_all("a", href=True):
            href = a.get("href", "").strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            absolute = urljoin(base_url, href)
            parts = urlsplit(absolute)
            if parts.netloc != base.netloc:
                continue
            text = a.get_text(" ", strip=True)
            if not text:
                continue
            if absolute in seen:
                continue
            seen.add(absolute)
            items.append(LinkItem(name=text, url=absolute))
            if len(items) >= max_items:
                break

        if not items:
            return []

        return [FileSection(title="Useful Links", items=items)]
