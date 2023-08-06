from pydantic import BaseModel, Field


class UserPayTVModel(BaseModel):
    paytvprovider_id: int = Field(alias="paytvprovider_id")
    ud_key: int = Field(alias="ud_key")
