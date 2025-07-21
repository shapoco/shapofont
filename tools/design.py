from PIL import Image


class Marker:
    VALID_BOTTOM_LINE = -1
    DISABLED_BOTTOM_LINE = -2


class GrayBitmap:

    def __init__(self, data: list[int], w: int, h: int, offset: int, stride: int):
        self.data = data
        self.width = w
        self.height = h
        self.offset = offset
        self.stride = stride

    def from_file(file_path: str):
        pil_img = Image.open(file_path)
        w, h = pil_img.size
        data: list[int] = []
        for y in range(h):
            for x in range(w):
                (r, g, b, a) = pil_img.getpixel((x, y))
                if r > 192 and g < 64 and b < 64:
                    data.append(Marker.VALID_BOTTOM_LINE)
                elif r < 64 and g < 64 and b > 192:
                    data.append(Marker.DISABLED_BOTTOM_LINE)
                else:
                    gray = (r + g + b) // 3
                    data.append(gray)

        pil_img.close()

        return GrayBitmap(data, w, h, 0, w)

    def get(self, x: int, y: int) -> Marker:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError(f"Index out of bounds: ({x}, {y})")
        return self.data[self.offset + y * self.stride + x]

    def crop(self, x: int, y: int, width: int, height: int):
        if x < 0 or y < 0 or x + width > self.width or y + height > self.height:
            raise IndexError("Crop dimensions out of bounds")
        return GrayBitmap(
            self.data, width, height, self.offset + y * self.stride + x, self.stride
        )

    def to_byte_segments(self, vertical_scan: bool, bit_reverse: bool) -> list[int]:
        array = []

        if vertical_scan:
            for x_coarse in range(0, self.width, 8):
                for y in range(self.height):
                    byte = 0
                    for x_fine in range(8):
                        x = x_coarse + x_fine
                        i_bit = 7 - x_fine if bit_reverse else x_fine
                        if x < self.width and self.get(x, y) >= 128:
                            byte |= 1 << i_bit
                    array.append(byte)
        else:
            for y_coarse in range(0, self.height, 8):
                for x in range(self.width):
                    byte = 0
                    for y_fine in range(8):
                        y = y_coarse + y_fine
                        i_bit = 7 - y_fine if bit_reverse else y_fine
                        if y < self.height and self.get(x, y) >= 128:
                            byte |= 1 << i_bit
                    array.append(byte)

        return array
