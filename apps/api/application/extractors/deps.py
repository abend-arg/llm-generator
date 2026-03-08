from fastapi import Depends

from .contracts import ExtractorProtocol
from .html_extractor import HtmlExtractor
from .llms_txt_extractor import LlmsTxtExtractor


def get_extractors(
    llms: LlmsTxtExtractor = Depends(LlmsTxtExtractor),
    html: HtmlExtractor = Depends(HtmlExtractor),
) -> list[ExtractorProtocol]:
    return [llms, html]
