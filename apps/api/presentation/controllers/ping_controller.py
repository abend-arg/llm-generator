from application import PingService
from fastapi import Depends


class PingController:
    def __init__(self, service: PingService = Depends()) -> None:
        self._service = service

    def get_ping(self) -> dict[str, str]:
        return self._service.get_ping()
