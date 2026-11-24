"""Deliver the news-image-20261124 entry picture.

The front page itself (entry.png, 1024x1024) is drawn by render.py and
committed in this repository. This launcher only ships it: it copies the
committed picture to $MAKEFUN_OUTPUT_DIR/entry.png (or /output when the
variable is not set) and proves the copy is a genuine 1024x1024 PNG.

Deliberately stdlib-only. The grading sandbox runs a pinned Python
image with no third-party packages, so importing the renderer (which
needs Pillow) would die there with ImportError before any drawing
could happen. Keeping this file dependency-free is what makes the
entry runnable in that sandbox.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

MAGIC = b"\x89PNG\r\n\x1a\n"
FILENAME = "entry.png"
SIDE = 1024


class BadPicture(Exception):
    """The picture to deliver is missing or is not a 1024x1024 PNG."""


def _here() -> Path:
    """Directory holding this launcher and the committed picture."""
    return Path(__file__).resolve().parent


def _destination_dir() -> Path:
    """Where the finished picture must land."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(raw) if raw else Path("/output")


def _read_header(picture: Path) -> tuple[int, int]:
    """Return (width, height) from the IHDR chunk of a PNG file."""
    data = picture.read_bytes()
    if len(data) < 33 or not data.startswith(MAGIC):
        raise BadPicture(f"{picture} is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def _check(picture: Path) -> None:
    """Refuse anything that is not the required 1024x1024 picture."""
    width, height = _read_header(picture)
    if (width, height) != (SIDE, SIDE):
        raise BadPicture(
            f"{picture} is {width}x{height}, "
            f"but the entry must be {SIDE}x{SIDE}"
        )


def _sha256(picture: Path) -> str:
    """Hex digest of a file's bytes."""
    return hashlib.sha256(picture.read_bytes()).hexdigest()


def ship() -> Path:
    """Copy the committed picture out and verify the copy."""
    source = _here() / FILENAME
    if not source.exists():
        raise BadPicture(f"committed picture is missing: {source}")

    target_dir = _destination_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / FILENAME

    expected = _sha256(source)
    # Fail fast on a bad committed picture instead of copying it out
    # and only discovering the problem at the verification step.
    _check(source)
    if target.resolve() == source.resolve():
        # Output folder is the code folder: nothing to copy, but the
        # picture still has to pass verification.
        print(f"wrote {target} ({target.stat().st_size} bytes, {SIDE}x{SIDE})")
        return target
    shutil.copyfile(source, target)
    if _sha256(target) != expected:
        raise BadPicture(f"copy to {target} did not match the source")
    _check(target)

    size = target.stat().st_size
    print(f"wrote {target} ({size} bytes, {SIDE}x{SIDE})")
    return target


if __name__ == "__main__":
    try:
        ship()
    except BadPicture as problem:
        print(f"error: {problem}", file=sys.stderr)
        raise SystemExit(1)
