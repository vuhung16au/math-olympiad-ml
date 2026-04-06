# scripts

This folder contains helper scripts for generating QR codes used by HSC booklet projects.

## Scripts

- `generate_qrcodes.py`
  - Generates or updates `assets/qrcode.png` for each `HSC-*` booklet folder.
  - Does **not** modify LaTeX source files.

- `setup_qrcodes.py`
  - Generates or updates `assets/qrcode.png` for a curated list of HSC booklets.
  - Also inserts a QR-code page into each booklet `.tex` file if it is missing.

## Run from repository root

```bash
python scripts/generate_qrcodes.py
python scripts/setup_qrcodes.py
```

## Notes

- Run commands from the repository root (the folder containing `README.md`).
- The scripts may install the `qrcode[pil]` dependency automatically if needed.
- After running, rebuild booklet PDFs to reflect any LaTeX updates.
