from typing import Optional

from pydantic import BaseModel, Field


class PackageHavingContentBundleModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    package_id: int = Field(alias="package_id")
    content_bundle_id: int = Field(alias="content_bundle_id")
