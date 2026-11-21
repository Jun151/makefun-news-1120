"""Draw three editorial scenes and compose them on the Ver.3 newsprint layout."""

import argparse
from math import cos, pi, sin
from pathlib import Path

from render_v3 import PAPER, SERIF, pixels, render


NIGHT = "#172f3c"
HONEY = "#f0bc7d"


def bridge_scene(art):
    """An editorial river crossing with damage and a closed lane."""
    art.rect((0, 0, 312, 169), "#b9bcb1")
    art.rect((0, 82, 312, 169), "#4d7883")
    for left, top, width in ((0, 63, 25), (26, 51, 20), (47, 57, 13),
                             (61, 38, 24), (86, 57, 16), (103, 65, 29),
                             (137, 54, 23), (265, 54, 27), (293, 62, 19)):
        art.rect((left, top, left+width, 88), "#536b71")
        if width >= 20:
            art.rect((left+5, top+10, left+8, top+14), "#d7c2a1")
            art.rect((left+12, top+10, left+15, top+14), "#d7c2a1")
    art.rect((0, 87, 312, 91), "#3d5962")
    for y, x, end in ((111, 35, 85), (132, 11, 67), (151, 157, 239), (158, 235, 302)):
        art.line((x, y, end, y), "#8aacad", 1.5)
    # The silhouette stays continuous because the reporting establishes damage,
    # not the collapse of a span. The localized break in the edge is editorial.
    for x, y in ((44, 119), (114, 108), (230, 89), (288, 79)):
        art.polygon((x,y,x+17,y-3,x+17,y+35,x,y+39), "#304b57")
    art.polygon((0,115, 133,95, 153,100, 171,94, 182,86, 312,64, 312,81, 0,135), NIGHT)
    art.line((0,114, 132,94), PAPER, 4)
    art.line((184,85, 312,63), PAPER, 4)
    art.line((132,94, 145,97, 151,101, 164,97, 171,94, 178,89, 184,85), HONEY, 6)
    for x, y in ((16, 110), (40, 106), (64, 103), (88, 99), (112, 96),
                 (207, 81), (231, 77), (255, 73), (279, 69)):
        art.line((x,y,x,y-13), PAPER, 2)
    art.line((0,101, 123,82), PAPER, 2)
    art.line((196,70, 312,50), PAPER, 2)
    # A single striped road barricade cues the reported traffic disruption.
    art.line((134,80,134,95,176,90,176,73), "#c27f4d", 2)
    art.polygon((129,75,181,68,181,79,129,86), PAPER)
    for x, y in ((137, 74), (149, 72.5), (161, 71), (173, 69.5)):
        art.line((x,y,x-6,y+10), "#a44236", 4)


def climate_scene(art):
    """Two delegates work over a disputed draft at the climate conference."""
    art.rect((0, 0, 312, 169), "#1d493e")
    art.rect((0, 0, 312, 65), "#29584a")
    art.text(149, 11, "COP31", 37, PAPER, SERIF, anchor="mt")
    # Fossil fuels are the subject of dispute, represented by a barrel on the backdrop.
    art.oval((252, 11, 288, 23), "#e1b57d")
    art.rect((252, 18, 288, 47), "#c49362")
    art.oval((252, 42, 288, 52), "#c49362")
    art.line((252, 23, 288, 23), "#ecc192", 2)
    art.line((252, 45, 288, 45), "#986a49", 2)
    art.polygon((270,25, 264,34, 276,34), "#27483d")
    art.oval((264,31,276,41), "#27483d")
    art.polygon((0,169, 0,127, 25,103, 64,88, 85,92, 111,124, 142,143, 132,169), "#223844")
    art.polygon((312,169, 312,123, 288,101, 256,88, 231,95, 204,131, 175,141, 182,169), "#385349")
    # Turned faces and open gestures direct attention to one shared document.
    art.oval((47,48,87,95), "#bf865e")
    art.polygon((45,76, 42,61, 49,47, 72,44, 88,54, 83,63, 62,60, 57,80), "#342f2c")
    art.polygon((78,66, 91,74, 81,80, 81,91, 69,96, 59,87), "#bf865e")
    art.oval((222,47,264,95), "#dfb08b")
    art.polygon((223,73, 216,64, 222,47, 244,41, 263,49, 270,62, 267,81, 257,88, 251,65), "#523b33")
    art.polygon((226,65, 215,76, 224,79, 224,92, 236,97, 245,87), "#dfb08b")
    art.polygon((60, 170, 118, 126, 197, 126, 256, 170), "#805f49")
    art.polygon((118,161, 132,128, 175,128, 194,161), "#f5e6c2")
    art.line((139,138,174,138), "#9a8c70", 2)
    art.line((135,145,178,145), "#ac4d39", 2)
    art.line((137,152,169,152), "#9a8c70", 2)
    art.polygon((109,126, 120,132, 129,133, 141,142, 127,143, 111,138, 103,131), "#bf865e")
    art.polygon((203,120, 193,120, 184,114, 179,117, 184,126, 199,132, 207,128), "#dfb08b")


def star(art, x, y, radius):
    points = []
    for index in range(10):
        angle = -pi / 2 + index * pi / 5
        length = radius if index % 2 == 0 else radius * .40
        points.extend((x + cos(angle)*length, y + sin(angle)*length))
    art.polygon(points, "#f5ce68")


def nuclear_scene(art):
    """The three countries behind a single warning at a press lectern."""
    art.rect((0, 0, 312, 169), "#223e56")
    for stripe in range(13):
        top = 14 + stripe * 42 / 13
        bottom = 14 + (stripe+1) * 42 / 13
        art.rect((19, top, 98, bottom), "#b44d45" if stripe % 2 == 0 else "#efdfca")
    art.rect((19, 14, 50, 37), "#334e7a")
    for y in (19, 25, 31):
        for x in (25, 33, 41):
            art.oval((x-1,y-1,x+1,y+1), PAPER)
    art.rect((116,14,195,55), "#af433a")
    star(art, 134, 29, 9)
    for x, y in ((147,20), (152,25), (152,31), (147,36)):
        star(art, x, y, 2.2)
    for index, color in enumerate(("#efdfca", "#4d6caa", "#b44d45")):
        art.rect((213,14+index*14,292,27+index*14), color)
    # One oversize warning symbol supplies the focus. The microphone cues the briefing.
    art.polygon((75,90, 237,90, 222,169, 90,169), "#284354")
    art.rect((67,87,245,99), "#5d7986")
    art.line((185,87, 177,73, 166,69), "#101f2b", 5)
    art.oval((158,66,171,73), "#101f2b")
    art.polygon((156,90,198,158,114,158), HONEY)
    for start in (0, 120, 240):
        art.draw.pieslice(pixels((137,119,175,157)), start+8, start+64, fill=NIGHT)
    art.oval((149,131,163,145), HONEY)
    art.oval((152,134,160,142), NIGHT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fonts", type=Path, default=Path("C:/Windows/Fonts"))
    options = parser.parse_args()
    render(options.fonts, Path(__file__).with_name("world-edition-v5.png"),
           lead_scenes=(bridge_scene, climate_scene, nuclear_scene))
