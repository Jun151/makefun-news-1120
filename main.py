"""Write the finished editorial artwork to the make.fun output directory."""

from os import environ
from pathlib import Path


def main() -> None:
    artwork = Path(__file__).resolve().with_name("world-edition.png")
    png = artwork.read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or len(png) > 1_048_576:
        raise ValueError("The artwork must be a PNG of at most 1 MiB")

    destination = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(png)


if __name__ == "__main__":
    main()
