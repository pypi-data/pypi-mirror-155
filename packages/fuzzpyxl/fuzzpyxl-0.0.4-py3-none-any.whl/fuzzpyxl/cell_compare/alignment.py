from typing import Optional
from openpyxl.styles.alignment import Alignment as oxlAlignment


from openpyxl.workbook.workbook import Workbook
from .base import BaseComparer, ReadOnlyCellTypes, SearchCell


class AlignmentCompare(BaseComparer):
    def __init__(self, weigth: int = 1):
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:
        if cell.alignment is None and search_cell.alignment is None:
            return 100
        elif cell.alignment is not None and search_cell.alignment is None:
            return 100
        elif cell.alignment is None and search_cell.alignment is not None:
            return 0

        res = 0
        increment_value = 50

        if cell.alignment.horizontal == search_cell.alignment.horizontal:  # type: ignore
            res += increment_value

        if cell.alignment.vertical == search_cell.alignment.vertical:  # type: ignore
            res += increment_value

        return res
