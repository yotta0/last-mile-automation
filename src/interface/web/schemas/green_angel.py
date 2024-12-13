from pydantic import BaseModel
from typing import Optional


class GreenAngelSchema(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True

class GreenAngelsPaginatedSchema(BaseModel):
    total_pages: int
    page: int
    per_page: int
    green_angels: list[GreenAngelSchema]

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class GreenAngelCreateSchema(BaseModel):
    name: str
    is_active: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class GreenAngelUpdateSchema(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
