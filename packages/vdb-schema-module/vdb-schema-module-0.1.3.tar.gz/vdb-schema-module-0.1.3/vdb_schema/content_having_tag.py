from typing import Optional

from pydantic import BaseModel, Field


class ContentHavingTagModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    content_id: int = Field(alias="content_id")
    tags_id: int = Field(alias="tags_id")
