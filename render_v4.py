"""Render the three-lead Ver.4 with an atlas strip and fifteen selected briefs."""

import argparse
import json
from pathlib import Path

from PIL import Image

from edition_v3 import LEADS, SECTIONS
from render_v3 import BOLD, COLUMN, INK, LEFT, PAGE, PAPER, PITCH, RED, RIGHT, RULE, SERIF
from render_v3 import Canvas, draw_antalya, draw_kyiv, draw_washington, pixels


SELECTED = (
    ("stocks", "japan", "uk-eu", "taiwan", "chile"),
    ("gaza", "yemen", "sudan", "myanmar", "denmark"),
    ("peru", "flood", "children", "brazil", "skating"),
)

PLACES = (
    ("KYIV / EASTERN POLAND", ("Strikes on Kyiv bridges", "Missiles fall in NATO territory"), "#87372e"),
    ("ANTALYA, TÜRKİYE", ("Mediterranean host city", "UN climate talks run late"), "#1f5446"),
    ("WASHINGTON, U.S.", ("Nov 20 White House remarks", "Shenzhen summit: Nov 19"), "#234866"),
)

ART_NOTES = (
    ("KYIV RIVER CROSSING", "3 bridges hit"),
    ("CLIMATE SUMMIT", "Draft omits fossil fuels"),
    ("WHITE HOUSE", "Nuclear buildup warning"),
)

LEAD_COPY = (
    "Russian strikes hit Kyiv overnight. Missiles also fell in Poland, drawing a NATO rebuke.",
    "Negotiators ran past the deadline. A draft that left out fossil fuels drew criticism.",
    "Trump spoke after U.S., Chinese and Russian leaders pledged nuclear-risk talks in Shenzhen.",
)


def draw_locations(sheet, land_path):
    sheet.rect((LEFT, 487, RIGHT, 600), "#eee2cd")
    sheet.text(42, 497, "WHERE IT HAPPENED", 17, INK, SERIF)

    def project(lon, lat):
        return 42 + (lon + 180) * 0.735, 519 + (84 - lat) * 0.51

    data = json.loads(land_path.read_text(encoding="utf-8"))
    for feature in data["features"]:
        geometry = feature["geometry"]
        shapes = geometry["coordinates"]
        if geometry["type"] == "Polygon":
            shapes = [shapes]
        for exterior, *_ in shapes:
            if max(lat for _, lat in exterior) >= -60:
                points = tuple(value for lon, lat in exterior
                               for value in project(lon, max(lat, -60)))
                sheet.polygon(points, "#9ba99b")

    markers = ((30.52, 50.45, 225, 524), (30.70, 36.90, 225, 560), (-77.04, 38.91, 105, 528))
    poland_x, poland_y = project(22.9, 50.6)
    sheet.oval((poland_x-2, poland_y-2, poland_x+2, poland_y+2), PLACES[0][2])
    for index, ((lon, lat, x, y), (name, lines, color)) in enumerate(
        zip(markers, PLACES, strict=True), start=1
    ):
        px, py = project(lon, lat)
        sheet.line((px, py, x, y), color, 2)
        sheet.oval((px-3, py-3, px+3, py+3), color)
        sheet.oval((x-10, y-10, x+10, y+10), color)
        sheet.text(x, y, str(index), 13, PAPER, anchor="mm")

        left = 319 + (index-1) * 226
        sheet.line((left, 511, left, 583), RULE)
        sheet.oval((left+12, 518, left+36, 542), color)
        sheet.text(left+24, 530, str(index), 14, PAPER, anchor="mm")
        sheet.text(left+43, 523, name, 13, color, limit=178)
        for row, words in enumerate(lines):
            sheet.text(left+13, 550+17*row, words, 14, face=BOLD, limit=207)


