from dataclasses import replace
from typing import Iterable
from urllib.parse import urlsplit

import httpx

from domain import ExtractedContent, FileSection, LinkItem, SourceType


class LlmsTxtExtractor:
    def _candidate_llms_urls(self, url: str) -> Iterable[str]:
        parts = urlsplit(url)
        if not parts.scheme or not parts.netloc:
            return []
        base = f"{parts.scheme}://{parts.netloc}"
        return (
            f"{base}/.well-known/llms.txt",
            f"{base}/llms.txt",
        )

    def _parse_link_item(self, line: str) -> LinkItem | None:
        # Expected: - [Name](url) or - [Name](url): notes
        if not line.startswith("- ["):
            return None
        try:
            name_part, rest = line[3:].split("](", 1)
            url_part, tail = rest.split(")", 1)
        except ValueError:
            return None
        notes = tail.strip()
        if notes.startswith(":"):
            notes = notes[1:].strip()
        elif notes:
            notes = notes.strip()
        else:
            notes = None
        return LinkItem(name=name_part.strip(), url=url_part.strip(), notes=notes)

    def _parse_llms_txt(
        self, text: str
    ) -> tuple[str | None, str | None, str | None, list[FileSection]]:
        lines = text.splitlines()

        title: str | None = None
        summary: str | None = None
        info: str | None = None
        sections: list[FileSection] = []

        info_buffer: list[str] = []
        section_info_started = False
        current_section_title: str | None = None
        current_section_items: list[LinkItem] = []

        for raw in lines:
            line = raw.rstrip()
            if not line:
                if current_section_title is None:
                    info_buffer.append("")
                continue

            match True:
                case _ if line.startswith("# "):  # title
                    if title is None:
                        title = line[2:].strip()
                case _ if line.startswith("## "):  # section header
                    if current_section_title and current_section_items:
                        sections.append(
                            FileSection(
                                title=current_section_title,
                                items=list(current_section_items),
                            )
                        )
                        current_section_items = []
                    section_info_started = False
                    current_section_title = line[3:].strip()
                case _ if line.startswith(">"):
                    if summary is None:  # summary / quote
                        summary = line.lstrip("> ").strip()
                    else:
                        info_buffer.append(line.lstrip("> ").strip())
                case _ if line.startswith("- "):  # list item / link
                    if current_section_title is None:
                        info_buffer.append(line)
                    else:
                        item = self._parse_link_item(line)
                        if item is not None:
                            current_section_items.append(item)
                        else:
                            if not section_info_started:
                                if info_buffer and info_buffer[-1] != "":
                                    info_buffer.append("")
                                section_info_started = True
                            info_buffer.append(line)
                case _:  # info / paragraph
                    if current_section_title is not None and not section_info_started:
                        if info_buffer and info_buffer[-1] != "":
                            info_buffer.append("")
                        section_info_started = True
                    info_buffer.append(line)

        if current_section_title and current_section_items:
            sections.append(
                FileSection(title=current_section_title, items=list(current_section_items))
            )

        if info_buffer:
            info = "\n".join(info_buffer).strip()

        return title, summary, info, sections

    def extract(self, data: ExtractedContent) -> ExtractedContent:
        extracted_title: str | None = None
        extracted_summary: str | None = None
        extracted_info: str | None = None
        extracted_sections: list[FileSection] = []

        for candidate in self._candidate_llms_urls(data.source_url):
            try:
                response = httpx.get(candidate, timeout=2.0)
            except httpx.RequestError:
                continue
            if response.status_code != 200:
                continue
            text = response.text.strip()
            if not text:
                continue
            extracted_title, extracted_summary, extracted_info, extracted_sections = (
                self._parse_llms_txt(text)
            )
            break

        updates: dict[str, object] = {}

        if not data.title and extracted_title:
            updates["title"] = extracted_title
        if data.summary is None and extracted_summary is not None:
            updates["summary"] = extracted_summary
        if data.info is None and extracted_info is not None:
            updates["info"] = extracted_info
        if extracted_sections:
            updates["sections"] = [*data.sections, *extracted_sections]
        if extracted_title or extracted_summary or extracted_info or extracted_sections:
            updates["source_type"] = SourceType.LLMS_TXT

        if not updates:
            return data

        return replace(data, **updates)
