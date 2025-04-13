from typing import List
from domain.entities import Deal

class SearchDealsUseCase:
    def __init__(self, deal_repository):
        self.deal_repository = deal_repository

    def execute(self, query: str) -> List[Deal]:
        return self.deal_repository.search(query) 