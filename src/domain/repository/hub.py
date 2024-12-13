from abc import ABC, abstractmethod

from src.domain.entities.hub import Hub


class IHubRepository(ABC):

    @abstractmethod
    def get_hubs_paginated(self, page: int, per_page: int):
        pass

    @abstractmethod
    def find_by_id(self, hub_id : int):
        pass

    @abstractmethod
    def save(self, hub: Hub):
        pass

    @abstractmethod
    def delete(self, hub: Hub):
        pass
