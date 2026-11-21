"""Compose the Ver.3 newspaper and draw its original editorial illustrations."""

import argparse
from functools import cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from edition_v3 import FIGURE_ORDER, LEADS, SECTIONS


PAGE = 1024
SCALE = 2
PAPER = "#f7efe0"
INK = "#172a37"
RED = "#962f29"
RULE = "#c8b79d"
SERIF = "georgiab.ttf"
BOLD = "arialbd.ttf"
REGULAR = "arial.ttf"
LEFT = 30
RIGHT = 994
COLUMN = 312
PITCH = 326


def pixels(values):
    return tuple(round(value * SCALE) for value in values)


class Canvas:
    def __init__(self, width, height, color, fonts):
        self.image = Image.new("RGB", pixels((width, height)), color)
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = fonts

    @cache
    def font(self, face, size):
        return ImageFont.truetype(str(self.fonts / face), size * SCALE)

    def width(self, words, size, face):
        return self.font(face, size).getlength(words) / SCALE

    def text(self, x, y, words, size, color=INK, face=BOLD, limit=None, anchor="lt"):
        if limit is not None and self.width(words, size, face) > limit:
            raise ValueError(f"Text exceeds {limit}px: {words}")
        self.draw.text(pixels((x, y)), words, font=self.font(face, size), fill=color, anchor=anchor)

    def paragraph(self, x, y, words, size, width, max_lines, leading):
        lines = [""]
        for word in words.split():
            joined = f"{lines[-1]} {word}".strip()
            if self.width(joined, size, REGULAR) <= width:
                lines[-1] = joined
            else:
                lines.append(word)
        if len(lines) > max_lines:
            raise ValueError(f"Paragraph exceeds {max_lines} lines: {words}")
        if len(lines) == 2 and self.width(lines[1], size, REGULAR) < width / 3:
            # Rebalance short closing lines so a single word does not hang below the story.
            tokens = lines[0].split()
            while len(tokens) > 1:
                next_line = f"{tokens[-1]} {lines[1]}"
                first_line = " ".join(tokens[:-1])
                if self.width(next_line, size, REGULAR) > self.width(first_line, size, REGULAR):
                    break
                tokens.pop()
                lines = [first_line, next_line]
        for index, line in enumerate(lines):
            self.text(x, y + index * leading, line, size, face=REGULAR, limit=width)

    def rect(self, bounds, color):
        self.draw.rectangle(pixels(bounds), fill=color)

    def oval(self, bounds, color):
        self.draw.ellipse(pixels(bounds), fill=color)

    def line(self, points, color, width=1):
        self.draw.line(pixels(points), fill=color, width=round(width * SCALE), joint="curve")

    def polygon(self, points, color):
        self.draw.polygon(pixels(points), fill=color)


def draw_kyiv(art):
    art.rect((0, 91, 312, 199), "#4f6871")
    art.oval((208, 17, 273, 82), "#eaab7d")
    for y in (42, 52, 63, 75):
        art.line((12, y, 116 + y, y), "#b58d81")
    # Riverbank skyline and a damaged deck, with the crossing still in place.
    for x, top, span in ((7, 61, 24), (31, 68, 15), (47, 48, 29),
                         (78, 63, 14), (94, 58, 34), (135, 67, 28),
                         (172, 58, 22), (207, 70, 35), (253, 64, 19), (277, 55, 23)):
        art.rect((x, top, x + span, 103), "#40505c")
        for window in range(x + 5, x + span - 4, 7):
            art.rect((window, top + 8, window + 2, top + 12), "#d4a88c")
    art.polygon((0, 103, 95, 109, 141, 129, 0, 149), "#354d56")
    art.polygon((312, 96, 251, 106, 226, 118, 312, 139), "#354d56")
    for y, x, end in ((123, 6, 99), (136, 169, 305), (154, 22, 146), (169, 156, 290),
                      (180, 14, 123), (188, 206, 300)):
        art.line((x, y, end, y), "#8ea3a1", 1)
    art.polygon((0, 163, 155, 135, 171, 136, 312, 105, 312, 117, 0, 181), "#28343b")
    art.line((0, 159, 152, 131), "#e5bc8c", 4)
    art.line((182, 130, 312, 102), "#e5bc8c", 4)
    for x, y, length in ((37, 155, 43), (104, 143, 45), (212, 131, 46), (271, 119, 37)):
        art.polygon((x, y, x + 13, y - 2, x + 13, y + length - 3, x, y + length), "#263943")
    art.line((0, 174, 312, 112), "#c58c68", 2)
    art.line((149, 132, 155, 135, 161, 130, 165, 133, 174, 131, 178, 127, 182, 130), "#efad7b", 3)
    for x in (17, 43, 69, 95, 121, 197, 222, 247, 272, 297):
        top = 162 - x * 0.19
        art.line((x, top - 11, x, top), "#eee2c3", 1)
    art.line((0, 151, 150, 123), "#e1d8bc")
    art.line((187, 120, 312, 94), "#e1d8bc")


