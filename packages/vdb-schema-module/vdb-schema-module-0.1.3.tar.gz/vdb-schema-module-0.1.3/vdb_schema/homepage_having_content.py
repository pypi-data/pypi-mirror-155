from typing import Optional

from pydantic import BaseModel, Field


class HomePageHavingContentModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    homepage_having_content_id: int = Field(alias="homepage_having_content_id")
    homepage_id: int = Field(alias="homepage_id")
    content_id: int = Field(alias="content_id")
