from typing import Optional
from openpyxl.workbook.workbook import Workbook
from .base import BaseComparer, ReadOnlyCellTypes, SearchCell


class DataTypeCompare(BaseComparer):
    def __init__(self, weigth: int = 1):
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:
        if search_cell.cell_type is None:
            return None
        
        return 100 if cell.data_type == search_cell.data_type else 0
