from typing import Optional

from pydantic import BaseModel, Field


class ContentCoreModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    content_core_id: Optional[int] = Field(alias="content_core_id")
    content_id: Optional[str] = Field(alias="content_id")
    season_id: Optional[str] = Field(alias="season_id")
    content_core_episode: Optional[str] = Field(alias="content_core_episode")
    content_core_title: Optional[str] = Field(alias="content_core_title")
