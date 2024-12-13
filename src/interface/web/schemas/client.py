from pydantic import BaseModel
from typing import Optional


class ClientSchema(BaseModel):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True

class ClientsPaginatedSchema(BaseModel):
    total_pages: int
    page: int
    per_page: int
    clients: list[ClientSchema]

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class ClientCreateSchema(BaseModel):
    is_active: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class ClientUpdateSchema(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
