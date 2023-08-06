from typing import Optional

from pydantic import BaseModel, Field


class ProductHavingPackageModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    product_id: str = Field(alias="product_id")
    package_id: str = Field(alias="package_id")
