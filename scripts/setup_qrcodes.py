#!/usr/bin/env python3
"""
Generate QR codes for all HSC-xxx booklet releases pages AND modify LaTeX files to include them.
"""

import subprocess
import sys
from pathlib import Path
import re

# Install qrcode if not available
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'qrcode[pil]'])
import qrcode

# List of all HSC booklets to process
HSC_BOOKLETS = [
    "HSC-Collections",
    "HSC-Combinatorics",
    "HSC-ComplexNumbers",
    "HSC-Distribution",
    "HSC-Functions",
    "HSC-Induction",
    "HSC-Inequalities",
    "HSC-Integrals",
    "HSC-LastResorts",
    "HSC-Math-Extension-2-Book",
    "HSC-Mechanics",
    "HSC-Polynomials",
    "HSC-Polynomials-Extension1",
    "HSC-Probability",
    "HSC-Proofs",
    "HSC-Trigonometry",
    "HSC-Vectors",
]

def generate_qrcode(folder_path, booklet_name):
    """Generate QR code for a booklet's releases page."""
    url = f"https://github.com/vuhung16au/math-olympiad-ml/tree/main/{booklet_name}/releases"
    
    # Create assets directory if it doesn't exist
    assets_dir = folder_path / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qrcode_path = assets_dir / "qrcode.png"
    img.save(qrcode_path)
    
    return qrcode_path

def find_insertion_point(tex_content):
    """Find the best place to insert QR code page (after title or first content)."""
    lines = tex_content.split('\n')
    
    # Look for \maketitle or \begin{document} followed by content
    for i, line in enumerate(lines):
        if '\\maketitle' in line:
            return i + 1
        if '\\tableofcontents' in line:
            return i + 1
        if '\\chapter{' in line or '\\section{' in line:
            return i
    
    # Fallback: find first non-comment line after \begin{document}
    for i, line in enumerate(lines):
        if '\\begin{document}' in line:
            return i + 1
    
    return 1

def modify_latex_file(tex_path, booklet_name):
    """Modify LaTeX file to include QR code on page 2."""
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if QR code is already included
    if 'qrcode.png' in content or 'QR Code' in content:
        print(f"  ⚠ QR code already present in {tex_path.name}")
        return False
    
    # Ensure graphicx package is included
    if '\\usepackage{graphicx}' not in content:
        # Add graphicx to preamble
        content = re.sub(
            r'(\\usepackage\{[^}]+\})',
            r'\1\n\\usepackage{graphicx}',
            content,
            count=1
        )
    
    # QR code page content
    qr_page = r"""
% QR Code Page (Page 2)
\newpage
\vspace*{\fill}
\begin{center}
    \includegraphics[width=0.25\textwidth]{assets/qrcode.png}
    \\[0.3cm]
    \small \textit{Download PDF and resources:} \\
    \footnotesize \url{https://github.com/vuhung16au/math-olympiad-ml}
\end{center}
\vspace*{\fill}
"""
    
    # Find insertion point
    lines = content.split('\n')
    insert_idx = find_insertion_point(content)
    
    # Insert QR code page
    lines.insert(insert_idx, qr_page)
    modified_content = '\n'.join(lines)
    
    # Write modified content
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    return True

def process_booklet(workspace_root, booklet_name):
    """Generate QR code and modify LaTeX for a single booklet."""
    folder_path = workspace_root / booklet_name
    
    if not folder_path.exists():
        print(f"✗ {booklet_name}: folder not found")
        return False
    
    # Find .tex file
    tex_file = folder_path / f"{booklet_name}.tex"
    if not tex_file.exists():
        print(f"✗ {booklet_name}: {booklet_name}.tex not found")
        return False
    
    try:
        # Generate QR code
        qr_path = generate_qrcode(folder_path, booklet_name)
        print(f"✓ {booklet_name}: QR code generated")
        
        # Modify LaTeX file
        if modify_latex_file(tex_file, booklet_name):
            print(f"✓ {booklet_name}: LaTeX file modified")
        else:
            print(f"✓ {booklet_name}: LaTeX file already has QR code")
        
        return True
    except Exception as e:
        print(f"✗ {booklet_name}: Error - {e}")
        return False

def main():
    """Main execution."""
    workspace_root = Path(__file__).resolve().parent.parent
    
    print("=" * 60)
    print("HSC Booklets: QR Code Setup")
    print("=" * 60)
    print()
    
    success_count = 0
    for booklet_name in HSC_BOOKLETS:
        if process_booklet(workspace_root, booklet_name):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"Summary: {success_count}/{len(HSC_BOOKLETS)} booklets processed")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Build PDFs: make pdf (in each folder)")
    print("2. Verify QR codes appear on page 2")
    print("3. Release: make release (in each folder)")

if __name__ == "__main__":
    main()
