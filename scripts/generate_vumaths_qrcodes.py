#!/usr/bin/env python3
"""Generate qrcode-vumaths.png for each HSC booklet assets folder."""

import subprocess
import sys
from pathlib import Path

HSC_BOOKLETS = [
    "HSC-Collections",
    "HSC-Combinatorics",
    "HSC-ComplexNumbers",
    "HSC-DifferentialEquations",
    "HSC-Distributions",
    "HSC-Functions",
    "HSC-Induction",
    "HSC-Inequalities",
    "HSC-Integrals",
    "HSC-LastResorts",
    "HSC-Mechanics",
    "HSC-Polynomials",
    "HSC-Polynomials-Extension1",
    "HSC-Probability",
    "HSC-Proofs",
    "HSC-Sequences",
    "HSC-Trigonometry",
    "HSC-Vectors",
]

VUMATHS_URL = "https://vumaths.com/"


def main() -> None:
    try:
        import qrcode
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "qrcode[pil]"])
        import qrcode

    repo_root = Path(__file__).resolve().parent.parent

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(VUMATHS_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    for booklet in HSC_BOOKLETS:
        assets_dir = repo_root / booklet / "assets"
        assets_dir.mkdir(exist_ok=True)
        out_path = assets_dir / "qrcode-vumaths.png"
        img.save(out_path)
        print(f"✓ {booklet}: {out_path}")


if __name__ == "__main__":
    main()
