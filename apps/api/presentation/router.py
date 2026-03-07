from typing import Annotated

from fastapi import APIRouter, Depends

from .controllers import PingController

router = APIRouter()


@router.get("/ping")
def ping(controller: Annotated[PingController, Depends()]) -> dict[str, str]:
    return controller.get_ping()
