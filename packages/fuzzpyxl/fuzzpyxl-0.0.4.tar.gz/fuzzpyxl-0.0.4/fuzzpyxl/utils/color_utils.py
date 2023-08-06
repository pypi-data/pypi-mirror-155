# This converter is based on code found in an openpyxl issue relating to theme/tint color conversion
# https://bitbucket.org/openpyxl/openpyxl/issues/987/add-utility-functions-for-colors-to-help
# Battle-hardened at GRID.is
import colorsys
from functools import lru_cache
from typing import Optional, List, Tuple

from openpyxl.styles import Color as oxlColor
from openpyxl.styles.colors import COLOR_INDEX as OXL_COLOR_INDEX
from openpyxl.xml.functions import QName, fromstring  # type: ignore
from openpyxl.workbook.workbook import Workbook  # type: ignore


class OpenpyxlWorkbookTheme:
    XML_NAMESPACE = "http://schemas.openxmlformats.org/drawingml/2006/main"

    def __init__(self, workbook: Workbook):
        self._workbook = workbook
        self._theme_colors: Optional[List[str]] = None

    @property
    def colors(self):
        if self._theme_colors is None:
            self._theme_colors = self._load_colors()
        return self._theme_colors

    def _load_colors(self):
        root = fromstring(self._workbook.loaded_theme)
        theme_el = root.find(self._qualify_name("themeElements"))
        color_schemes = theme_el.findall(self._qualify_name("clrScheme"))
        first_color_scheme = color_schemes[0]

        colors = []

        for c in [
            "lt1",
            "dk1",
            "lt2",
            "dk2",
            "accent1",
            "accent2",
            "accent3",
            "accent4",
            "accent5",
            "accent6",
            "hlink",
            "folHlink",
        ]:
            element = first_color_scheme.find(self._qualify_name(c))
            rgb = self._get_rgb_from_theme_color_element(element)
            colors.append(rgb)

        return colors

    @classmethod
    def _qualify_name(cls, name: str) -> str:
        qn = QName(cls.XML_NAMESPACE, name)
        return qn.text

    @staticmethod
    def _get_rgb_from_theme_color_element(element):
        color_attributes = element[0].attrib
        if "window" in color_attributes["val"]:
            return color_attributes["lastClr"]
        else:
            return color_attributes["val"]


class OpenpyxlColorToHexConverter:
    LAST_INDEXED_COLOR_WITH_ARGB_VALUE = 63
    RGBMAX = 0xFF
    HLSMAX = 240  # MS excel's tint function expects that HLS is base 240. see:
    # https://social.msdn.microsoft.com/Forums/en-US/e9d8c136-6d62-4098-9b1b-dac786149f43/excel-color-tint-algorithm-incorrect?forum=os_binaryfile#d3c2ac95-52e0-476b-86f1-e2a697f24969

    def __init__(self, theme: OpenpyxlWorkbookTheme):
        self._theme = theme

    @lru_cache(maxsize=20)
    def __call__(self, color: oxlColor) -> Optional[str]:

        argb = self._color_to_argb(color)
        if argb is None or self._argb_is_transparent(argb):
            return None
        else:
            return argb[2:]

    def _color_to_argb(self, color: oxlColor) -> Optional[str]:
        argb = None
        if color.type == "theme":  # type: ignore
            argb = self._theme_color_and_tint_to_argb(color.theme, color.tint)  # type: ignore
        if color.type == "auto":  # type: ignore
            raise NotImplementedError("color.type auto")  # type: ignore
        elif color.type == "indexed":  # type: ignore
            index = int(color.value)  # type: ignore
            if index <= self.LAST_INDEXED_COLOR_WITH_ARGB_VALUE:
                argb = OXL_COLOR_INDEX[index]
                # For some inexplicable reason, the alpha value is 00 for indexed colours according to ECMA-376
                # We need to force it to FF
                argb = "FF" + argb[2:]
        elif color.type == "rgb":  # type: ignore
            argb = color.value  # type: ignore
        return argb

    @staticmethod
    def _argb_to_rgba(rgba: Optional[str]) -> Optional[str]:
        if rgba is not None:
            assert len(rgba) == 8, "Expected 4-byte hex-encoded string of length 8"
            return rgba[2:8] + rgba[0:2]
        else:
            return None

    @staticmethod
    def _argb_is_transparent(rgba: str) -> bool:
        return rgba.startswith("00")

    @staticmethod
    def _drop_alpha_if_opaque(rgba: str) -> str:
        return rgba[:-2] if rgba.endswith("FF") else rgba

    @staticmethod
    def _use_4bit_per_channel_if_possible(rgba: str) -> str:
        hex_pairs = [rgba[x : x + 2] for x in range(0, len(rgba), 2)]
        if all(p[0] == p[1] for p in hex_pairs):
            return rgba[::2]
        return rgba

    @classmethod
    def simplify_rgba(cls, rgba: str) -> str:
        simplified = cls._drop_alpha_if_opaque(rgba)
        simplified = cls._use_4bit_per_channel_if_possible(simplified)
        return simplified

    def _theme_color_and_tint_to_argb(self, color_index: int, tint: float):
        rgb = self._theme.colors[color_index]
        hue, lightness, saturation = self._rgb_to_hls(rgb)
        lightness = self._apply_tint(tint, lightness)
        return "FF" + self._hls_to_rgb(hue, lightness, saturation)

    @classmethod
    def _rgb_to_hls(cls, rgb: str) -> Tuple[int, ...]:
        red = int(rgb[0:2], 16) / cls.RGBMAX
        green = int(rgb[2:4], 16) / cls.RGBMAX
        blue = int(rgb[4:], 16) / cls.RGBMAX

        hls_float = colorsys.rgb_to_hls(red, green, blue)
        hls_int = tuple(int(round(v * cls.HLSMAX)) for v in hls_float)
        return hls_int

    @classmethod
    def _hls_to_rgb(cls, hue: int, lightness: int, saturation: int):
        rgb_float = colorsys.hls_to_rgb(
            hue / cls.HLSMAX, lightness / cls.HLSMAX, saturation / cls.HLSMAX
        )
        rgb_int = tuple(int(round(v * cls.RGBMAX)) for v in rgb_float)
        rgb_hex = ("%02x%02x%02x" % rgb_int).upper()
        return rgb_hex

    @classmethod
    def _apply_tint(cls, tint: float, lightness: int) -> int:
        # How to apply tint values is explained on pages 1756-1757 in the 1st part of the ECMA standard (5th edition)
        if tint < 0:
            # Make darker
            epsilon = 1.0 + tint
            resulting_lightness = epsilon * lightness
        else:
            # Make brighter
            epsilon = 1.0 - tint
            resulting_lightness = epsilon * lightness + (1.0 - epsilon) * cls.HLSMAX
        return int(round(resulting_lightness))


def delta_e_from_hex(color1: str, color2: str) -> float:
    from colormath.color_objects import sRGBColor, LabColor  # type: ignore
    from colormath.color_conversions import convert_color  # type: ignore
    from colormath.color_diff import delta_e_cie2000  # type: ignore

    color1_rgb = sRGBColor.new_from_rgb_hex(color1)
    color2_rgb = sRGBColor.new_from_rgb_hex(color2)
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)

    delta_e = delta_e_cie2000(color1_lab, color2_lab)

    return delta_e
