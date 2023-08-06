from typing import Optional
from openpyxl.cell.read_only import EmptyCell
from .base import BaseComparer, ReadOnlyCellTypes, SearchCell


class RegexCompare(BaseComparer):
    def __init__(self, weigth: int = 1):
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:
        if search_cell.re_pattern is None:
            return None
            
        return 100 if bool(search_cell.re_pattern.match(str(cell.value))) else 0