def render(land_path, fonts, output):
    sheet = Canvas(PAGE, PAGE, PAPER, fonts)
    sheet.rect((LEFT, 13, RIGHT, 17), INK)
    sheet.text(LEFT, 25, "THE WORLD EDITION", 49, face=SERIF)
    sheet.text(LEFT, 75, "FRIDAY 20 NOVEMBER 2026", 20, RED)
    sheet.text(RIGHT, 42, "WORLD NEWS IN ONE IMAGE", 15, RED, anchor="rt")
    story_count = len(LEADS) + sum(map(len, SELECTED))
    sheet.text(RIGHT, 66, f"{story_count} STORIES", 19, anchor="rt")

    sheet.rect((LEFT, 106, RIGHT, 135), RED)
    sheet.text(LEFT+10, 110, "3 BIG STORIES", 23, PAPER, SERIF)
    scenes = (draw_kyiv, draw_antalya, draw_washington)
    backgrounds = ("#8c7778", "#214b45", "#223b57")
    for index, (story, scene, bg, (scene_label, finding), (_, _, color), summary) in enumerate(
        zip(LEADS, scenes, backgrounds, ART_NOTES, PLACES, LEAD_COPY, strict=True), start=1
    ):
        x = LEFT + (index-1)*PITCH
        art = Canvas(COLUMN, 199, bg, fonts)
        scene(art)
        if story.id == "kyiv":
            art.line((157, 132, 120, 33, 106, 33), "#f6e3b6", 1.5)
            art.oval((154, 129, 160, 135), "#f6e3b6")
            art.rect((10, 22, 107, 43), "#28343b")
            art.text(16, 27, "BRIDGE DAMAGE", 10, PAPER)
        sheet.image.paste(art.image, pixels((x, 145)))
        sheet.rect((x, 344, x+COLUMN-1, 373), color)
        sheet.oval((x+7, 348, x+27, 368), PAPER)
        sheet.text(x+17, 358, str(index), 12, color, anchor="mm")
        note_width = COLUMN - 49 - sheet.width(finding, 13, BOLD)
        sheet.text(x+34, 353, scene_label, 11, PAPER, limit=note_width)
        sheet.text(x+COLUMN-7, 352, finding, 13, PAPER, anchor="rt")
        available = COLUMN - sheet.width(story.source, 12, BOLD) - 8
        sheet.text(x, 382, f"{story.where} / {story.beat}".upper(), 12, RED, limit=available)
        sheet.text(x+COLUMN, 382, story.source, 12, anchor="rt")
        for row, words in enumerate(story.headline.splitlines()):
            sheet.text(x, 398+25*row, words, 22, face=SERIF, limit=COLUMN)
        sheet.paragraph(x, 449, summary, 14, COLUMN, 2, 15)

    draw_locations(sheet, land_path)

    for col, ((name, stories), ids) in enumerate(zip(SECTIONS, SELECTED, strict=True)):
        x = LEFT + col*PITCH
        color = ("#1f5446", "#87372e", "#234866")[col]
        sheet.rect((x, 613, x+COLUMN, 640), color)
        sheet.text(x+9, 619, name, 17, PAPER, SERIF)
        by_id = {story.id: story for story in stories}
        for row, story_id in enumerate(ids):
            story = by_id[story_id]
            y = 650 + 61*row
            available = COLUMN - sheet.width(story.source, 11, BOLD) - 6
            sheet.text(x, y, f"{story.where} / {story.beat}".upper(), 11, color, limit=available)
            sheet.text(x+COLUMN, y, story.source, 11, anchor="rt")
            sheet.text(x, y+14, story.headline, 17, limit=COLUMN)
            sheet.paragraph(x, y+32, story.detail, 13, COLUMN, 2, 13)
            if row < len(ids)-1:
                sheet.line((x, y+59, x+COLUMN, y+59), RULE)

    sheet.rect((LEFT, 958, RIGHT, 1010), "#e8dcc6")
    sheet.line((LEFT, 958, RIGHT, 958), INK, 2)
    sheet.text(41, 968, "DATE CHECK", 16, RED, SERIF)
    sheet.text(167, 968, "Nov 20 local events or new developments. Earlier standalone stories excluded.", 14)
    sheet.text(167, 988, "Peru quake: Nov 20 local / Nov 21 UTC. Nov 19 Shenzhen summit is context for Nov 20 remarks.", 13)
    sheet.image.resize((PAGE, PAGE), Image.Resampling.LANCZOS).save(output, optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("land", type=Path)
    parser.add_argument("--fonts", type=Path, default=Path("C:/Windows/Fonts"))
    options = parser.parse_args()
    render(options.land, options.fonts, Path(__file__).with_name("world-edition-v4.png"))
