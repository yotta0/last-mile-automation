from pydantic import BaseModel
from typing import Optional


class HubSchema(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True

class HubsPaginatedSchema(BaseModel):
    size: int
    total_pages: int
    page: int
    per_page: int
    items: list[HubSchema]

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class HubCreateSchema(BaseModel):
    name: str
    is_active: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class HubUpdateSchema(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
