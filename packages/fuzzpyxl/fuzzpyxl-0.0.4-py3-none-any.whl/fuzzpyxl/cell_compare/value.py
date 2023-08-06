from typing import Callable, Optional
from openpyxl.workbook.workbook import Workbook
from openpyxl.cell.cell import Cell
from .base import BaseComparer, ReadOnlyCellTypes, SearchCell


class ValueCompare(BaseComparer):
    def __init__(
        self,
        compare_callback: Optional[
            Callable[[ReadOnlyCellTypes, SearchCell], int]
        ] = None,
        weigth: int = 1,
    ):
        if compare_callback is None:
            self.compare_callback = self._base_compare
        else:
            self.compare_callback = compare_callback
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:
        return self.compare_callback(cell, search_cell)

    @staticmethod
    def _base_compare(
        cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:
        return 100 if cell.value == search_cell.value else 0
