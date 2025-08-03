from PIL import Image


class Marker:
    GLYPH = -1
    SPACING = -2


def to_hsv(rgb) -> tuple[float, float, float]:
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    mx = max(r, g, b)
    mn = min(r, g, b)
    dr = mx - mn
    if mx == mn:
        h = 0
    elif mn == b:
        h = 60 + (g - r) * 60 / dr
    elif mn == r:
        h = 180 + (b - g) * 60 / dr
    elif mn == g:
        h = 300 + (r - b) * 60 / dr
    return (h, dr, mx)


class GrayBitmap:

    def __init__(self, data: list[int], w: int, h: int, offset: int, stride: int):
        self.data = data
        self.width = w
        self.height = h
        self.offset = offset
        self.stride = stride

    def from_file(file_path: str):
        pil_img = Image.open(file_path)
        width, height = pil_img.size
        data: list[int] = []
        for y in range(height):
            for x in range(width):
                (h, s, v) = to_hsv(pil_img.getpixel((x, y)))
                if s < 64:
                    data.append(v)
                    continue
                elif s >= 128 and v > 128:
                    if h < 30 or 330 <= h:
                        # red
                        data.append(Marker.GLYPH)
                    elif 210 < h <= 270:
                        # blue
                        data.append(Marker.SPACING)
                    else:
                        raise ValueError("Unknown pixel color")

        pil_img.close()

        return GrayBitmap(data, width, height, 0, width)

    def get(self, x: int, y: int, default_col: int | None = None) -> Marker:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            if default_col == None:
                raise IndexError(f"Index out of bounds: ({x}, {y})")
            else:
                return default_col
        return self.data[self.offset + y * self.stride + x]

    def crop(self, x: int, y: int, width: int, height: int):
        if x < 0 or y < 0 or x + width > self.width or y + height > self.height:
            raise IndexError("Crop dimensions out of bounds")
        return GrayBitmap(
            self.data, width, height, self.offset + y * self.stride + x, self.stride
        )

    def to_byte_segments(self, vertical_frag: bool, msb1st: bool) -> list[int]:
        array = []

        if vertical_frag:
            for y_coarse in range(0, self.height, 8):
                for x in range(self.width):
                    byte = 0
                    for y_fine in range(8):
                        y = y_coarse + y_fine
                        i_bit = 7 - y_fine if msb1st else y_fine
                        if y < self.height and self.get(x, y) >= 128:
                            byte |= 1 << i_bit
                    array.append(byte)
        else:
            for x_coarse in range(0, self.width, 8):
                for y in range(self.height):
                    byte = 0
                    for x_fine in range(8):
                        x = x_coarse + x_fine
                        i_bit = 7 - x_fine if msb1st else x_fine
                        if x < self.width and self.get(x, y) >= 128:
                            byte |= 1 << i_bit
                    array.append(byte)

        return array
