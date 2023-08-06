import io

from PIL import Image, ImageDraw


def draw_circle_at_position(png_bytes: bytes, x: int, y: int, size: int = 25, color='red') -> bytes:
    image = Image.open(io.BytesIO(png_bytes))
    draw = ImageDraw.Draw(image)
    draw.ellipse((x - size / 2, y - size / 2, x + size / 2, y + size / 2), outline=color, width=5)
    draw.ellipse((x - size / 10 / 2, y - size / 10 / 2, x + size / 10 / 2, y + size / 10 / 2), fill=color)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    # image.save("../Draw.png") # <-- Uncomment to see identified objects in image locally
    return img_byte_arr.getvalue()


def draw_rectangle_at_position(png_bytes: bytes, x: int, y: int, width: int, height: int, color='yellow'):
    image = Image.open(io.BytesIO(png_bytes))
    draw = ImageDraw.Draw(image)
    draw.rectangle((x, y, x + width, y + height), outline=color, width=5)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    # image.save("../Draw.png") # <-- Uncomment to see identified objects in image locally
    return img_byte_arr.getvalue()
