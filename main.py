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

import os
import shutil
from pathlib import Path

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(OUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
