from typing import Optional

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    product_id: str = Field(alias="product_id")
    product_name: str = Field(alias="product_name")
    product_name_en: Optional[str] = Field(alias="product_name_en")
