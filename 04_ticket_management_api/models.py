from pydantic import BaseModel, Field
from typing import Optional, Literal


class TicketCreate(BaseModel):
    client: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=5, max_length=500)
    category: str = "general"


class TicketUpdate(BaseModel):
    client: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=5, max_length=500)
    category: str
    priority: Literal["high", "medium", "normal"]


class TicketPatch(BaseModel):
    client: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    message: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=500
    )
    category: Optional[str] = None
    priority: Optional[Literal["high", "medium", "normal"]] = None
