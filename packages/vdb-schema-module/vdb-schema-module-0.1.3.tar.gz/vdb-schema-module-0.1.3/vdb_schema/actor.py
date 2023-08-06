from typing import Optional

from pydantic import BaseModel, Field


class ActorModel(BaseModel):
    created_on: Optional[str] = Field(alias="created_on")
    modified_on: Optional[str] = Field(alias="modified_on")
    actor_name: str = Field(alias="actor_name")
    actor_id: int = Field(alias="actor_id")
