from fastapi import APIRouter, Depends, Response

from .controllers import ExportContentController, PingController
from .schemas import ExportContentRequest

router = APIRouter()


@router.get("/ping")
def ping(controller: PingController = Depends()) -> dict[str, str]:
    return controller.get_ping()


@router.post("/export-content")
def export_content(
    payload: ExportContentRequest,
    controller: ExportContentController = Depends(),
) -> Response:
    filename, content = controller.export(str(payload.url))
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
