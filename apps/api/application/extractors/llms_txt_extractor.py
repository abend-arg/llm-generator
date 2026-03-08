from domain import ExtractedContent


class LlmsTxtExtractor:
    def extract(self, url: str) -> ExtractedContent:
        return ExtractedContent(source_url=url, source_type="llms_txt", content="")
