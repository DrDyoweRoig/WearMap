# OpenScan — Implementation Plan

## Goal
Open-source Python image analysis tool equivalent to SigmaScan Pro.
Modern UI with light green color palette. Ships as a Windows executable.

## Tech Stack
- **PyQt6** — UI framework (modern, LGPL-licensed)
- **Pillow** — image loading support (TIFF, etc.)
- **NumPy** — calculations
- **PyInstaller** — compile to .exe

## Files [NEW]

| File | Purpose |
|------|---------|
| `openscan/requirements.txt` | Python dependencies |
| `openscan/build.bat` | PyInstaller one-click build |
| `openscan/main.py` | Entry point |
| `openscan/style.py` | Full QSS stylesheet (light green theme) |
| `openscan/measurements.py` | Data models: Calibration, Measurement, MeasurementType |
| `openscan/canvas.py` | QGraphicsView canvas + MeasurementItem graphics + Tool logic |
| `openscan/dialogs.py` | CalibrationDialog, AboutDialog |
| `openscan/main_window.py` | MainWindow — toolbar, panels, menus, status bar |

## Features per Module

### measurements.py
- `MeasurementType` enum: DISTANCE, AREA, ANGLE, COUNT
- `Calibration` dataclass: pixel→real scale, unit string
- `Measurement` dataclass: id, type, points, color, label
- Value calculation methods: _distance, _area (shoelace), _angle (dot product)
- `display_value(cal)` → formatted string with unit

### canvas.py
- `Tool` constants: SELECT, DISTANCE, AREA, ANGLE, COUNT, CALIBRATE
- `MeasurementItem(QGraphicsItem)`: paints distance/area/angle/count overlays
  - Cosmetic pen (doesn't scale with zoom)
  - Labels with white background bubbles
  - Filled handle points at vertices
- `ImageCanvas(QGraphicsView)`:
  - `load_image(path)` → pixmap at scene (0,0), fit to view
  - Scroll wheel zoom (anchor under mouse)
  - Middle-click or SELECT tool → scroll hand drag
  - Tool click logic: distance/calibrate (2 pts), area (N pts, right-click/dbl-click close), angle (3 pts), count (accumulate)
  - Live preview (dashed line from last point to cursor)
  - Signals: `measurement_added`, `calibration_line_drawn(float)`, `position_changed(x,y)`

### dialogs.py
- `CalibrationDialog(pixel_length)`: QDialog asking real-world length + unit
- `AboutDialog`: version, license, description

### main_window.py
- Toolbar: Open, | , Select, Distance, Area, Angle, Count, Calibrate, | , Zoom+, Zoom−, Fit, | , Export CSV, Delete
- Central QSplitter: canvas (left, 70%) | right panel (30%)
- Right panel tabs: **Measurements** (QTableWidget: #, Type, Value, Label) + Delete btn
- Status bar: `x=__, y=__  |  Zoom: __x  |  Calibration: __`
- Drag-and-drop image files onto window

## Color Palette
```
Background:    #F0FFF4
Panel bg:      #ECFDF5
Toolbar bg:    #DCFCE7
Border:        #86EFAC / #BBF7D0
Primary green: #22C55E
Button hover:  #16A34A
Text dark:     #166534 / #14532D
Canvas bg:     #1a1a2e  (dark, makes image pop)
```

## Measurement Colors (cycling)
`#22C55E, #0EA5E9, #F59E0B, #EF4444, #8B5CF6, #EC4899, #14B8A6, #F97316`
