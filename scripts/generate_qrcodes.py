#!/usr/bin/env python3
"""
Generate QR codes for all HSC-xxx booklet releases pages.
Stores QR codes in each booklet's assets/ directory.
"""

import subprocess
from pathlib import Path

try:
    import qrcode
except ImportError:
    print("Installing qrcode library...")
    subprocess.check_call(['pip', 'install', 'qrcode[pil]'])
    import qrcode

def generate_qrcodes():
    """Generate QR codes for all HSC-xxx folders."""
    workspace_root = Path(__file__).resolve().parent.parent
    
    for folder in workspace_root.iterdir():
        if folder.is_dir() and folder.name.startswith('HSC-'):
            # Generate URL for this booklet's releases page
            url = f"https://github.com/vuhung16au/math-olympiad-ml/tree/main/{folder.name}/releases"
            
            # Create assets directory if it doesn't exist
            assets_dir = folder / "assets"
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
            
            print(f"✓ Generated QR code for {folder.name}")
            print(f"  URL: {url}")
            print(f"  Saved to: {qrcode_path}")

if __name__ == "__main__":
    generate_qrcodes()
    print("\nDone! QR codes generated for all HSC-xxx booklets.")
