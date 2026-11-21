"""Draw three editorial scenes and compose them on the Ver.3 newsprint layout."""

import argparse
from math import cos, pi, sin
from pathlib import Path

from render_v3 import PAPER, SERIF, pixels, render


NIGHT = "#172f3c"
HONEY = "#f0bc7d"


def bridge_scene(art):
    """An editorial river crossing with damage and a closed lane."""
    art.rect((0, 0, 312, 169), "#aeb1a7")
    art.rect((0, 64, 312, 88), "#c5b49e")
    art.rect((0, 82, 312, 169), "#416d7c")
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
    art.polygon((0,115, 133,95, 153,103, 171,97, 182,86, 312,64, 312,81, 0,139), NIGHT)
    art.line((0,135,312,79), "#8a9a98", 2.5)
    art.line((0,114, 132,94), PAPER, 4)
    art.line((184,85, 312,63), PAPER, 4)
    art.polygon((127,94, 139,94, 153,101, 169,95, 183,84, 186,93,
                 173,102, 171,112, 158,107, 148,117, 143,103, 129,102), "#d68d66")
    art.line((145,101, 148,114, 156,107, 164,109, 172,99), "#573a31", 3)
    for x, y in ((16, 110), (40, 106), (64, 103), (88, 99), (112, 96),
                 (207, 81), (231, 77), (255, 73), (279, 69)):
        art.line((x,y,x,y-13), PAPER, 2)
    art.line((0,101, 122,82, 132,88), PAPER, 2.5)
    art.line((177,79, 196,70, 312,50), PAPER, 2.5)
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
    art.polygon((104,163, 126,122, 183,122, 207,163), "#f5e6c2")
    art.text(156, 139, "FOSSIL FUELS", 11, "#543f32", anchor="mm")
    art.line((117,139,195,139), "#aa4839", 2.5)
    art.line((130,151,181,151), "#9a8c70", 2)
    art.polygon((108,124, 117,129, 132,129, 141,133, 133,135, 119,137, 104,132), "#bf865e")
    art.polygon((203,119, 192,119, 185,112, 180,115, 186,125, 198,130, 207,127), "#dfb08b")
    art.line((76,72,81,73), "#4a3432", 1.5)
    art.line((225,73,229,72), "#4a3432", 1.5)


def star(art, x, y, radius):
    points = []
    for index in range(10):
        angle = -pi / 2 + index * pi / 5
        length = radius if index % 2 == 0 else radius * .40
        points.extend((x + cos(angle)*length, y + sin(angle)*length))
    art.polygon(points, "#f5ce68")


def nuclear_scene(art):
    """An editorial portrait of Trump during the White House briefing."""
    art.rect((0, 0, 312, 169), "#223e56")
    art.rect((77, 0, 239, 169), "#34556e")
    art.line((78, 0, 78, 169), "#54738a", 2)
    art.line((239, 0, 239, 169), "#54738a", 2)
    # Trilateral context sits beside the portrait, outside the briefing scene.
    for stripe in range(13):
        top = 36 + stripe * 24 / 13
        bottom = 36 + (stripe+1) * 24 / 13
        art.rect((17, top, 62, bottom), "#b44d45" if stripe % 2 == 0 else "#efdfca")
    art.rect((17, 36, 34, 49), "#334e7a")
    for y in (39, 43, 47):
        for x in (20, 25, 30):
            art.oval((x-.65,y-.65,x+.65,y+.65), PAPER)
    art.rect((17,68,62,92), "#af433a")
    star(art, 27, 76, 5)
    for x, y in ((33,70), (36,73), (36,77), (34,80)):
        star(art, x, y, 1.1)
    for index, color in enumerate(("#efdfca", "#4d6caa", "#b44d45")):
        art.rect((17,100+index*8,62,108+index*8), color)

    # Frontal, waist-up speech composition. The hair silhouette, face and red tie
    # carry the likeness even when the panel is reduced to thumbnail size.
    art.polygon((68,169, 76,144, 89,128, 123,114, 150,107, 180,108,
                 215,121, 238,134, 249,169), "#162737")
    art.polygon((91,169, 101,133, 136,116, 149,127, 145,169), "#24394e")
    art.polygon((232,169, 220,136, 185,115, 174,128, 181,169), "#263a50")
    art.polygon((140,99, 139,121, 160,135, 182,118, 179,98), "#bd7856")
    art.polygon((136,114, 160,122, 184,112, 176,169, 146,169), PAPER)
    art.polygon((155,123, 166,123, 171,132, 166,138, 173,169, 151,169, 155,137, 151,132), "#a73938")
    art.polygon((135,114, 154,122, 148,137, 135,126), "#fff1d6")
    art.polygon((183,113, 168,122, 174,137, 185,125), "#fff1d6")

    art.oval((119,60,134,83), "#c48761")
    art.oval((188,59,202,81), "#bd7959")
    art.polygon((126,45, 135,29, 158,26, 184,32, 193,50, 195,74, 190,93,
                 181,105, 165,112, 151,109, 138,101, 129,84, 125,65), "#e1a580")
    art.polygon((180,48, 193,51, 195,74, 190,93, 181,105, 165,112,
                 155,109, 172,101, 183,90, 185,69), "#be7c5e")
    art.polygon((121,64, 119,45, 125,33, 132,28, 126,27, 142,18, 155,16,
                 173,19, 188,15, 200,20, 194,29, 199,35, 192,51, 187,56,
                 182,43, 168,39, 155,42, 139,37, 132,49, 130,66, 126,70), "#e0bc77")
    art.polygon((129,31, 145,21, 161,20, 175,23, 191,20, 184,27, 171,31,
                 151,30, 140,35), "#f6d597")
    art.line((137,60,145,58,153,60), "#865741", 2.5)
    art.line((172,60,180,58,186,60), "#865741", 2.5)
    art.line((139,66,146,65,151,67), "#593d38", 2)
    art.line((172,66,178,65,184,67), "#593d38", 2)
    art.line((163,63,159,78,165,79), "#a3634e", 2)
    art.oval((149,88,176,97), "#6c413d")
    art.line((154,89,171,89), "#f1d7b8", 2)

    art.line((207,166,202,142,188,123), "#0b202d", 4)
    art.oval((182,118,194,126), "#0b202d")
    art.rect((91,163,234,169), "#527184")
    art.polygon((273,87,297,128,249,128), HONEY)
    for start in (0, 120, 240):
        art.draw.pieslice(pixels((263,105,283,125)), start+8, start+64, fill=NIGHT)
    art.oval((269,111,277,119), HONEY)
    art.oval((271,113,275,117), NIGHT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fonts", type=Path, default=Path("C:/Windows/Fonts"))
    options = parser.parse_args()
    render(options.fonts, Path(__file__).with_name("world-edition-v5.png"),
           lead_scenes=(bridge_scene, climate_scene, nuclear_scene))
