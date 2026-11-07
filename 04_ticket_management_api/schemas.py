from pydantic import BaseModel, Field
from typing import Literal, Optional


class TicketCreate(BaseModel):
    client: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5)
    category: str = Field(..., min_length=3)

class TicketUpdate(BaseModel):
    client: str
    message: str
    category: str
    priority: Literal["low", "medium", "high"]


class TicketPatch(BaseModel):
    client: Optional[str] = None
    message: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None