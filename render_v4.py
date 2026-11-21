"""Render Ver.4 with three explanatory panels and an atlas of all 18 stories."""

import argparse
import json
from itertools import combinations
from math import hypot
from pathlib import Path

from PIL import Image

from edition_v3 import LEADS, SECTIONS
from render_v3 import BOLD, COLUMN, INK, LEFT, PAGE, PAPER, PITCH, RED, RIGHT, RULE, SERIF
from render_v3 import Canvas, pixels
from v4_illustrations import climate_talks, kyiv_bridges, nuclear_timeline


SELECTED = (
    ("stocks", "japan", "uk-eu", "taiwan", "chile"),
    ("gaza", "yemen", "sudan", "myanmar", "denmark"),
    ("peru", "flood", "children", "brazil", "skating"),
)

ECONOMY = "#215448"
POLITICS = "#785243"
BRIEFS = "#235071"
LAND_DATA = Path(__file__).with_name("assets") / "ne_110m_land.geojson"

ART_NOTES = (
    ("KYIV RIVER CROSSINGS", "3 bridges hit"),
    ("CLIMATE SUMMIT", "Deadline passes"),
    ("U.S. / CHINA / RUSSIA", "Two days of diplomacy"),
)

LEAD_COPY = (
    "Russian strikes hit Kyiv overnight. Missiles also fell in Poland, drawing a NATO rebuke.",
    "Negotiators ran past the deadline. A draft that left out fossil fuels drew criticism.",
    "Trump spoke after U.S., Chinese and Russian leaders pledged nuclear-risk talks in Shenzhen.",
)

# Verified event, venue or representative location, longitude/latitude, and label center.
# Country-wide stories use representative points as documented in README.md.
MAP_POINTS = {
    "kyiv": ("Kyiv", 30.515, 50.435, 589, 525),
    "cop31": ("Antalya", 30.698, 36.892, 609, 551),
    "nuclear": ("Washington, D.C.", -77.011, 38.901, 310, 525),
    "stocks": ("New York City", -73.996, 40.722, 388, 527),
    "japan": ("Tokyo", 139.749, 35.687, 801, 545),
    "uk-eu": ("Brussels", 4.331, 50.835, 475, 530),
    "taiwan": ("Taipei", 121.568, 25.036, 766, 581),
    "chile": ("Santiago", -70.651, -33.440, 336, 620),
    "gaza": ("Deir al-Balah", 34.35, 31.42, 618, 576),
    "yemen": ("Al Hudaydah", 42.951, 14.800, 624, 603),
    "sudan": ("Ed Damazin", 34.350, 11.770, 530, 582),
    "myanmar": ("Naypyitaw", 96.117, 19.769, 687, 592),
    "denmark": ("Copenhagen", 12.565, 55.671, 510, 518),
    "peru": ("Junín epicentral area", -76.19, -10.97, 309, 582),
    "flood": ("Sanford, central St. Johns River", -81.280, 28.790, 298, 552),
    "children": ("Pretoria", 28.227, -25.705, 542, 618),
    "brazil": ("Brasília", -47.918, -15.781, 423, 614),
    "skating": ("Helsinki", 24.932, 60.164, 550, 517),
}


def badge(sheet, number, x, y, color, radius, size):
    sheet.oval((x-radius, y-radius, x+radius, y+radius), color)
    sheet.text(x, y, f"{number:02}", size, PAPER, anchor="mm")


def draw_locations(sheet, land_path, stories):
    sheet.rect((LEFT, 482, RIGHT, 635), "#ede2cd")
    sheet.text(42, 491, "WHERE IT HAPPENED", 19, INK, SERIF)
    for x, label, color in (
        (426, "01–03  TOP STORIES", RED),
        (558, "04–08  ECONOMY", ECONOMY),
        (674, "09–13  POLITICS & CONFLICT", POLITICS),
        (842, "14–18  WORLD BRIEFS", BRIEFS),
    ):
        sheet.oval((x, 495, x+7, 502), color)
        sheet.text(x+12, 493, label, 10, color)

    def atlas_x(x):
        return 512 + (x - 512) * 1.12

    def project(lon, lat):
        return atlas_x(153 + (lon + 180) * 1.91), 517 + (80 - lat) * 0.79

    data = json.loads(land_path.read_text(encoding="utf-8"))
    for feature in data["features"]:
        geometry = feature["geometry"]
        shapes = geometry["coordinates"]
        if geometry["type"] == "Polygon":
            shapes = [shapes]
        for exterior, *_ in shapes:
            if max(lat for _, lat in exterior) >= -60:
                points = tuple(value for lon, lat in exterior
                               for value in project(lon, min(80, max(lat, -58))))
                sheet.polygon(points, "#acb3a2")

    markers = []
    for number, (story, color) in enumerate(stories, start=1):
        _, lon, lat, x, y = MAP_POINTS[story.id]
        x = atlas_x(x)
        radius = 12 if number <= 3 else 10
        if not (LEFT+radius <= x <= RIGHT-radius and 505+radius <= y <= 635-radius):
            raise ValueError(f"Map label outside its area: {story.id}")
        markers.append((number, color, x, y, radius))
        px, py = project(lon, lat)
        sheet.line((px, py, x, y), PAPER, 3)
        sheet.line((px, py, x, y), color, 1.25)
        sheet.oval((px-2, py-2, px+2, py+2), color)
    for first, second in combinations(markers, 2):
        if hypot(first[2]-second[2], first[3]-second[3]) < first[4]+second[4]+2:
            raise ValueError(f"Overlapping map labels: {first[0]} and {second[0]}")
    for number, color, x, y, radius in markers:
        badge(sheet, number, x, y, color, radius, 12 if number <= 3 else 11)


