from fastapi import Depends

from .contracts import ExtractorProtocol
from .default_title_extractor import DefaultTitleExtractor
from .html_extractor import HtmlExtractor
from .llms_txt_extractor import LlmsTxtExtractor


def get_extractors(
    llms: LlmsTxtExtractor = Depends(LlmsTxtExtractor),
    html: HtmlExtractor = Depends(HtmlExtractor),
    default_title: DefaultTitleExtractor = Depends(DefaultTitleExtractor),
) -> list[ExtractorProtocol]:
    return [llms, html, default_title]
