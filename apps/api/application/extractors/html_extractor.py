from dataclasses import replace

import httpx
from bs4 import BeautifulSoup

from domain import ExtractedContent, SourceType


class HtmlExtractor:
    def extract(self, data: ExtractedContent) -> ExtractedContent:
        extracted_title: str | None = None
        extracted_summary: str | None = None
        extracted_info: str | None = None
        extracted_sections = []

        if not data.source_url:
            return data

        try:
            response = httpx.get(data.source_url, timeout=2.0)
        except httpx.RequestError:
            return data
        if response.status_code != 200:
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
