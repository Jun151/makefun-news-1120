"""Authoring tool. The contest runs main.py and needs no drawing libraries."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
SCALE = 2
PAPER = "#f7f2e8"
INK = "#102c35"
FADED = "#4d6062"
RULE = "#b7b8a9"
OCEAN = "#103740"
GRID = "#28505a"
LAND = "#45727a"
GOLD = "#ffca78"
RED = "#a33d30"
SERIF = "georgiab.ttf"
SANS = "arial.ttf"
BOLD = "arialbd.ttf"

STORIES = [
    ("2", "POLAND & UKRAINE  /  WAR", ("Russian missiles", "land in Poland"),
     ("NATO condemned the breach. Russian", "strikes also hit three bridges in Kyiv."), 21.8, 50.4, 731, 218),
    ("3", "TÜRKIYE  /  CLIMATE", ("COP31 talks", "go into overtime"),
     ("The draft deal drew criticism for", "omitting any mention of fossil fuels."), 30.7, 36.9, 748, 282),
    ("4", "IRAN  /  DIPLOMACY", ("Trump doubts", "deal with Iran"),
     ("He said Tehran wanted an agreement but", "would not offer terms he could accept."), 51.4, 35.7, 813, 255),
    ("5", "MYANMAR  /  JUSTICE", ("Myanmar rejects", "genocide ruling"),
     ("The UN’s top court found Myanmar", "responsible for genocide of Rohingya."), 96.1, 19.8, 845, 315),
    ("6", "SUDAN  /  CIVIL WAR", ("Blue Nile moves", "to mobilize troops"),
     ("A rival armed alliance claimed it had", "seized more towns in southeast Sudan."), 34.4, 11.8, 781, 326),
    ("7", "PERU  /  EARTHQUAKE", ("6.7 quake shakes", "the Peruvian Andes"),
     ("The Friday evening quake struck near", "Carhuamayo and was felt in Lima."), -75.85, -10.84, 574, 335),
]


def render(land_path: Path, fonts: Path, output: Path) -> None:
    image = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), PAPER)
    draw = ImageDraw.Draw(image)

    def coordinates(values):
        return tuple(round(value * SCALE) for value in values)

    def label(x, y, words, size, face=SANS, color=INK, anchor="lt"):
        font = ImageFont.truetype(str(fonts / face), size * SCALE)
        draw.text(coordinates((x, y)), words, fill=color, font=font, anchor=anchor)

    def line(points, color, width=1):
        draw.line(coordinates(points), fill=color, width=width * SCALE)

    def box(left, top, right, bottom, color):
        draw.rectangle(coordinates((left, top, right, bottom)), fill=color)

    def badge(x, y, number, face, type_color, radius=13):
        draw.ellipse(coordinates((x-radius, y-radius, x+radius, y+radius)), fill=face)
        label(x, y, number, 15, BOLD, type_color, "mm")

    def project(lon, lat):
        return 449 + (lon + 180) * 1.46, 187 + (84 - lat) * 1.48

    box(0, 0, SIZE, 10, RED)
    label(40, 32, "WORLD NEWS", 20, BOLD, RED)
    label(984, 28, "FRIDAY  /  20 NOVEMBER 2026", 28, BOLD, INK, "rt")
    label(37, 64, "The World Edition", 68, SERIF)
    line((40, 141, 984, 141), INK, 2)

    box(40, 158, 984, 428, OCEAN)
    for lon in range(-180, 181, 30):
        line((*project(lon, 84), *project(lon, -60)), GRID)
    for lat in range(-60, 81, 20):
        line((*project(-180, lat), *project(180, lat)), GRID)

    data = json.loads(land_path.read_text(encoding="utf-8"))
    for feature in data["features"]:
        geometry = feature["geometry"]
        polygons = geometry["coordinates"]
        if geometry["type"] == "Polygon":
            polygons = [polygons]
        for exterior, *_ in polygons:
            if max(lat for _, lat in exterior) < -60:
                continue
            points = [coordinates(project(lon, max(lat, -60))) for lon, lat in exterior]
            draw.polygon(points, fill=LAND)

    # Connect the crowded European and Asian locations to separated map labels.
    markers = [
        ("1", 114.06, 22.54, 915, 291),
        *((number, *location) for number, _, _, _, *location in STORIES),
    ]
    for number, lon, lat, x, y in markers:
        px, py = project(lon, lat)
        line((px, py, x, y), GOLD, 2)
        draw.ellipse(coordinates((px-3, py-3, px+3, py+3)), fill=GOLD)
        badge(x, y, number, GOLD, INK)

    badge(70, 190, "1", GOLD, INK)
    label(93, 183, "U.S.  /  CHINA  /  RUSSIA", 17, BOLD, GOLD)
    label(57, 215, "China’s nuclear", 43, SERIF, PAPER)
    label(57, 270, "buildup in focus", 43, SERIF, PAPER)
    for y, words in zip((337, 363, 389), (
        "Trump warned of a rapid buildup a day",
        "after the three powers pledged talks",
        "on nuclear risks at the Shenzhen summit.",
    )):
        label(59, y, words, 20, SANS, PAPER)

    for index, story in enumerate(STORIES):
        number, section, headline, detail, *_ = story
        row, column = divmod(index, 2)
        left = 40 + column * 480
        top = 450 + row * 174
        line((left, top, left + 464, top), RULE)
        badge(left + 13, top + 27, number, RED, PAPER)
        label(left + 35, top + 20, section, 17, BOLD, RED)
        for index_line, words in enumerate(headline):
            label(left, top + 44 + index_line * 39, words, 36, SERIF)
        for index_line, words in enumerate(detail):
            label(left, top + 127 + index_line * 23, words, 20, SANS, FADED)

    line((512, 450, 512, 959), RULE)
    line((40, 976, 984, 976), INK, 2)
    label(40, 990, "REPORTING  AP  /  REUTERS  /  SUDAN TRIBUNE", 14, BOLD)
    label(984, 990, "VERIFICATION  UNFCCC  /  USGS", 14, BOLD, INK, "rt")

    image.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(output, optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("land", type=Path, help="Natural Earth 110m land GeoJSON")
    parser.add_argument("--fonts", type=Path, default=Path("C:/Windows/Fonts"))
    args = parser.parse_args()
    render(args.land, args.fonts, Path(__file__).with_name("world-edition.png"))
