# WearMap

**WearMap** is an open-source desktop application written in Python and PyQt6 for quantitative dental wear image analysis. It provides an integrated environment for measuring and classifying wear features on scanning electron microscope (SEM) and macroscopic dental images, with automated implementation of the Puech (1983) directionality classification system.

WearMap is published alongside the article:

> **[Citation placeholder — to be filled upon publication in SoftwareX]**
> DOI: [to be assigned]

---

## Code Metadata

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| License | MIT |
| Platform | Windows 10/11 (64-bit); source runs on any Python 3.10+ OS |
| Python dependencies | PyQt6 ≥ 6.4, Pillow ≥ 9.0, NumPy ≥ 1.21, openpyxl ≥ 3.0 |
| Permanent archive | [![DOI](https://zenodo.org/badge/DOI/PENDING.svg)](https://doi.org/PENDING) |
| User manual | `Wearmap_Manual.docx` (included in repository) |

---

## Description

WearMap addresses the reproducibility deficit in quantitative dental wear research by integrating the complete analysis pipeline — image loading, non-destructive enhancement, calibrated measurement, automated Puech classification, and structured statistical export — in a single open-source application.

The software is designed as a modern, open-source replacement for the discontinued SigmaScan Pro and eliminates the traditional multi-step workflow (SigmaScan Pro → SPSS post-processing) by computing and exporting Puech categories directly from each measurement.

### Features

| Feature | Description |
|---------|-------------|
| **Distance** | Two-click line measurement with real-world length, slope angle, and Puech class |
| **Area** | N-vertex polygon; area computed via Shoelace formula |
| **Angle** | Three-point angle (vertex at second click) |
| **Count** | Click-to-place numbered object counters |
| **Pits** | Click-to-place pit markers with pixel-coordinate export |
| **Calibration** | Draw reference line → enter real-world length; units span pm, nm, Å, µm, mm, cm, m, km, in, ft |
| **Puech classification** | Automated P1–P4 directionality from slope angle × jaw × side, replicating the original SPSS script logic |
| **Striation types** | User-defined striation type labels (1–9 keyboard shortcuts), configurable via Analysis menu |
| **Image filters** | Non-destructive brightness, contrast, sharpness, blur, grayscale, invert; special presets: Auto Contrast, Histogram Equalisation, Edge Detection, Sharpen |
| **Multi-image navigation** | Folder browsing with full per-image state preservation (measurements, calibration, tooth context) |
| **2D Landmarking & GPA** | Place N landmarks per image; Generalized Procrustes Analysis + k-means clustering with automatic elbow-method k selection |
| **Export** | Excel (.xlsx, two sheets), CSV, and tab-separated text |
| **Annotated image export** | PNG/TIFF/JPEG at original resolution with all overlays rendered at native scale |
| **Scale bar** | Visual scale bar overlay embeddable in exported images |
| **Drag-and-drop** | Drop image files directly onto the window |

### Puech (1983) Directionality Classification

Each distance measurement is automatically classified on the basis of striation slope angle (θ, normalised to α ∈ [0°, 180°]) and anatomical tooth context:

| Normalised angle α | Category |
|--------------------|----------|
| ≤ 22.5° or ≥ 157.5° | **P1 — Horizontal** |
| 22.5° – 67.5° (╲ diagonal) | **P3 Mesiodistal** (Lower-Left / Upper-Right) or **P4 Distomesial** (Lower-Right / Upper-Left) |
| 67.5° – 112.5° | **P2 — Vertical** |
| 112.5° – 157.5° (╱ diagonal) | **P3 Mesiodistal** (Lower-Right / Upper-Left) or **P4 Distomesial** (Lower-Left / Upper-Right) |

Classification updates in real time when the Tooth Context (jaw, side) is changed.

---

## Requirements

- Python ≥ 3.10
- PyQt6 ≥ 6.4.0
- Pillow ≥ 9.0.0
- NumPy ≥ 1.21.0
- openpyxl ≥ 3.0.0

A pre-built, self-contained Windows executable is available under [Releases](https://github.com/DrDyoweRoig/wearmap/releases) and requires no Python installation.

---

## Installation

### From source

```bash
git clone https://github.com/DrDyoweRoig/wearmap.git
cd wearmap
pip install -r requirements.txt
python main.py
```

### Windows executable

Download `Wearmap.exe` from the [Releases](https://github.com/DrDyoweRoig/wearmap/releases) page and run it directly.

### Build the executable yourself (Windows)

```bat
build.bat
```

Requires Python with PyInstaller installed. Output: `dist/Wearmap.exe`.

---

## Usage

### Basic workflow

1. **Open an image** — `File → Open Image` (Ctrl+O), `File → Open Folder` (Ctrl+Shift+O), or drag-and-drop onto the window.
2. **Set tooth context** — Select Jaw, Side, and Tooth type in the *Tooth Context* panel.
3. **Calibrate** — Press **K**, draw a line over the SEM scale bar, enter its real-world length and unit.
4. **Measure** — Use the measurement tools (see keyboard shortcuts below).
5. **Export** — `File → Export` (Ctrl+E) to save measurements to Excel, CSV, or text.

### Keyboard shortcuts

| Key | Action |
|-----|--------|
| **S** | Pan / Select |
| **D** | Distance |
| **A** | Area |
| **G** | Angle |
| **C** | Count |
| **P** | Pits |
| **K** | Calibrate |
| **L** | Toggle measurement labels |
| **1–9** | Assign striation type to selected measurement(s) |
| **Del** | Delete selected measurement |
| **←** / **→** | Navigate to previous / next image in folder |
| Ctrl+O | Open image |
| Ctrl+E | Export measurements |
| Ctrl+Shift+S | Save annotated image |
| Ctrl+L | Open 2D Landmarking dialog |

### Supported image formats

PNG, JPEG, TIFF, BMP, GIF, WebP, PLU, PLUX

### Export format

The Excel export contains two sheets:

- **Detail** — one row per measurement: Image, ID, Type, Tooth, Jaw, Side, Unit, Value, Slope (°), Puech class, Striation Type, Points (px)
- **Summary** — one row per Puech category (P1–P4) per image: count, mean distance, standard deviation; a bold **TOTAL** row aggregates all distance measurements per image

---

## Project structure

```
wearmap/
├── main.py              # Application entry point
├── main_window.py       # Main window: toolbar, panels, menus, export logic
├── canvas.py            # QGraphicsView canvas, measurement overlays, image filters
├── measurements.py      # Data models (Calibration, Measurement) and Puech algorithm
├── dialogs.py           # Calibration, scale bar, and striation type dialogs
├── landmark_dialog.py   # 2D Landmarking & Procrustes cluster analysis module
├── style.py             # Qt stylesheet (light green theme)
├── logo.ico             # Application icon
├── logo.png             # Logo
├── requirements.txt     # Python dependencies
├── build.bat            # Windows executable build script
├── Wearmap.spec         # PyInstaller specification
├── Wearmap_Manual.docx  # User manual
└── Wearmap_SoftwareX.docx  # SoftwareX article draft
```

---

## Citation

If you use WearMap in your research, please cite:

> Epitíe Dyowe Roig, A. (2025). Wearmap: An open-source Python application for quantitative dental wear image analysis and Puech directionality classification. *SoftwareX*, [volume], [pages]. DOI: [to be assigned]

BibTeX:
```bibtex
@article{wearmap2025,
  author  = {Epit{\'i}e Dyowe Roig, Albert},
  title   = {Wearmap: An open-source {Python} application for quantitative dental wear image analysis and {Puech} directionality classification},
  journal = {SoftwareX},
  year    = {2025},
  volume  = {},
  pages   = {},
  doi     = {}
}
```

---

## References

Puech, P.F. (1983). Tooth wear in La Ferrassie man. *American Journal of Physical Anthropology*, 61(2), 149–157. https://doi.org/10.1002/ajpa.1330610204

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Albert Epitíe Dyowe Roig, University of Barcelona.
