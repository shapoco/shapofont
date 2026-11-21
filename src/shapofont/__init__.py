"""ShapoFont: bitmap font tools for embedded projects.

Converts font designs drawn with a painting tool (PNG + JSON) into
Adafruit GFXfont headers and LVGL font sources.
"""

from .design import GrayBitmap, Marker
from .font import BitmapFont, RawGlyph

__all__ = ["GrayBitmap", "Marker", "BitmapFont", "RawGlyph"]
