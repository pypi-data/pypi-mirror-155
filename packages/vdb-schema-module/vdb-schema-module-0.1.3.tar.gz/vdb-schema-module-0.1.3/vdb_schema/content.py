from typing import Optional

from pydantic import BaseModel, Field


class ContentModel(BaseModel):
    content_id: str = Field(alias="content_id")
    title: str = Field(alias="title")
    year: Optional[str] = Field(alias="year")
    synopsis: Optional[str] = Field(alias="synopsis")
    synopsis_en: Optional[str] = Field(alias="synopsis_en")
    type: str = Field(alias="type")
    status: str = Field(alias="status")
    rating: str = Field(alias="rating")
    is_free: str = Field(alias="is_free")
    is_original: str = Field(alias="is_original")
    is_branded: str = Field(alias="is_branded")
    is_exclusive: str = Field(alias="is_exclusive")
    is_geo_block: Optional[str] = Field(alias="is_geo_block")
    duration_minute: str = Field(alias="duration_minute")
    language: Optional[str] = Field(alias="language")
    start_date: Optional[str] = Field(alias="start_date")
    end_date: Optional[str] = Field(alias="end_date")
    category_id: Optional[str] = Field(alias="category_id")
    subcategory_id: Optional[str] = Field(alias="subcategory_id")
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
