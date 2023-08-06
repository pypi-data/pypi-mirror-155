from typing import Optional

from pydantic import BaseModel, Field


class TagsModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    tag_id: int = Field(alias="tag_id")
    tag_name: str = Field(alias="tag_name")
    tag_description: str = Field(alias="tag_description")
