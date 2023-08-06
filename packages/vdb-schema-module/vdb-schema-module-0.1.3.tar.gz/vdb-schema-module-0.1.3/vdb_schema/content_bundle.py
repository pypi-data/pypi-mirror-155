from typing import Optional

from pydantic import BaseModel, Field


class ContentBundleModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    content_bundle_id: str = Field(alias="content_bundle_id")
    name: str = Field(alias="name")
