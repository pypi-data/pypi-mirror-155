from typing import Optional

from pydantic import BaseModel, Field


class ContentHavingDirectorModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    actor_id: int = Field(alias="actor_id")
    content_id: int = Field(alias="content_id")