def draw_antalya(art):
    art.rect((0, 0, 312, 112), "#163e3a")
    art.rect((23, 21, 288, 133), "#24554a")
    for y in (13, 23, 95, 103):
        art.line((0, y, 312, y), "#366a5c")
    art.text(156, 34, "COP31", 44, "#f5e3ad", SERIF, anchor="mt")
    art.text(156, 82, "ANTALYA", 13, "#e2e0b6", anchor="mt")
    art.rect((0, 110, 312, 136), "#9a7d5c")
    art.rect((0, 134, 312, 199), "#293d39")
    for x in (39, 79, 233, 272):
        art.rect((x - 12, 103, x + 12, 124), "#1b3735")
        art.oval((x - 6, 92, x + 6, 104), "#c59678")
        art.line((x + 10, 114, x + 15, 108), "#f3dcae", 1)
    art.polygon((140, 102, 171, 102, 164, 135, 147, 135), "#b99665")
    art.oval((149, 87, 162, 101), "#e1ad86")
    art.line((170, 104, 166, 95, 160, 93), "#f3dcae", 2)
    # A silent protest in the foreground. The signs describe the issue.
    for x, y, words in ((24, 128, "FOSSIL FUELS"), (226, 136, "CLIMATE ACTION")):
        art.rect((x, y, x + 66, y + 26), "#ede0b4")
        art.text(x + 33, y + 9, words, 7, "#24493f", anchor="mt")
        art.line((x + 32, y + 26, x + 34, y + 65), "#bfa586", 2)
    for x, top, c in ((11, 157, "#486959"), (53, 167, "#5d7e69"), (91, 151, "#3f6f62"),
                      (130, 164, "#7b745f"), (169, 152, "#426e66"), (208, 169, "#66765e"),
                      (244, 160, "#49735f"), (288, 166, "#526b5b")):
        art.oval((x-9, top, x+9, top+19), "#b7886f")
        art.oval((x-21, top+15, x+21, top+60), c)


def draw_washington(art):
    art.rect((0, 0, 312, 199), "#223b57")
    for x in (13, 22, 36, 48, 262, 274, 291, 302):
        art.line((x, 0, x, 199), "#355471", 2)
    art.oval((85, 17, 225, 107), "#42617a")
    art.polygon((101, 68, 155, 41, 208, 68), "#b8c7c7")
    art.rect((101, 68, 209, 95), "#ced6d0")
    for x in (119, 137, 155, 173, 191):
        art.rect((x, 71, x+3, 94), "#5b7687")
    for x, y, field in ((35, 53, "#b65249"), (233, 50, "#b95346")):
        art.line((x, y, x, 169), "#dfc49c", 2)
        art.rect((x, y, x+42, y+34), field)
    for y in (60, 69, 78):
        art.rect((35, y, 77, y+3), "#e7d6b6")
    art.rect((35, 53, 54, 70), "#344b6c")
    for x, y in ((41,57), (49,61), (42,66)):
        art.oval((x-1, y-1, x+1, y+1), "#f2e3c2")
    art.polygon((246,53,248,58,253,58,249,61,251,66,246,63,241,66,243,61,239,58,244,58), "#f1ca77")
    art.polygon((109, 150, 121, 125, 143, 118, 169, 118, 191, 126, 204, 152), "#192a39")
    art.oval((139, 79, 173, 124), "#d2a081")
    art.polygon((139, 98, 138, 85, 148, 77, 174, 80, 174, 89, 154, 87), "#e1bc83")
    art.polygon((145, 119, 156, 141, 167, 119), "#eee4ce")
    art.polygon((154, 127, 158, 127, 162, 143, 151, 143), "#a64843")
    for x, end in ((139, 130), (176, 184)):
        art.line((x, 151, end, 123, end-6, 120), "#131e29", 3)
    art.polygon((91, 145, 221, 145, 205, 202, 107, 202), "#684139")
    art.rect((87, 145, 225, 153), "#dfbb80")
    art.oval((143, 162, 169, 188), "#d6b37c")
    art.oval((148, 167, 164, 183), "#493631")


