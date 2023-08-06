from typing import Optional

from pydantic import BaseModel, Field


class UserDetailHavingPackageModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    package_id: int = Field(alias="package_id")
    user_detail_having_package_id: int = Field(alias="user_detail_having_package_id")
    ud_key: int = Field(alias="ud_key")
