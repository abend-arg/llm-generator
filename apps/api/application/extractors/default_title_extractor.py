from dataclasses import replace

from domain import ExtractedContent


class DefaultTitleExtractor:
    def extract(self, data: ExtractedContent) -> ExtractedContent:
        if data.title:
            return data
        return replace(data, title=data.source_url)
