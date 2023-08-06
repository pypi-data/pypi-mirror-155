from typing import Optional

from pydantic import BaseModel, Field


class SubCategoryModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    subcategory_id: int = Field(alias="subcategory_id")
    subcategory: str = Field(alias="subcategory")
    subcategory_en: str = Field(alias="subcategory_en")
