"""Render the 30-story print edition from local fonts and Natural Earth data."""

import argparse
import json
import re
from functools import cache
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from edition_news import BRIEFS, CARDS, LEADS, LEAD_DETAILS


PAPER = "#f7efdf"
INK = "#192c30"
RED = "#972f28"
RULE = "#c2b39a"
SCALE = 2
ROOT = Path(__file__).resolve().parent
STATS = re.compile(r"(\b(?:M6\.7|3\.7%|0\.6%|2\.2%|2032|19\+|3(?= Kyiv)))")

GLYPHS = {
    "link": [(-16,-2,-7,-11,0,-11,4,-7,-3,0), (16,2,7,11,0,11,-4,7,3,0), (-7,6,7,-6)],
    "pulse": [(-16,0,-7,0,-3,-9,2,12,7,-4,11,0,16,0)],
    "chart": [(-14,-13,-14,13,15,13), (-10,-8,-3,-2,2,-5,13,7), (6,7,13,7,13,0)],
    "scales": [(0,-13,0,14,-9,14,9,14), (-13,-7,13,-7), (-9,-7,-15,5,-4,5,-9,-7),
               (9,-7,4,5,15,5,9,-7)],
    "quake": [(-16,8,-8,-6,-3,-1,4,-11,16,8), (-16,12,16,12), (-4,5,-1,-3,3,7)],
    "exchange": [(-15,-6,14,-6,7,-12), (15,7,-14,7,-7,1)],
    "flag": [(-9,15,-9,-13,14,-13,7,-6,14,0,-9,0)],
    "rain": [(-15,3,-15,-2,-9,-5,-6,-11,2,-13,9,-6,14,-5,16,3,-15,3),
             (-8,8,-11,14), (1,8,-2,14), (10,8,7,14)],
    "shield": [(-12,-9,0,-13,12,-9,10,4,0,14,-10,4,-12,-9), (-5,0,-1,4,6,-4)],
}