def render(fonts, output, *, lead_scenes=None):
    sheet = Canvas(PAGE, PAGE, PAPER, fonts)
    stories = (*LEADS, *(story for _, section in SECTIONS for story in section))
    figures = {story.id: story for story in stories}
    sheet.rect((LEFT, 13, RIGHT, 17), INK)
    sheet.text(LEFT, 25, "THE WORLD EDITION", 49, face=SERIF, limit=710)
    sheet.text(RIGHT, 36, "WORLD NEWS IN ONE IMAGE", 15, RED, anchor="rt")
    sheet.text(RIGHT, 56, f"{len(stories)} STORIES", 21, anchor="rt")
    sheet.text(LEFT, 75, "FRIDAY 20 NOVEMBER 2026", 20, RED)

    art_top, art_height = 98, 199
    if lead_scenes is None:
        lead_scenes = (draw_kyiv, draw_antalya, draw_washington)
    else:
        sheet.rect((LEFT, 98, RIGHT, 122), RED)
        sheet.text(LEFT+9, 101, "3 BIG STORIES", 20, PAPER, SERIF)
        art_top, art_height = 128, 169

    for index, (story, bg, scene) in enumerate(zip(
        LEADS, ("#8c7778", "#214b45", "#223b57"), lead_scenes, strict=True,
    )):
        x = LEFT + PITCH * index
        art = Canvas(COLUMN, art_height, bg, fonts)
        scene(art)
        sheet.image.paste(art.image, pixels((x, art_top)))
        available = COLUMN - sheet.width(story.source, 13, BOLD) - 8
        sheet.text(x, 304, f"{story.where} / {story.beat}".upper(), 13, RED, limit=available)
        sheet.text(x + COLUMN, 304, story.source, 13, anchor="rt")
        for row, line in enumerate(story.headline.splitlines()):
            sheet.text(x, 323 + 27*row, line, 24, face=SERIF, limit=COLUMN)
        sheet.paragraph(x, 380, story.detail, 15, COLUMN, 3, 16)

    sheet.rect((LEFT, 429, RIGHT, 493), "#e8ddc7")
    sheet.line((LEFT, 429, RIGHT, 429), RED, 2)
    figure_width = (RIGHT - LEFT)/len(FIGURE_ORDER)
    for index, story_id in enumerate(FIGURE_ORDER):
        story = figures[story_id]
        x = LEFT + index*figure_width
        center = x + figure_width/2
        if index:
            sheet.line((x, 441, x, 482), RULE)
        sheet.text(center, 437, story.figure, 34, RED, face=SERIF, anchor="mt")
        sheet.text(center, 475, story.figure_label, 13, anchor="mt")

    for index, (section_name, section) in enumerate(SECTIONS):
        x = LEFT + PITCH*index
        section_color = ("#235048", "#842f2c", "#233e51")[index]
        sheet.rect((x, 506, x+COLUMN, 531), section_color)
        sheet.text(x+8, 511, section_name, 17, PAPER, face=SERIF)
        for row, story in enumerate(section):
            y = 539+51*row
            available = COLUMN - sheet.width(story.source, 11, BOLD) - 7
            sheet.text(x, y, f"{story.where} / {story.beat}".upper(), 11, RED, limit=available)
            sheet.text(x+COLUMN, y, story.source, 11, anchor="rt")
            sheet.text(x, y+11, story.headline, 16, limit=COLUMN)
            sheet.paragraph(x, y+27, story.detail, 12, COLUMN, 2, 12)
            if row < len(section)-1:
                sheet.line((x, y+49, x+COLUMN, y+49), RULE)

    sheet.rect((LEFT, 951, RIGHT, 1010), "#e8ddc7")
    sheet.line((LEFT, 951, RIGHT, 951), INK, 2)
    sheet.text(41, 963, "DATE CHECK", 17, RED)
    sheet.text(162, 962, "Nov 20 local events or first reports. Earlier events appear only with a new development.",
               15, limit=820)
    sheet.text(162, 980, "Peru quake: Nov 20 PET / Nov 21 UTC. Shenzhen, Nov 19, is background to Nov 20 remarks.",
               14, face=REGULAR, limit=820)
    sheet.text(162, 997, "Excluded: Anthropic’s Nov 19 IPO debut. Source credits appear beside each story.",
               12, face=REGULAR, limit=820)
    sheet.image.resize((PAGE, PAGE), Image.Resampling.LANCZOS).save(output, optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fonts", type=Path, default=Path("C:/Windows/Fonts"))
    options = parser.parse_args()
    render(options.fonts, Path(__file__).with_name("world-edition-v3.png"))
