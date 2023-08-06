from pydantic import BaseModel, Field


class PayTvProviderModel(BaseModel):
    paytvprovider_id: int = Field(alias="paytvprovider_id")
    paytvprovider_name: str = Field(alias="paytvprovider_name")
