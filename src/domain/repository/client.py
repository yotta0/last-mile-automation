from abc import ABC, abstractmethod

from src.domain.entities.client import Client


class IClientRepository(ABC):

    @abstractmethod
    def get_clients_paginated(self, page: int, per_page: int):
        pass

    @abstractmethod
    def find_by_id(self, client_id : int):
        pass

    @abstractmethod
    def save(self, client: Client):
        pass

    @abstractmethod
    def delete(self, client: Client):
        pass
