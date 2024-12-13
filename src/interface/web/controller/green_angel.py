from src.interface.web.schemas.green_angel import GreenAngelCreateSchema, GreenAngelUpdateSchema
from src.application.service.green_angel import GreenAngelService


class GreenAngelController:
    def __init__(self, green_angel_service: GreenAngelService):
        self.green_angel_service = green_angel_service

    def get_green_angels(self, page: int, per_page: int) -> dict:
        return self.green_angel_service.get_green_angels_paginated(page, per_page)

    def get_green_angel(self, green_angel_id: int) -> dict:
        return self.green_angel_service.find_green_angel(green_angel_id)

    def create_green_angel(self, green_angel_create: GreenAngelCreateSchema) -> dict:
        return self.green_angel_service.create_green_angel(green_angel_create)

    def update_green_angel(self, green_angel_id: int, green_angel_update: GreenAngelUpdateSchema) -> dict:
        return self.green_angel_service.update_green_angel(green_angel_id, green_angel_update)

    def delete_green_angel(self, green_angel_id: int) -> dict:
        return self.green_angel_service.delete_green_angel(green_angel_id)
