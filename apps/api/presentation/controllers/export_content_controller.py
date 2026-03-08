from application import ExportContentService
from fastapi import Depends


class ExportContentController:
    def __init__(self, service: ExportContentService = Depends()) -> None:
        self._service = service

    def export(self, url: str) -> tuple[str, str]:
        return self._service.export(url)
