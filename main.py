"""Export Version 4 by default, with the earlier editions selectable."""

from argparse import ArgumentParser
from os import environ
from pathlib import Path


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    editions = {
        "1": "world-edition.png",
        "2": "world-edition-newsroom.png",
        "3": "world-edition-v3.png",
        "4": "world-edition-v4.png",
    }
    parser.add_argument("--version", choices=tuple(editions), default="4")
    filename = editions[parser.parse_args().version]
    artwork = Path(__file__).resolve().with_name(filename)
    png = artwork.read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or len(png) > 1_048_576:
        raise ValueError("The artwork must be a PNG of at most 1 MiB")

    destination = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(png)


if __name__ == "__main__":
    main()
