from typing import Optional

from pydantic import BaseModel, Field


class CategoryModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    category_en: str = Field(alias="category_en")
    category_id: int = Field(alias="category_id")
    content_type: str = Field(alias="content_type")
    category: str = Field(alias="category")
