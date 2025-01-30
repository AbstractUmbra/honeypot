import pathlib
from collections.abc import Mapping
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

_BASE_IMG = pathlib.Path("static/img.png")
if not _BASE_IMG.exists():
    raise RuntimeError("No base image found.")

_BASE_FONT = pathlib.Path("static/font.ttc")
if not _BASE_FONT.exists():
    raise RuntimeError("No font found.")

BASE_DATA = BytesIO(_BASE_IMG.read_bytes())
BASE_DATA.seek(0)

FONT = ImageFont.truetype(str(_BASE_FONT), 15)
FILL = (0, 0, 0)


def find_longest_prefix(text: str, max_width: int = 400) -> int:
    start, end = 0, len(text)

    while start <= end:
        mid = (start + end) // 2
        current_text = text[:mid]

        _, _, width, _ = FONT.getbbox(current_text)
        if width <= max_width:
            start = mid + 1
        else:
            end = mid - 1

    return start


def generate_honeypot_image(ip: str, path: str, method: str, headers: Mapping[str, str]) -> BytesIO:
    image = Image.open(BASE_DATA)
    draw = ImageDraw.Draw(image)

    headers_ = [f"IP: {ip}", f"Route: {path}", f"Method: {method}", " ", "Headers:"]
    headers_ += [f"{key}: {value}" for key, value in headers.items()]

    x, y = 305, 100
    for line in headers_:
        while line:
            index = find_longest_prefix(line)
            _, _, _, height = FONT.getbbox(line[:index])
            draw.text((x, y), text=line[:index], font=FONT, fill=FILL)
            y += height + 2

            line = line[index:]  # noqa: PLW2901 # intended

    output = BytesIO()
    image.save(output, "png")

    output.seek(0)
    BASE_DATA.seek(0)

    return output
