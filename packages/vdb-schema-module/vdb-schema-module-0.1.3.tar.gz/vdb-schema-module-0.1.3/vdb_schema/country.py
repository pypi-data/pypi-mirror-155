from typing import Optional

from pydantic import BaseModel, Field


class CountryModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    country_id: int = Field(alias="country_id")
    country_name: str = Field(alias="country_name")
    country_description: str = Field(alias="country_description")
