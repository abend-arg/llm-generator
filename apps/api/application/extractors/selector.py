from .contracts import ExtractorProtocol
from .html_extractor import HtmlExtractor
from .llms_txt_extractor import LlmsTxtExtractor


class ExtractorSelector:
    def pick(self, url: str) -> ExtractorProtocol:
        _ = url
        # Business rule placeholder: prefer llms.txt when available
        return LlmsTxtExtractor()
