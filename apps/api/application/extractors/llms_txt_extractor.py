from dataclasses import replace

from domain import ExtractedContent


class LlmsTxtExtractor:
    def extract(self, data: ExtractedContent) -> ExtractedContent:
        extracted_title: str | None = None
        extracted_summary: str | None = None
        extracted_notes: list[str] = []
        extracted_sections = []

        updates: dict[str, object] = {}

        if not data.title and extracted_title:
            updates["title"] = extracted_title
        if data.summary is None and extracted_summary is not None:
            updates["summary"] = extracted_summary
        if extracted_notes:
            updates["notes"] = [*data.notes, *extracted_notes]
        if extracted_sections:
            updates["sections"] = [*data.sections, *extracted_sections]

        if not updates:
            return data

        return replace(data, **updates)
