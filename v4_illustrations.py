"""Original explanatory panels for Ver.4, drawn in a common newsroom style."""

from render_v3 import INK, PAPER, SERIF


def kyiv_bridges(art):
    """Show the three reported crossings without assigning damage severity."""
    art.rect((0, 0, 312, 199), "#263e49")
    art.polygon((102, 0, 163, 0, 165, 35, 152, 71, 160, 105,
                 157, 141, 183, 175, 180, 199, 111, 199, 111, 172,
                 104, 141, 113, 106, 101, 73, 111, 38), "#52818d")
    for x, y in ((16, 48), (29, 62), (43, 43), (190, 59), (204, 43),
                 (238, 67), (256, 49), (18, 117), (47, 124), (198, 127)):
        art.rect((x, y, x+9, y+7), "#44616a")
    art.text(13, 14, "KYIV", 28, PAPER, SERIF)
    art.text(300, 19, "DNIPRO RIVER", 13, "#a8cfce", anchor="rt")
    for y, name in ((76, "Podilsko-Voskresenskyi"), (110, "Darnytskyi"), (144, "Southern")):
        art.line((57, y+2, 197, y+2), "#1a343e", 11)
        art.line((57, y, 197, y), "#f2d3a2", 6)
        art.oval((128, y-6, 140, y+6), "#a64236")
        art.line((140, y, 197, y), "#f2d3a2", 1)
        art.text(204, y, name, 9 if y == 76 else 12, PAPER, anchor="lm", limit=105)
    art.rect((0, 172, 312, 199), "#213742")
    art.text(12, 179, "11 REGIONS", 13, "#ffbd88")
    art.text(97, 180, "with outages in Ukraine", 12, PAPER)
    art.text(302, 161, "SCHEMATIC", 9, "#bed1cb", anchor="rt")


def climate_talks(art):
    art.rect((0, 0, 312, 199), "#20463d")
    art.text(14, 11, "COP31", 34, PAPER, SERIF)
    art.text(297, 19, "UN TALKS  /  ANTALYA", 12, "#c4d5b2", anchor="rt")
    art.text(297, 37, "Tens of thousands of participants", 10, PAPER, anchor="rt")
    # Delegations around the floor, with a shared draft and a deadline clock.
    art.oval((23, 68, 179, 159), "#416b58")
    art.oval((41, 80, 161, 146), "#264a40")
    for x, y in ((48, 75), (85, 65), (124, 67), (157, 83), (164, 120),
                 (139, 148), (96, 154), (56, 145), (33, 119)):
        art.rect((x-7, y-1, x+7, y+6), "#76947a")
        art.oval((x-5, y-8, x+5, y+2), "#e0b28b")
    art.rect((63, 92, 141, 133), "#f0e0b9")
    art.text(102, 101, "DRAFT DEAL", 11, "#22453c", anchor="mt")
    art.line((75, 122, 129, 122), "#8d9c7c", 2)
    art.line((144, 112, 198, 112), "#cdd9b7", 2)
    art.oval((228, 56, 273, 101), "#dfd4af")
    art.line((251, 64, 251, 79, 265, 79), "#25493e", 3)
    art.text(247, 110, "OVERTIME", 15, PAPER, anchor="mt")
    art.text(247, 132, "Talks continue", 12, "#d0dfbf", anchor="mt")
    art.rect((0, 172, 312, 199), "#17372f")
    art.text(13, 180, "Draft omitted fossil fuels; objections followed", 12, PAPER)


def nuclear_timeline(art):
    art.rect((0, 0, 312, 199), "#233d57")
    art.text(13, 14, "19 NOV", 14, "#c4d5dd")
    art.text(299, 14, "20 NOV", 14, "#f6c29b", anchor="rt")
    art.line((13, 41, 299, 41), "#92aabc", 2)
    art.oval((13, 36, 23, 46), "#c4d5dd")
    art.oval((290, 36, 300, 46), "#f6c29b")
    art.text(13, 53, "SHENZHEN", 15, PAPER)
    art.text(299, 53, "WASHINGTON", 15, PAPER, anchor="rt")
    # A shared negotiating table and the following day's podium.
    art.oval((26, 91, 138, 147), "#46647e")
    for x, y, name in ((45, 101, "U.S."), (93, 101, "CHINA"), (82, 130, "RUSSIA")):
        art.rect((x-18, y-8, x+18, y+8), "#263d54")
        art.text(x, y, name, 9, PAPER, anchor="mm")
    art.line((145, 120, 178, 120), "#dfbc94", 2)
    art.line((172, 115, 178, 120, 172, 125), "#dfbc94", 2)
    art.polygon((198, 132, 208, 106, 222, 101, 243, 101, 260, 110, 269, 131), INK)
    art.oval((220, 74, 246, 110), "#d1a283")
    art.polygon((219, 89, 219, 79, 227, 74, 246, 75, 247, 81, 234, 80), "#e5c68f")
    art.polygon((194, 127, 275, 127, 265, 157, 202, 157), "#96684c")
    art.rect((190, 126, 278, 132), "#dec091")
    art.line((252, 127, 250, 111, 244, 108), "#152838", 2)
    art.rect((0, 172, 312, 199), "#192e44")
    art.text(11, 179, "Nuclear-risk talks pledged", 11, PAPER)
    art.text(301, 179, "Trump warns of buildup", 11, "#f6c29b", anchor="rt")
