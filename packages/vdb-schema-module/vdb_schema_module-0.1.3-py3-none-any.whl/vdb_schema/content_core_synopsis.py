from typing import Optional

from pydantic import BaseModel, Field


class ContentCoreSynopsisModel(BaseModel):
    content_core_synopsis_created_on: Optional[str] = Field(
        alias="content_core_synopsis_created_on"
    )
    content_core_synopsis_modified_on: Optional[str] = Field(
        alias="content_core_synopsis_modified_on"
    )
    content_core_id: str = Field(alias="content_core_id")
    content_core_synopsis: str = Field(alias="content_core_synopsis")
    content_core_synopsis_en: str = Field(alias="content_core_synopsis_en")
