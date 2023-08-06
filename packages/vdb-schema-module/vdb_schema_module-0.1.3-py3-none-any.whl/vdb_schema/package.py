from typing import Optional

from pydantic import BaseModel, Field


class PackageModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    package_id: int = Field(alias="package_id")
    package_name: Optional[str] = Field(alias="package_name")
    package_name_en: Optional[str] = Field(alias="package_name_en")
    package_is_pay_tv: Optional[int] = Field(alias="package_is_pay_tv")
