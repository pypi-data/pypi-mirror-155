from typing import Optional

from pydantic import BaseModel, Field


class HomePageModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    homepage_id: str = Field(alias="homepage_id")
    homepage_title: Optional[str] = Field(alias="homepage_title")
    homepage_title_en: Optional[str] = Field(alias="homepage_title_en")
    homepage_status: Optional[str] = Field(alias="homepage_status")
    homepage_type: Optional[str] = Field(alias="homepage_type")
    is_connected: Optional[str] = Field(alias="is_connected")
