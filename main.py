# Passport spread of the Republic of Marenveld, for make.fun
# (program/v1, Python 3.13, standard library only).
#
# The spread itself lives in entry.png next to this file: it was drawn by
# draw_passport.py (Pillow, run locally) as an invented passport spread --
# data page with portrait and machine-readable zone, facing visa page with
# a Drenmark visa, entry/exit stamps from Drenmark, Aurelia and the Isle
# of Keth, a lighthouse-levy fee stamp, and the condition of issue that
# Marenveld is reached by ferry and coastal steamer only.
#
# The grader runs this program with no network, twice, and both runs must
# write identical bytes. Copying the finished PNG is deterministic by
# construction, so this entrypoint does exactly that: it places the spread
# at <output>/entry.png, where <output> is $MAKEFUN_OUTPUT_DIR when set
# (local runs) and /output otherwise (the grader's container).

import hashlib
import os
import shutil
import struct
from pathlib import Path

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

# The spread must be exactly 1024x1024: a bad or truncated render must
# never be shipped silently.
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _verify_png(path: Path, reference: Path) -> None:
    """Fail loudly unless path is a byte-identical copy of reference and
    a well-formed PNG of the expected dimensions."""
    data = path.read_bytes()
    expected = reference.read_bytes()
    if len(data) != len(expected):
        raise SystemExit(
            f"entry.png size mismatch: got {len(data)} bytes, "
            f"expected {len(expected)}"
        )
    if hashlib.sha256(data).hexdigest() != hashlib.sha256(expected).hexdigest():
        raise SystemExit("entry.png bytes differ from the source render")
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            f"entry.png is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(OUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    _verify_png(dest, src)


if __name__ == "__main__":
    main()