def render(land_path: Path, fonts: Path, destination: Path) -> None:
    image = Image.new("RGB", (1024*SCALE, 1024*SCALE), PAPER)
    draw = ImageDraw.Draw(image)

    def pixels(values):
        return tuple(round(value*SCALE) for value in values)

    @cache
    def font(face, size):
        return ImageFont.truetype(str(fonts / face), size*SCALE)

    def caption(x, y, words, size, color=INK, face="arialbd.ttf",
                limit=None, anchor="lt", stats=False):
        chosen = font(face, size)
        if limit is not None and chosen.getlength(words) > limit*SCALE:
            raise ValueError(f"Text exceeds its column: {words}")
        if stats:
            for index, part in enumerate(STATS.split(words)):
                draw.text(pixels((x,y)), part, font=chosen, fill=RED if index%2 else color,
                          anchor="ls")
                x += chosen.getlength(part)/SCALE
        else:
            draw.text(pixels((x,y)), words, font=chosen, fill=color, anchor=anchor)

    def line(points, color, width=1):
        draw.line(pixels(points), fill=color, width=round(width*SCALE), joint="curve")

    def rect(bounds, color):
        draw.rectangle(pixels(bounds), fill=color)

    def oval(bounds, color=None, outline=None, width=1):
        draw.ellipse(pixels(bounds), fill=color, outline=outline, width=round(width*SCALE))

    def polygon(points, color):
        draw.polygon(pixels(points), fill=color)

    def bridge(x, y):
        rect((x,y,x+310,y+102), "#203a43")
        oval((x+211,y+8,x+286,y+83), "#d88d62")
        polygon((x,y+66,x+62,y+41,x+134,y+65,x+201,y+48,x+310,y+70,x+310,y+102,x,y+102),
                "#31535a")
        for Y in (75, 85, 94):
            line((x+6,y+Y,x+304,y+Y), "#709694")
        for left, right in ((17,144),(168,293)):
            line((x+left,y+60,x+right,y+60), PAPER, 5)
            for offset in (left+17, right-19):
                line((x+offset,y+61,x+offset,y+91), PAPER, 3)
        line((x+133,y+41,x+149,y+50,x+146,y+58,x+158,y+66), "#ffad75", 3)
        line((x+166,y+44,x+159,y+53,x+164,y+58), "#ffad75", 2)

    def climate(x, y):
        rect((x,y,x+310,y+102), "#27483d")
        oval((x+114,y+7,x+202,y+95), "#bdd2a0")
        for offset in (18,32,46):
            oval((x+114+offset,y+7,x+202-offset/2,y+95), outline="#496a50")
        for Y in (34,51,68):
            line((x+120,y+Y,x+196,y+Y), "#496a50")
        for tower, height in ((24,37),(57,54),(83,27)):
            rect((x+tower,y+99-height,x+tower+12,y+101), "#d8a174")
        for bx, by in ((65,35),(78,28),(91,29)):
            oval((x+bx-9,y+by-5,x+bx+9,y+by+5), "#d8a174")
        line((x+249,y+39,x+249,y+78), PAPER, 7)
        oval((x+237,y+74,x+261,y+98), "#f0be7b")
        for Y in (45,54,63):
            line((x+258,y+Y,x+271,y+Y), PAPER, 2)

    def nuclear(x, y):
        rect((x,y,x+310,y+102), "#612e30")
        for radius in (33,44):
            oval((x+155-radius,y+51-radius,x+155+radius,y+51+radius), outline="#a8584a")
        for turn in (0, pi/3, 2*pi/3):
            orbit = []
            for step in range(97):
                angle = step*pi/48
                a,b = 47*cos(angle), 15*sin(angle)
                orbit.extend((x+155+a*cos(turn)-b*sin(turn), y+51+a*sin(turn)+b*cos(turn)))
            line(orbit, "#ffbd88", 3)
        oval((x+149,y+45,x+161,y+57), "#ffbd88")
        for point_x, point_y in ((41,36),(267,29),(59,76),(250,78),(284,62)):
            oval((x+point_x-3,y+point_y-3,x+point_x+3,y+point_y+3), "#c17e6b")

    def project(lon, lat):
        return 778 + (lon+180)*0.57, 20 + (84-lat)*0.37

    for feature in json.loads(land_path.read_text(encoding="utf-8"))["features"]:
        geometry = feature["geometry"]
        shapes = geometry["coordinates"]
        if geometry["type"] == "Polygon":
            shapes = [shapes]
        for exterior, *_ in shapes:
            if max(lat for _, lat in exterior) >= -60:
                points = tuple(value for lon, lat in exterior for value in project(lon, max(lat,-60)))
                polygon(points, "#778b7e")
    for lon, lat in ((-76,-11),(-81,28),(-77,39),(21,50),(31,37),(34,12),(96,20),(151,-33)):
        x,y = project(lon,lat)
        oval((x-2,y-2,x+2,y+2), RED)

    rect((28,13,996,17), INK)
    caption(28,27,"THE WORLD EDITION",52,face="georgiab.ttf")
    caption(30,88,"FRIDAY 20 NOVEMBER 2026",22,RED)
    count = len(LEADS) + len(CARDS) + sum(len(stories) for _, stories in BRIEFS)
    caption(996,88,f"{count} STORIES ACROSS SIX CONTINENTS",15,anchor="rt")
    rect((28,115,996,117), INK)

    for i, ((region, words, _, credit, _), draw_scene, detail) in enumerate(
        zip(LEADS, (bridge, climate, nuclear), LEAD_DETAILS, strict=True)
    ):
        x = 28+329*i
        draw_scene(x,125)
        caption(x,238,region,13,RED,limit=238)
        caption(x+310,238,credit,13,anchor="rt")
        for row, words_line in enumerate(words):
            caption(x,259+row*31,words_line,24,face="georgiab.ttf",limit=310)
        caption(x,335,detail,15,limit=310,stats=True)
    rect((28,350,996,351), RULE)

    accents = ("#e3e8d5", "#ecd4c9", "#d9e5e3")
    for i, (region, words, icon, credit, _) in enumerate(CARDS):
        row, col = divmod(i,3)
        x,y = 28+329*col, 362+87*row
        rect((x,y,x+310,y+78), "#eee3cf")
        oval((x+8,y+13,x+59,y+64), accents[(row+col)%3])
        for segment in GLYPHS[icon]:
            points = tuple(value+(x+33 if j%2==0 else y+38) for j,value in enumerate(segment))
            line(points, RED, 2.5)
        caption(x+66,y+9,region,12,RED,limit=173)
        caption(x+303,y+9,credit,12,anchor="rt")
        for offset, words_line in enumerate(words):
            caption(x+66,y+42+20*offset,words_line,19,limit=237,stats=True)

    for col, (section, stories) in enumerate(BRIEFS):
        x = 28+329*col
        rect((x,630,x+310,658), INK)
        caption(x+8,637,section,15,PAPER)
        for row, (region, headline, credit, _) in enumerate(stories):
            y = 670+48*row
            caption(x,y,region,13,RED,limit=205)
            caption(x+310,y,credit,13,anchor="rt")
            caption(x,y+30,headline,17,limit=310,stats=True)
            rect((x,y+39,x+310,y+39), RULE)

    rect((28,962,996,1010), "#e0d5bf")
    caption(38,969,"DATE CHECK",15,RED)
    caption(150,969,"Nov 20 local events or first reports only. Earlier standalone stories excluded.",15,limit=833)
    caption(150,990,"Nov 19 Shenzhen summit is context; Peru quake was Nov 20 locally (Nov 21 UTC).",14,limit=833)
    image.resize((1024,1024), Image.Resampling.LANCZOS).save(destination, optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("land", type=Path)
    parser.add_argument("--fonts", type=Path, default=Path("C:/Windows/Fonts"))
    options = parser.parse_args()
    render(options.land, options.fonts, ROOT / "world-edition-newsroom.png")
