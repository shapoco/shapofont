"""Loading of font design images.

A design image is a PNG with a black background, white (or gray) glyphs,
red "glyph marker" lines below each glyph and optional blue "anti-spacer"
lines below the markers.
"""

from __future__ import annotations

from PIL import Image


class Marker:
    """Special pixel values stored in a GrayBitmap for marker colors."""

    GLYPH = -1  # red line: glyph marker
    SPACING = -2  # blue line: left/right side anti-spacer


def rgb_to_hsv(rgb: tuple[int, ...]) -> tuple[float, int, int]:
    """Return (hue in degrees, chroma 0-255, value 0-255)."""
    r, g, b = rgb[0], rgb[1], rgb[2]
    mx = max(r, g, b)
    mn = min(r, g, b)
    chroma = mx - mn
    if chroma == 0:
        h = 0.0
    elif mn == b:
        h = 60 + (g - r) * 60 / chroma
    elif mn == r:
        h = 180 + (b - g) * 60 / chroma
    else:
        h = 300 + (r - b) * 60 / chroma
    return (h, chroma, mx)


def quantize_gray(value: int, bits_per_pixel: int) -> int:
    """Quantize a 0-255 gray value to `bits_per_pixel` levels, scaled back to 0-255."""
    levels = (1 << bits_per_pixel) - 1
    level = (value * levels + 127) // 255
    return level * 255 // levels


def classify_pixel(rgb: tuple[int, ...], bits_per_pixel: int) -> int:
    """Map a design pixel to a gray value (0-255) or a Marker value."""
    h, chroma, v = rgb_to_hsv(rgb)
    if chroma < 64:
        return quantize_gray(v, bits_per_pixel)
    if chroma >= 128 and v > 128:
        if h < 30 or 330 <= h:
            return Marker.GLYPH
        if 210 < h <= 270:
            return Marker.SPACING
    raise ValueError(f"Unknown pixel color: #{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}")


class GrayBitmap:
    """A 2D array of gray values (0-255) and Marker values.

    `crop()` returns a view sharing the same backing list, so `offset` and
    `stride` describe where the view lives inside `data`.
    """

    def __init__(self, data: list[int], width: int, height: int, offset: int = 0, stride: int | None = None):
        self.data = data
        self.width = width
        self.height = height
        self.offset = offset
        self.stride = width if stride is None else stride

    @staticmethod
    def create(width: int, height: int) -> "GrayBitmap":
        return GrayBitmap([0] * (width * height), width, height)

    @staticmethod
    def from_file(file_path: str, bits_per_pixel: int) -> "GrayBitmap":
        if bits_per_pixel not in (1, 2, 4, 8):
            raise ValueError(f"Unsupported bits_per_pixel: {bits_per_pixel}")
        with Image.open(file_path) as pil_img:
            rgb_img = pil_img.convert("RGB")
        width, height = rgb_img.size
        data: list[int] = []
        for y in range(height):
            for x in range(width):
                try:
                    data.append(classify_pixel(rgb_img.getpixel((x, y)), bits_per_pixel))
                except ValueError as e:
                    raise ValueError(f"{file_path} ({x}, {y}): {e}") from e
        return GrayBitmap(data, width, height)

    def export(self, file_path: str) -> None:
        """Save as a grayscale PNG, lifting black slightly so the glyphs stand out."""
        pil_img = Image.new("L", (self.width, self.height))
        pixels = [32 + (max(0, self.get(x, y)) * 192 // 256) for y in range(self.height) for x in range(self.width)]
        pil_img.putdata(pixels)
        pil_img.save(file_path)

    def contains(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x: int, y: int, default: int | None = None) -> int:
        if not self.contains(x, y):
            if default is None:
                raise IndexError(f"Index out of bounds: ({x}, {y})")
            return default
        return self.data[self.offset + y * self.stride + x]

    def set(self, x: int, y: int, value: int) -> None:
        if not self.contains(x, y):
            raise IndexError(f"Index out of bounds: ({x}, {y})")
        self.data[self.offset + y * self.stride + x] = value

    def crop(self, x: int, y: int, width: int, height: int) -> "GrayBitmap":
        """Return a view of a sub-rectangle (shares the backing data)."""
        if x < 0 or y < 0 or x + width > self.width or y + height > self.height:
            raise IndexError("Crop dimensions out of bounds")
        return GrayBitmap(self.data, width, height, self.offset + y * self.stride + x, self.stride)

    def bounding_box(self, threshold: int = 1) -> tuple[int, int, int, int] | None:
        """Return (x, y, w, h) of the pixels >= threshold, or None if empty."""
        x_min, y_min, x_max, y_max = self.width, self.height, -1, -1
        for y in range(self.height):
            for x in range(self.width):
                if self.get(x, y) >= threshold:
                    x_min, x_max = min(x_min, x), max(x_max, x)
                    y_min, y_max = min(y_min, y), max(y_max, y)
        if x_max < 0:
            return None
        return (x_min, y_min, x_max - x_min + 1, y_max - y_min + 1)

    def draw(self, src: "GrayBitmap", x: int, y: int, scale: int = 1) -> None:
        """Alpha-blend `src` onto this bitmap at (x, y), scaled by an integer factor."""
        for sy in range(src.height):
            for sx in range(src.width):
                col = src.get(sx, sy)
                if col <= 0:
                    continue
                for y_sub in range(scale):
                    for x_sub in range(scale):
                        dx = x + sx * scale + x_sub
                        dy = y + sy * scale + y_sub
                        if not self.contains(dx, dy):
                            continue
                        bg = self.get(dx, dy)
                        self.set(dx, dy, bg + ((255 - bg) * col + 128) // 255)
