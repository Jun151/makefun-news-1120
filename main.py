"""Export Version 2 by default, or select the preserved Version 1."""

from argparse import ArgumentParser
from os import environ
from pathlib import Path


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--version", choices=("1", "2"), default="2")
    version = parser.parse_args().version
    filename = {"1": "world-edition.png", "2": "world-edition-newsroom.png"}[version]
    artwork = Path(__file__).resolve().with_name(filename)
    png = artwork.read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or len(png) > 1_048_576:
        raise ValueError("The artwork must be a PNG of at most 1 MiB")

    destination = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(png)


if __name__ == "__main__":
    main()
