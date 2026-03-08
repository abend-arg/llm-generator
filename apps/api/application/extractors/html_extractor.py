from dataclasses import replace

import httpx
from bs4 import BeautifulSoup

from domain import ExtractedContent, SourceType


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
        if soup.title and soup.title.string:
            raw_title = soup.title.string.strip()
            if raw_title:
                extracted_title = raw_title
        if not extracted_title:
            h1 = soup.find("h1")
            if h1 and h1.get_text(strip=True):
                extracted_title = h1.get_text(strip=True)

        if extracted_summary is None:
            extracted_summary = self._extract_summary(soup)

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
            response = httpx.get(url, timeout=2.0)
        except httpx.RequestError:
            return None
        if response.status_code != 200:
            return None
        return response

    def _extract_summary(self, soup: BeautifulSoup) -> str | None:
        candidates: list[str] = []
        reject_keywords = {
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

        containers = soup.find_all(["main", "article", "section", "div"])
        for tag in containers:
            if self._is_rejected(tag, reject_keywords) or not self._has_hs(tag):
                continue
            nodes = tag.find_all(["p", "ul", "span", "div"], recursive=False)
            if not nodes:
                continue
            text = "\n".join(n.get_text("\n", strip=True) for n in nodes).strip()
            if text:
                candidates.append(text)

        if not candidates:
            for n in soup.find_all(["p", "li", "span", "div"]):
                text = n.get_text(" ", strip=True)
                if text:
                    candidates.append(text)

        if not candidates:
            return None

        best_text = max(candidates, key=len)
        if len(best_text) < 100:
            return None
        return best_text[:600]
