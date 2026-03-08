from fastapi import Depends

from application import ExportContentService


class ExportContentController:
    def __init__(
        self, service: ExportContentService = Depends()
    ) -> None:
        self._service = service

    def export(self, url: str) -> tuple[str, str]:
        return self._service.export(url)
