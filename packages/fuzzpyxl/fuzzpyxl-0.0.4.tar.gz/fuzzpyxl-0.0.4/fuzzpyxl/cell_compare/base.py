from abc import ABC, abstractmethod
import re
from typing import Callable, List, Optional, Union,Tuple
from dataclasses import dataclass, field
from openpyxl.styles import Color as oxlColor
from openpyxl.styles.borders import Border as oxlBorder
from openpyxl.styles.borders import Side as oxlSide
from openpyxl.styles.alignment import Alignment as oxlAlignment
from openpyxl.styles.fonts import Font as oxlFont
from openpyxl.worksheet.worksheet import Worksheet

from openpyxl.cell.read_only import ReadOnlyCell, EmptyCell


ReadOnlyCellTypes = Union[ReadOnlyCell, EmptyCell]


def init_oxlBorder(
    left=None,
    right=None,
    top=None,
    bottom=None,
    diagonal=None,
    diagonal_direction=None,
    vertical=None,
    horizontal=None,
    diagonalUp=False,
    diagonalDown=False,
    outline=True,
    start=None,
    end=None,
) -> oxlBorder:
    if right is None:
        right = oxlSide()
    if left is None:
        left = oxlSide()
    if top is None:
        top = oxlSide()
    if bottom is None:
        bottom = oxlSide()
    return oxlBorder(
        left=left,
        right=right,
        top=top,
        bottom=bottom,
        diagonal=diagonal,
        diagonal_direction=diagonal_direction,  # type: ignore
        vertical=vertical,  # type: ignore
        horizontal=horizontal,  # type: ignore
        diagonalUp=diagonalUp,
        diagonalDown=diagonalDown,
        outline=outline,
        start=start,  # type: ignore
        end=end,  # type: ignore
    )


def init_oxlAlignment(
    horizontal=None,
    vertical=None,
    textRotation=0,
    wrapText=None,
    shrinkToFit=None,
    indent=0,
    relativeIndent=0,
    justifyLastLine=None,
    readingOrder=0,
    text_rotation=None,
    wrap_text=None,
    shrink_to_fit=None,
    mergeCell=None,
):

    return oxlAlignment(
        horizontal=horizontal,
        vertical=vertical,
        textRotation=textRotation,
        wrapText=wrapText,
        shrinkToFit=shrinkToFit,
        indent=indent,
        relativeIndent=relativeIndent,
        justifyLastLine=justifyLastLine,
        readingOrder=readingOrder,
        text_rotation=text_rotation,
        wrap_text=wrap_text,
        shrink_to_fit=shrink_to_fit,
        mergeCell=mergeCell,
    )


def init_oxlFont(
    name=None,
    sz=11.0,
    b=True,
    i=False,
    charset=None,
    u=None,
    strike=None,
    color=None,
    scheme=None,
    family=None,
    size=None,
    bold=None,
    italic=None,
    strikethrough=None,
    underline=None,
    vertAlign=None,
    outline=None,
    shadow=None,
    condense=None,
    extend=None,
):

    return oxlFont(
        name=name,
        sz=sz,  # type: ignore
        b=b,
        i=i,
        charset=charset,
        u=u,
        strike=strike,
        color=color,
        scheme=scheme,
        family=family,
        size=size,
        bold=bold,
        italic=italic,
        strikethrough=strikethrough,
        underline=underline,
        vertAlign=vertAlign,
        outline=outline,
        shadow=shadow,
        condense=condense,
        extend=extend,
    )





@dataclass
class SearchCell:
    fill_color: Optional[oxlColor] = None
    data_type: Optional[str] = None
    ignore: bool = False
    cell_type: Optional[ReadOnlyCellTypes] = None    
    border: Optional[oxlBorder] = field(default_factory=init_oxlBorder)
    value: Optional[Union[str, int, float]] = None
    re_pattern:Optional[re.Pattern] = field(default=None)
    alignment: Optional[oxlAlignment] = field(default_factory=init_oxlAlignment)
    font: Optional[oxlFont] = field(default_factory=init_oxlFont)

    def __post_init__(self):
        if self.re_pattern is None:
            return
        if isinstance(self.re_pattern,str):
            self.re_pattern = re.compile(self.re_pattern)


class BaseComparer(ABC):
    def __init__(self, weigth: int):
        self.weigth = weigth

    def compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Tuple[int, int]:
        score = self._compare(cell, search_cell)
        if score is None:
            return (0,0)
         
        return (self.weigth,score)

    @abstractmethod
    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> Optional[int]:
        pass


class CombinedComparer:
    def __init__(self, *args: BaseComparer):
        self.comparers = list(args)

    def compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCell
    ) -> int:
        """Compares a real cell from a docuemnt with a specific cell for wich you are looking for comparison

        Args:
            cell (ReadOnlyCellTypes): input cell from the duument
            search_cell (SearchCell): input cell wich cell is compared total_weigth

        Returns:
            int: Return a vlue between 0 and 100, 100 means they are the same, 0 means they are totally different
        """
        
        if search_cell.ignore:
            return 100
        
        total_weight,total_match_score = 0,0
        for comparer in self.comparers:
            weigth,unweighted_score = comparer.compare(cell, search_cell)
            score = (weigth * unweighted_score)
            total_weight += weigth
            total_match_score += score

        if total_weight == 0:
            return 0
        res_scaled = int(total_match_score / total_weight) # put the result again between 0 and 100
        return res_scaled


def find_row_idxs(ws: Worksheet,row_definition:List[SearchCell],matcher:CombinedComparer,thershhold:int = 85):

    found_idxs = []
    for row_idx,row in enumerate(ws,start =1):
        per_row_values = []
        for cell, search_cell in zip(row, row_definition):
            value = matcher.compare(cell, search_cell)
            per_row_values.append(value)


        if (sum(per_row_values) / len(row_definition)) > thershhold:
            found_idxs.append(row_idx)

    return found_idxs