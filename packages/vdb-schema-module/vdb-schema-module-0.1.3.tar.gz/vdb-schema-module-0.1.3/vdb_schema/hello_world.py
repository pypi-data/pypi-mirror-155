from typing import Optional

from pydantic import BaseModel


class HelloWorldModel(BaseModel):
    id: str
    name: str
    consumer_message: Optional[str]
