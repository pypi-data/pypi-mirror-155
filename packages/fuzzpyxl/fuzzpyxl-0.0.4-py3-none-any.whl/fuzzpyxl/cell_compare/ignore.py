from typing import Optional
from .base import BaseComparer, ReadOnlyCellTypes, SearchCell


class IgnoreCompare(BaseComparer):
    def __init__(self, weigth: int = 0,return_value:int = 100):
        super().__init__(weigth=weigth)
        self.return_value = return_value

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:
        if search_cell.ignore:
            return None
        return self.return_value