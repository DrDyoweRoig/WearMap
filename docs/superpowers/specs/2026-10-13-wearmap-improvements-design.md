# Wearmap — Icon, Analysis Area, Manual and Modern UI (Design)

Date: 2026-10-13 · Status: pending review

## Goal
Fix the app-icon bug, add a manually placed rectangular analysis area (ROI) whose
contents are counted/summarised, add Help → Read Manual, and modernise the UI —
without breaking the existing measurement/export workflow.

## Success criteria
1. `Wearmap.exe` shows a sharp icon in Explorer and the taskbar (ICO contains 16–256 px).
2. The user can create a W×H rectangle (calibrated units, px if uncalibrated), move and resize it
   on the image, and see live stats of what lies inside. State is stored per image and exported.
3. Help → Read Manual opens `Wearmap_Manual.docx` from source and from the frozen `.exe`.
4. UI uses a central theme (light + optional dark), SVG icons instead of emoji, no hard-coded colours.
5. Review fixes: Flip no longer deletes measurements; export extension handling is safe; `clear_all` resets ids.

## Review findings addressed
- `logo.ico` is 16×16 only; no AppUserModelID in `main.py` (icon bug).
- `MainWindow._flip` → `canvas.rotate_image(0)` → `clear_all()` silently drops measurements.
- `_export`: `base.replace(ext, ...)` replaces every occurrence of the extension in the path.
- Hard-coded colours in toolbar/status bar; `clear_all` does not reset `_next_id`.

## Design

### 1. Icon
- `tools/make_icon.py`: Pillow, `logo.png` → `logo.ico` with sizes 16,24,32,48,64,128,256 (LANCZOS).
- `main.py`: `ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Wearmap.App")` (Windows only, guarded).
- Rebuild exe and verify visually.

### 2. Analysis area (ROI)
- `measurements.py`: `AnalysisROI(x, y, w, h)` dataclass (px) + `contains(point)` and `compute_roi_stats(roi, measurements, cal, jaw, side)`
  (pure functions, GUI-free, unit-tested).
- Inclusion rule: a DISTANCE is inside if its **midpoint** is inside; COUNT/PITS points counted individually.
- Stats: striation count, count per Puech class P1–P4, mean ± SD length, ROI area, density (striations / mm² when calibrated),
  pits/count points inside.
- `canvas.py`: `ROIItem` (movable, 8 resize handles, min size, clamped to image); emits `roi_changed`.
  `get_state`/`restore_state` carry the ROI per image. One ROI per image.
- `dialogs.py`: `ROIDialog` (width, height, unit label from calibration).
- `main_window.py`: Edit → Create Analysis Area… / Remove Analysis Area; "Analysis Area" card in the side panel updated on `roi_changed`
  and on measurement changes.
- Export: extra sheet "ROI" (xlsx) / `_roi` file (csv, txt) with one row per image that has a ROI.

### 3. Manual
- Help → Read Manual: `QDesktopServices.openUrl(QUrl.fromLocalFile(path))`; path resolved from `sys._MEIPASS` or the source dir.
  Missing file → message box with the searched path.
- `Wearmap.spec` / `build.bat` add `Wearmap_Manual.docx` to datas.

### 4. Modern UI (approach A: own QSS tokens + SVG icons)
- `theme.py`: token dicts (light, dark), `build_qss(tokens)`; `style.py` becomes a thin wrapper. View → Theme (Light/Dark), choice stored in `QSettings`.
- `icons/*.svg` monochrome, tinted at runtime to the theme foreground; loader `icons.py` with cache.
- Larger grouped toolbar, card-style side panel, cleaner table, status-bar pills, clear active-tool state. Green accent kept.

### 5. Review fixes
Flip transforms measurement points (mirror coordinates) instead of clearing; safe extension handling via `os.path.splitext`; `clear_all` resets `_next_id`.

## Error handling
ROI larger than image is clamped; ROI with no calibration reports px and omits density; icon/theme asset missing falls back to text.

## Testing
`pytest` for `contains`, midpoint rule, stats and unit conversion, state round-trip, flip coordinate mapping, export path handling.
GUI behaviour verified manually by running the app.

## Order of work
5 → 1 → 3 → 2 → 4, one commit per step.

## Out of scope
Multiple ROIs per image, rotated/elliptical/polygon ROI, QML rewrite.
