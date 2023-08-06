from typing import Optional
from .base import BaseComparer, ReadOnlyCellTypes, SearchCell


class FontSizeCompare(BaseComparer):
    def __init__(self, font_size_range: float = 5, weigth: int = 1):
        self.font_size_range = font_size_range
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:

        if cell.font is None and search_cell.font is None:
            return 100
        elif cell.font is not None and search_cell.font is None:
            return 100
        elif cell.font is None and search_cell.font is not None:
            return 0

        diff_sz = abs(cell.font.sz - search_cell.font.sz)  # type: ignore

        if diff_sz > self.font_size_range:
            return 0
        else:
            return int(( self.font_size_range/ diff_sz) * 100)
