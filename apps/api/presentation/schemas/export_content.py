from pydantic import BaseModel, HttpUrl


class ExportContentRequest(BaseModel):
    url: HttpUrl
