from typing import Dict, List, Optional
from app.tools import repository


class FakeRepository(repository.AbstractRepository):
    def __init__(self, id_column: str):
        self.id_column = id_column
        self.data: List[Dict] = []
        self.commited = False

    def _get(self, identifier: str) -> Optional[Dict]:
        for item in self.data:
            if item[self.id_column] == identifier:
                return item
        return None

    def _add(self, data: Dict) -> None:
        self.commited = False
        self.data.append(data)

    def _commit(self):
        self.commit = True