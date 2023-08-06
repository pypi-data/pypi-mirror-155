from typing import Optional
from fuzzpyxl.utils.color_utils import (
    OpenpyxlColorToHexConverter,
    OpenpyxlWorkbookTheme,
    delta_e_from_hex,
)
from openpyxl.workbook.workbook import Workbook
from openpyxl.styles import Color as oxlColor

from .base import BaseComparer, ReadOnlyCellTypes, SearchCell


class ColorDeltaECompare(BaseComparer):
    def __init__(self, workbook: Workbook, weigth: int = 1):
        theme = OpenpyxlWorkbookTheme(workbook)
        self._cellcolor_to_hex = OpenpyxlColorToHexConverter(theme)
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:

        if cell.fill is None and search_cell.fill_color is None:
            return 100
        elif cell.fill is not None and search_cell.fill_color is None:
            return 100
        elif cell.fill is None and search_cell.fill_color is not None:
            return 0
        

        cell_start_color: oxlColor = cell.fill.start_color
        cell_color_hex = self._cellcolor_to_hex(cell_start_color)  # type: ignore
        search_color_hex = self._cellcolor_to_hex(search_cell.fill_color)  # type: ignore

        if cell_color_hex is None and search_color_hex is None:
            return 100
        elif cell_color_hex is not None and search_color_hex is None:
            return 100
        elif cell_color_hex is None and search_color_hex is not None:
            return 0
        

        delta_e = delta_e_from_hex(cell_color_hex, search_color_hex)  # type: ignore

        return int(delta_e)
