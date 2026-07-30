#!/usr/bin/env python3
"""Replace single-QR page blocks with shared dual-QR include in all HSC booklets."""

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

STANDARD_OLD = """% QR Code Page (Page 2)
\\newpage
\\vspace*{\\fill}
\\begin{center}
    \\includegraphics[width=0.25\\textwidth]{assets/qrcode.png}
    \\\\[0.3cm]
    \\small \\textit{Download PDF and resources:} \\\\
    \\footnotesize \\url{https://github.com/vuhung16au/math-olympiad-ml}
\\end{center}
\\vspace*{\\fill}
"""

STANDARD_OLD_NO_COMMENT = """\\newpage
\\vspace*{\\fill}
\\begin{center}
    \\includegraphics[width=0.25\\textwidth]{assets/qrcode.png}
    \\\\[0.5cm]
    \\small \\textit{Booklet repository:} \\\\[0.2cm]
    \\footnotesize \\texttt{\\detokenize{https://github.com/vuhung16au/math-olympiad-ml/}}
\\end{center}
\\vspace*{\\fill}
"""

THISPAGE_OLD = """% QR Code Page (Page 2)
\\newpage
\\thispagestyle{empty}
\\vspace*{\\fill}
\\begin{center}
    \\includegraphics[width=0.25\\textwidth]{assets/qrcode.png}
    \\\\[0.3cm]
    \\small \\textit{Download PDF and resources:} \\\\
    \\footnotesize \\url{https://github.com/vuhung16au/math-olympiad-ml}
\\end{center}
\\vspace*{\\fill}
"""

STANDARD_NEW = """% QR Code Page (Page 2)
\\newpage
\\input{../HSC-Common/assets/qrcode-page.tex}
"""

THISPAGE_NEW = """% QR Code Page (Page 2)
\\newpage
\\thispagestyle{empty}
\\input{../HSC-Common/assets/qrcode-page.tex}
"""

DIFFEQ_NEW = """% QR Code Page (Page 2)
\\newpage
\\input{../HSC-Common/assets/qrcode-page.tex}
"""


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent

    for booklet in HSC_BOOKLETS:
        tex_path = repo_root / booklet / f"{booklet}.tex"
        content = tex_path.read_text(encoding="utf-8")

        if booklet in {"HSC-Vectors", "HSC-Proofs"}:
            old, new = THISPAGE_OLD, THISPAGE_NEW
        elif booklet == "HSC-DifferentialEquations":
            old, new = STANDARD_OLD_NO_COMMENT, DIFFEQ_NEW
        else:
            old, new = STANDARD_OLD, STANDARD_NEW

        if old not in content:
            raise SystemExit(f"Could not find QR block in {tex_path}")

        tex_path.write_text(content.replace(old, new, 1), encoding="utf-8")
        print(f"✓ {booklet}")

    print(f"\nUpdated {len(HSC_BOOKLETS)} booklets.")


if __name__ == "__main__":
    main()
