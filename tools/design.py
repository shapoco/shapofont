from PIL import Image

class Marker:
    VALID_BOTTOM_LINE = -1
    DISABLED_BOTTOM_LINE = -2

class Bitmap:

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

        return Bitmap(data, w, h, 0, w)

    def get(self, x: int, y: int) -> Marker:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError(f"Index out of bounds: ({x}, {y})")
        return self.data[self.offset + y * self.stride + x]

    def crop(self, x: int, y: int, width: int, height: int):
        if x < 0 or y < 0 or x + width > self.width or y + height > self.height:
            raise IndexError("Crop dimensions out of bounds")
        return Bitmap(
            self.data, width, height, self.offset + y * self.stride + x, self.stride
        )