def render(land_path, fonts, output):
    sheet = Canvas(PAGE, PAGE, PAPER, fonts)
    sheet.rect((LEFT, 13, RIGHT, 17), INK)
    sheet.text(LEFT, 25, "THE WORLD EDITION", 49, face=SERIF)
    sheet.text(LEFT, 75, "FRIDAY 20 NOVEMBER 2026", 20, RED)
    sheet.text(RIGHT, 42, "WORLD NEWS IN ONE IMAGE", 15, RED, anchor="rt")
    sections = []
    for (name, stories), ids, color in zip(SECTIONS, SELECTED,
                                            (ECONOMY, POLITICS, BRIEFS), strict=True):
        by_id = {story.id: story for story in stories}
        sections.append((name, tuple(by_id[story_id] for story_id in ids), color))
    mapped_stories = [(story, RED) for story in LEADS]
    mapped_stories.extend((story, color) for _, stories, color in sections for story in stories)
    if len(mapped_stories) != len(MAP_POINTS) or {s.id for s, _ in mapped_stories} != MAP_POINTS.keys():
        raise ValueError("Every article must have exactly one map point")
    sheet.text(RIGHT, 66, f"{len(mapped_stories)} STORIES", 19, anchor="rt")

    sheet.rect((LEFT, 106, RIGHT, 135), RED)
    sheet.text(LEFT+10, 110, "3 BIG STORIES", 23, PAPER, SERIF)
    scenes = (kyiv_bridges, climate_talks, nuclear_timeline)
    for index, (story, scene, (scene_label, finding), summary) in enumerate(
        zip(LEADS, scenes, ART_NOTES, LEAD_COPY, strict=True), start=1
    ):
        x = LEFT + (index-1)*PITCH
        art = Canvas(COLUMN, 199, PAPER, fonts)
        scene(art)
        sheet.image.paste(art.image, pixels((x, 145)))
        sheet.rect((x, 344, x+COLUMN-1, 373), RED)
        sheet.oval((x+6, 347, x+28, 369), PAPER)
        sheet.text(x+17, 358, f"{index:02}", 11, RED, anchor="mm")
        note_width = COLUMN - 49 - sheet.width(finding, 13, BOLD)
        sheet.text(x+34, 353, scene_label, 11, PAPER, limit=note_width)
        sheet.text(x+COLUMN-7, 352, finding, 13, PAPER, anchor="rt")
        available = COLUMN - sheet.width(story.source, 12, BOLD) - 8
        sheet.text(x, 382, f"{story.where} / {story.beat}".upper(), 12, RED, limit=available)
        sheet.text(x+COLUMN, 382, story.source, 12, anchor="rt")
        for row, words in enumerate(story.headline.splitlines()):
            sheet.text(x, 398+25*row, words, 22, face=SERIF, limit=COLUMN)
        sheet.paragraph(x, 449, summary, 14, COLUMN, 2, 15)

    draw_locations(sheet, land_path, mapped_stories)

    for col, (name, stories, color) in enumerate(sections):
        x = LEFT + col*PITCH
        sheet.rect((x, 642, x+COLUMN, 666), color)
        sheet.text(x+9, 647, name, 17, PAPER, SERIF)
        for row, story in enumerate(stories):
            number = len(LEADS) + sum(len(entries) for _, entries, _ in sections[:col]) + row + 1
            y = 675 + 56*row
            sheet.rect((x, y-1, x+20, y+11), color)
            sheet.text(x+10, y+5, f"{number:02}", 9, PAPER, anchor="mm")
            available = COLUMN - sheet.width(story.source, 11, BOLD) - 31
            sheet.text(x+25, y, f"{story.where} / {story.beat}".upper(), 11, color, limit=available)
            sheet.text(x+COLUMN, y, story.source, 11, anchor="rt")
            sheet.text(x, y+14, story.headline, 17, limit=COLUMN)
            sheet.paragraph(x, y+30, story.detail, 13, COLUMN, 2, 12)
            if row < len(stories)-1:
                sheet.line((x, y+53, x+COLUMN, y+53), RULE)

    sheet.rect((LEFT, 958, RIGHT, 1010), "#e8dcc6")
    sheet.line((LEFT, 958, RIGHT, 958), INK, 2)
    sheet.text(41, 968, "DATE CHECK", 16, RED, SERIF)
    sheet.text(167, 968, "Nov 20 local events or new developments. Earlier standalone stories excluded.", 14)
    sheet.text(167, 988, "Peru quake: Nov 20 local / Nov 21 UTC. Nov 19 Shenzhen summit is context for Nov 20 remarks.", 13)
    sheet.image.resize((PAGE, PAGE), Image.Resampling.LANCZOS).save(output, optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("land", type=Path, nargs="?", default=LAND_DATA)
    parser.add_argument("--fonts", type=Path, default=Path("C:/Windows/Fonts"))
    options = parser.parse_args()
    render(options.land, options.fonts, Path(__file__).with_name("world-edition-v4.png"))
