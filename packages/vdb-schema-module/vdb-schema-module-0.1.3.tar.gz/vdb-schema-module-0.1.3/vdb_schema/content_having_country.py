from typing import Optional

from pydantic import BaseModel, Field


class ContentHavingCountryModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    country_id: int = Field(alias="country_id")
    content_id: int = Field(alias="content_id")
