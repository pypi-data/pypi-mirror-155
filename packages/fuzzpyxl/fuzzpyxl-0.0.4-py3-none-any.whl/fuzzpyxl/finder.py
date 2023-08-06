from dataclasses import dataclass
from collections import namedtuple
from typing import Callable, List, Optional, Union, Tuple

from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class CellArea:
    """Defines a area inside a Excel Page, index starts from 1"""

    min_row: Optional[int] = None
    max_row: Optional[int] = None
    min_col: Optional[int] = None
    max_col: Optional[int] = None


def find_values_in_area_callback(
    worksheet: Worksheet,
    search_cell: Callable[[Cell], bool],
    search_area: CellArea,
) -> List[Cell]:
    """find all occurences of a value inside a given area with a callback function

    Args:
        worksheet (Worksheet): Worksheet
        search_cell (Callable[[Cell], bool]): callback function wich return if
            the cell is of the specific value or color or else
        search_area (CellArea): area to serach the Excelpage


    Returns:
        List[Cell]: All found cells wich contain value
    """
    result = [
        cell
        for row in worksheet.iter_rows(
            min_row=search_area.min_row,
            max_row=search_area.max_row,
            min_col=search_area.min_col,
            max_col=search_area.max_col,
        )
        for cell in row
        if search_cell(cell)
    ]

    return result


def find_values_in_area(
    worksheet: Worksheet,
    search_cell: Union[str, int, float, Callable[[Cell], bool]],
    search_area: CellArea,
) -> List[Cell]:
    """find all occurences of a value inside a given area

    Args:
        worksheet (Worksheet): Worksheet
        search_cell: (Union[str, int, float, Callable[[Cell], bool]]),: Value or callabe,
            for a value the value of the cell is choosen
        search_area (CellArea): area to serach the Excelpage

    Returns:
        List[Cell]: All found cells wich match to the callback
    """

    tmp = (
        search_cell if callable(search_cell) else lambda cell: cell.value == search_cell
    )

    result = find_values_in_area_callback(
        worksheet=worksheet,
        search_cell=tmp,
        search_area=search_area,
    )
    return result


def find_first_value_in_area(
    worksheet: Worksheet,
    search_cell: Union[str, int, float, Callable[[Cell], bool]],
    search_area: CellArea,
    row_direction: str = "first",
    col_direction: str = "first",
    major_direction: str = "row",
) -> Optional[Cell]:
    """get first matched value in the searcharea

    Args:
        worksheet (Worksheet): Worksheet
        search_cell: (Union[str, asd, float,Callable[[Cell], bool]),: Value or callabe,
            for a value the value of the cell is choosen
        search_area (CellArea): area to serach the Excelpage
        row_direction (str, optional): get first or last value in row direction [first,last].
            Defaults to "first".
        col_direction (str, optional): get first or last value in coloumn direction [first,last].
             Defaults to "first".
        major_direction (str, optional): if to order by row of coloumn
            first[row,column]. Defaults to "row".

    Returns:
        Optional[Cell]: Returns the found cell or None
    """

    result = find_n_values_in_area(
        worksheet=worksheet,
        search_cell=search_cell,
        search_area=search_area,
        row_direction=row_direction,
        col_direction=col_direction,
        major_direction=major_direction,
        num_results=1,
    )
    if result is None:
        return None
    return result[0]


def find_n_values_in_area(
    worksheet: Worksheet,
    search_cell: Union[str, int, float, Callable[[Cell], bool]],
    search_area: CellArea,
    row_direction: str = "first",
    col_direction: str = "first",
    major_direction: str = "row",
    num_results: int = -1,
) -> Optional[List[Cell]]:
    """get n matched values in the searcharea

    Args:
        worksheet (Worksheet): Worksheet
        search_cell (Union[str,int,float]): Valeu to look for in the area
        search_area (CellArea): area to serach the Excelpage
        row_direction (str, optional): get first or last value in row direction [first,last].
            Defaults to "first".
        col_direction (str, optional): get first or last value in coloumn direction [first,last].
            Defaults to "first".
        major_direction (str, optional): if to order by row of coloumn first[row,column].
            Defaults to "row".
        num_results (str, optional): How many results to return. Defaults to -1. When set to negative all values are returned

    Returns:
        Optional[Cell]: Returns the found cell or None
    """

    found_cells = find_values_in_area(
        worksheet=worksheet,
        search_cell=search_cell,
        search_area=search_area,
    )
    if not found_cells:
        return None
    Cellidx = namedtuple("Cellidx", "orig_idx row column")
    cell_idxs = [
        Cellidx(idx, cell.row, cell.column) for idx, cell in enumerate(found_cells)
    ]
    max_row = max(cell_idx.row for cell_idx in cell_idxs)
    max_col = max(cell_idx.column for cell_idx in cell_idxs)

    if row_direction == "first":
        row_offset_f = lambda row: row
    elif row_direction == "last":
        row_offset_f = lambda row: max_row - row
    else:
        raise ValueError(f"invalid argument row_direction {row_direction}")

    if col_direction == "first":
        col_offset_f = lambda col: col
    elif col_direction == "last":
        col_offset_f = lambda col: max_col - col
    else:
        raise ValueError(f"invalid argument col_direction {col_direction}")

    if major_direction == "row":
        sort_f = lambda el: (row_offset_f(el.row), col_offset_f(el.column))
    elif major_direction == "column":
        sort_f = lambda el: (col_offset_f(el.column), row_offset_f(el.row))
    else:
        raise ValueError(f"invalid argument major_direction {major_direction}")

    sorted_cell_idxs = sorted(cell_idxs, key=sort_f)
    if num_results < 0:
        sliced_sorted_cell_idxs = sorted_cell_idxs
    elif num_results > 0:
        sliced_sorted_cell_idxs = sorted_cell_idxs[:num_results]
    else:
        raise ValueError(f"the value {num_results} is Invalid for num_results")

    result = [
        found_cells[sorted_cell.orig_idx] for sorted_cell in sliced_sorted_cell_idxs
    ]
    return result


def find_table_area(
    worksheet: Worksheet,
    search_area: CellArea,
    top_left_search_cell: Union[str, int, float, Callable[[Cell], bool]],
    bottom_right_search_cell: Union[str, int, float, Callable[[Cell], bool]],
) -> Optional[Tuple[Cell, Cell]]:
    """Return the top left and bottom right index of the Table object, when there are multiple or None found values None is returned

    Args:
        worksheet (Worksheet): Worksheet
        search_area (CellArea): area to serach the Excelpage
        top_left_search_cell (Union[str, int, float, Callable[[Cell], bool]]): Value to look for to determine top left corner
        bottom_right_search_cell (Union[str, int, float, Callable[[Cell], bool]]):  Value to look for to determine the bottom right corner

    Returns:
        Optional[Tuple[Cell]]: top_left and bottom_right Cell if found, else None
    """

    top_left = find_n_values_in_area(
        worksheet=worksheet,
        search_cell=top_left_search_cell,
        search_area=search_area,
        row_direction="first",
        col_direction="first",
        major_direction="row",
    )

    bottom_right = find_n_values_in_area(
        worksheet=worksheet,
        search_cell=bottom_right_search_cell,
        search_area=search_area,
        row_direction="last",
        col_direction="last",
        major_direction="row",
    )

    if top_left is None:
        return None
    elif len(top_left) > 1:
        return None

    if bottom_right is None:
        return None
    elif len(bottom_right) > 1:
        return None

    top_left, bottom_right = top_left[0], bottom_right[0]

    return (top_left, bottom_right)
