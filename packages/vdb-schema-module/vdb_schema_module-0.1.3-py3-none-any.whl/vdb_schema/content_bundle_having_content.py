from typing import Optional

from pydantic import BaseModel, Field


class ContentBundleHavingContentModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    content_bundle_id: int = Field(alias="content_bundle_id")
    content_id: int = Field(alias="content_id")
