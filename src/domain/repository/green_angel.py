from abc import ABC, abstractmethod

from src.domain.entities.green_angel import GreenAngel


class IGreenAngelRepository(ABC):

    @abstractmethod
    def get_green_angels_paginated(self, page: int, per_page: int):
        pass

    @abstractmethod
    def find_by_id(self, green_angel_id : int):
        pass

    @abstractmethod
    def save(self, green_angel: GreenAngel):
        pass

    @abstractmethod
    def delete(self, green_angel: GreenAngel):
        pass
