# Wearmap Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the app icon, add a movable/resizable rectangular analysis area (ROI) with live stats and export, add Help → Read Manual, modernise the UI with a light/dark theme and SVG icons, and fix three bugs found in review.

**Architecture:** GUI-free logic (ROI geometry/stats, flip mapping, export-path helper, unit table) goes in `measurements.py` / small helpers and is unit-tested with pytest. Qt code (`ROIItem`, dialogs, panel, theme) is thin and verified by running the app. Flat module layout of the repo is kept.

**Tech Stack:** Python 3, PyQt6 (+QtSvg), Pillow, numpy, openpyxl, PyInstaller, pytest.

**Spec:** `docs/superpowers/specs/2026-10-13-wearmap-improvements-design.md`

## Global Constraints

- Flat modules at repo root (`canvas.py`, `main_window.py`, `measurements.py`, `dialogs.py`, `style.py`); new modules: `theme.py`, `icons.py`, `paths.py`; new dirs: `tests/`, `tools/`, `icons/`.
- No new runtime dependency (QtSvg ships with PyQt6). `pytest` is dev-only (`requirements-dev.txt`).
- ICO sizes exactly: 16, 24, 32, 48, 64, 128, 256. AppUserModelID string: `"Wearmap.App"`.
- ROI inclusion rule: DISTANCE counts if its **midpoint** is inside; COUNT/PITS points counted individually. One ROI per image.
- ROI stats: striation count, count per Puech class 1–4, mean ± SD length (sample SD, n−1, SD = 0.0 for n = 1, matching `_build_summary_rows`), ROI area, density per mm² (only when calibrated and unit convertible), pits/count points inside.
- Manual file: `Wearmap_Manual.docx`, opened with `QDesktopServices.openUrl`; must also be listed in `Wearmap.spec` datas and `build.bat`.
- Theme choice persisted in `QSettings("Wearmap Project", "Wearmap")` key `theme` (`"light"`/`"dark"`); green accent kept.
- Do not stage the user's unrelated modified files (`README.md`, `CITATION.cff`, `.zenodo.json`, `gen_softwarex.py`, `Wearmap_SoftwareX.docx`). Always `git add` explicit paths.
- Commit messages end with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.

## Review Focus

- ROI with zero striations inside: mean/SD are `None`, no ZeroDivisionError, panel shows "—".
- ROI on an uncalibrated image (unit `px`) or unit not in the mm table: density is `None`, area shown in px².
- ROI dragged/resized partly outside the image or to zero size: clamped to the image, minimum 5 px.
- ROI dialog given 0, negative or larger-than-image size: rejected/clamped, never creates an invalid ROI.
- Switching images (different sizes) restores each image's own ROI and clears the panel when none.
- Flip with measurements, ROI and scale bar present: nothing is deleted; points mirror correctly.
- Export path whose folder contains ".csv"/".txt": only the final extension changes.
- Manual file missing: message box, no crash. Dark theme: no leftover light inline colours (white-on-white text).

---

### Task 1: Review fixes (flip, export path, clear_all)

**Files:**
- Create: `tests/conftest.py`, `tests/test_review_fixes.py`, `requirements-dev.txt`
- Modify: `measurements.py` (add helpers), `canvas.py:347-368,632-640` (add `flip_image`, reset id), `main_window.py:771-779,846-856`

**Interfaces:**
- Produces (measurements.py):
  - `flip_points(points: list[tuple[float,float]], axis: str, width: float, height: float) -> list[tuple[float,float]]` — axis `"h"` → `(width - x, y)`, `"v"` → `(x, height - y)`.
  - `summary_path(base: str) -> str` — inserts `_summary` before the final extension only (`os.path.splitext`).
- Produces (canvas.py): `ImageCanvas.flip_image(axis: str) -> None` — mirrors `_original_pil`, mirrors every measurement's points with `flip_points`, redraws pixmap, keeps measurements.

- [ ] **Step 1:** `requirements-dev.txt` containing `pytest>=8`; run `pip install pytest`. `tests/conftest.py` inserts the repo root into `sys.path` and sets `os.environ["QT_QPA_PLATFORM"]="offscreen"`.
- [ ] **Step 2: Write failing tests** in `tests/test_review_fixes.py`:
  - `test_flip_points_horizontal`: `flip_points([(10,20)], "h", 100, 50) == [(90,20)]`
  - `test_flip_points_vertical`: `flip_points([(10,20)], "v", 100, 50) == [(10,30)]`
  - `test_summary_path_only_last_extension`: `summary_path(r"C:\data.csv\out.csv") == r"C:\data.csv\out_summary.csv"`
  - `test_clear_all_resets_ids` (needs a `QApplication` fixture): add two measurements to an `ImageCanvas`, `clear_all()`, assert `canvas._next_id == 1`.
- [ ] **Step 3:** Run `pytest tests/test_review_fixes.py -v` → FAIL (names undefined).
- [ ] **Step 4:** Implement `flip_points` and `summary_path` in `measurements.py`; set `self._next_id = 1` and `self._color_idx = 0` in `ImageCanvas.clear_all`; implement `flip_image` (do not call `clear_all`; update `Measurement.points` in place and call `item.prepareGeometryChange()` + `update()` per item; update the pixmap with `_pil_to_canvas`).
- [ ] **Step 5:** `MainWindow._flip` calls `self.canvas.flip_image(axis)` then re-applies the current filter values (reuse the handler around `main_window.py:320-346`) and `_refresh_table()`. In `_export`, replace `base.replace(ext, ...)` with `summary_path(base)`.
- [ ] **Step 6:** Run `pytest -v` → PASS. Run the app (`python main.py`), load an image, draw a distance, Edit → Flip Horizontal: the line must remain, mirrored.
- [ ] **Step 7: Commit** `git add tests requirements-dev.txt measurements.py canvas.py main_window.py` — "fix: flip keeps measurements, safe summary path, clear_all resets ids".

### Task 2: Multi-size icon and taskbar identity

**Files:**
- Create: `tools/make_icon.py`, `tests/test_icon.py`
- Modify: `logo.ico` (regenerated), `main.py`

**Interfaces:**
- Produces: `tools/make_icon.py` function `build_ico(src_png: str, dst_ico: str) -> None`; CLI `python tools/make_icon.py` regenerates `logo.ico` from `logo.png`.

- [ ] **Step 1: Write failing test** `test_ico_has_all_sizes`: after `build_ico("logo.png", tmp_path/"x.ico")`, `PIL.Image.open(...).ico.sizes()` equals `{(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)}`.
- [ ] **Step 2:** Run → FAIL. Implement `build_ico` with Pillow (`save(..., format="ICO", sizes=[...])` from an RGBA 256+ source, LANCZOS resize first).
- [ ] **Step 3:** Run `python tools/make_icon.py`, then `pytest tests/test_icon.py -v` → PASS.
- [ ] **Step 4:** In `main.py`, before creating `QApplication`: on `sys.platform == "win32"` call `ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Wearmap.App")` inside try/except.
- [ ] **Step 5:** Run `build.bat`-equivalent PyInstaller build (`pyinstaller Wearmap.spec`); open `dist/Wearmap.exe`: check the file icon in Explorer (large icons view) and the taskbar icon. Report what you saw.
- [ ] **Step 6: Commit** `git add tools tests/test_icon.py logo.ico main.py` — "fix: multi-size icon and AppUserModelID".

### Task 3: Help → Read Manual

**Files:**
- Create: `paths.py`, `tests/test_paths.py`
- Modify: `main_window.py:406-407` (Help menu), `main.py` (use `resource_path`), `Wearmap.spec` datas, `build.bat`

**Interfaces:**
- Produces: `paths.resource_path(name: str) -> str` (uses `sys._MEIPASS` when frozen, else the directory of `paths.py`); `MainWindow._open_manual() -> None`.

- [ ] **Step 1: Write failing test** `test_resource_path_points_to_repo_file`: `os.path.exists(resource_path("Wearmap_Manual.docx"))` is True.
- [ ] **Step 2:** Run → FAIL; implement `paths.py`; run → PASS. Make `main.py` use it for the icon path.
- [ ] **Step 3:** Add Help → "Read Manual" (shortcut `F1`) calling `_open_manual`: `QDesktopServices.openUrl(QUrl.fromLocalFile(resource_path("Wearmap_Manual.docx")))`; if the file does not exist or `openUrl` returns False, `QMessageBox.warning` naming the path searched.
- [ ] **Step 4:** Add `('Wearmap_Manual.docx', '.')` to `datas` in `Wearmap.spec` and `--add-data "Wearmap_Manual.docx;."` to `build.bat`.
- [ ] **Step 5:** Run the app, press F1 / use the menu: Word opens the manual. Temporarily rename the file to confirm the warning appears, then restore it.
- [ ] **Step 6: Commit** `git add paths.py tests/test_paths.py main.py main_window.py Wearmap.spec build.bat` — "feat: Help > Read Manual".

### Task 4: ROI model and statistics (no GUI)

**Files:**
- Modify: `measurements.py`
- Create: `tests/test_roi.py`

**Interfaces:**
- Produces (measurements.py):
  - `UNIT_TO_MM: dict[str, float]` with keys `pm 1e-9, nm 1e-6, "Å" 1e-7, "μm" 1e-3 (Greek mu U+03BC), mm 1, cm 10, m 1000, km 1e6, in 25.4, ft 304.8`.
  - `@dataclass AnalysisROI(x: float, y: float, w: float, h: float)` with `contains(self, pt: tuple[float,float]) -> bool` (inclusive edges), `area_px(self) -> float`, `clamped(self, img_w: float, img_h: float, min_size: float = 5.0) -> "AnalysisROI"`.
  - `@dataclass ROIStats(n_striations: int, per_puech: dict[int,int], mean_len: float|None, sd_len: float|None, area: float, area_unit: str, density_per_mm2: float|None, n_points: int)`.
  - `compute_roi_stats(roi: AnalysisROI, measurements: list[Measurement], cal: Calibration, jaw: str, side: str) -> ROIStats` — lengths via `cal.to_real`; `per_puech` always has keys 1–4; striations with Puech 0 count toward `n_striations` but not `per_puech`.
  - `ROI_HEADERS: list[str]` = `["Image","Width","Height","Unit","Area","Striations","P1","P2","P3","P4","Mean length","SD length","Density (/mm²)","Points"]` and `roi_export_row(image_name: str, roi, stats: ROIStats, cal) -> list`.

- [ ] **Step 1: Write failing tests** in `tests/test_roi.py` (build `Measurement`/`Calibration` directly):
  - `test_contains_inclusive_edges`; `test_midpoint_rule`: distance (0,0)-(30,0) with ROI x=10..40 is inside (midpoint 15), a distance whose endpoints are inside but midpoint outside is impossible for a rectangle — instead test a line (0,0)-(30,0) vs ROI x=20..40 → outside (midpoint 15).
  - `test_empty_roi_stats`: mean/sd `None`, `n_striations == 0`, `per_puech == {1:0,2:0,3:0,4:0}`.
  - `test_single_striation_sd_zero`: one distance → `sd_len == 0.0`.
  - `test_mean_sd_calibrated`: two distances 10 px and 20 px, `Calibration(pixel_length=1, real_length=2, unit="μm", is_calibrated=True)` → mean 30.0, sd ≈ 14.142.
  - `test_density_calibrated`: ROI 1000×1000 px at 1 μm/px = 1 mm² area; 5 striations → `density_per_mm2 == 5.0`, `area == 1_000_000 * 1e-6`... assert `area == pytest.approx(1_000_000)` in μm² and density 5.0.
  - `test_density_none_when_uncalibrated`: `density_per_mm2 is None`, `area_unit == "px²"`.
  - `test_pits_and_count_points_inside`: PITS with 3 points (2 inside) → `n_points == 2`.
  - `test_clamped_inside_image_min_size`: ROI (−10,−10,500,500) on 100×80 image → (0,0,100,80); ROI w=0 → w == 5.0.
- [ ] **Step 2:** Run `pytest tests/test_roi.py -v` → FAIL.
- [ ] **Step 3:** Implement the above in `measurements.py` (density = `n_striations / (area_px * (cal.scale*UNIT_TO_MM[unit])**2)`; area_unit via `cal.unit_str(is_area=True)`).
- [ ] **Step 4:** Run `pytest -v` → all PASS.
- [ ] **Step 5: Commit** `git add measurements.py tests/test_roi.py` — "feat: ROI model and statistics".

### Task 5: ROI in canvas, dialog, panel, state and export

**Files:**
- Modify: `canvas.py` (new `ROIItem`, signals, state), `dialogs.py` (new `ROIDialog`), `main_window.py` (Edit menu, panel, refresh hooks, export)
- Create: `tests/test_roi_state.py`

**Interfaces:**
- Consumes: `AnalysisROI`, `compute_roi_stats`, `roi_export_row`, `ROI_HEADERS`, `summary_path` (Tasks 1, 4).
- Produces (canvas.py): `ImageCanvas.roi_changed = pyqtSignal(object)` (emits `AnalysisROI | None`); `set_roi(roi: AnalysisROI | None) -> None`; `get_roi() -> AnalysisROI | None`; `get_state()["roi"]` / `restore_state` carry it (`state.get("roi")`, so old states still load); `flip_image` (Task 1) also flips the ROI with `flip_roi`.
- Produces (dialogs.py): `ROIDialog(unit: str, scale: float, img_w: int, img_h: int, parent=None)` with `get_size_px() -> tuple[float, float]`; inputs in calibrated units, `scale` = real units per px (1.0 and unit `px` if uncalibrated); OK disabled unless 0 < size ≤ image size.
- Produces (main_window.py): Edit → "Create Analysis Area…", "Remove Analysis Area"; `_refresh_roi_panel()`; `_all_rois() -> list[tuple[str, AnalysisROI, Calibration, str, str, list[Measurement]]]`.

- [ ] **Step 1: Write failing tests** in `tests/test_roi_state.py` (offscreen `QApplication` fixture, canvas with a generated 200×100 PNG): `test_roi_roundtrip_state` (set ROI, `get_state()`, load another image, `restore_state`, `get_roi()` equals original); `test_restore_state_without_roi_key` (state dict lacking "roi" → `get_roi() is None`); `test_set_roi_clamps_to_image`; `test_flip_moves_roi` (ROI x=10,w=20 on width 200 flipped "h" → x=170).
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Implement `set_roi/get_roi/roi_changed`, state keys, and `flip_roi(roi, axis, w, h) -> AnalysisROI` in `measurements.py`. `ROIItem(QGraphicsRectItem)`: movable, 8 square child handles (cosmetic size, `ItemIgnoresTransformations`), dashed accent pen with translucent fill, clamped to `pixmap_item.boundingRect()` on every change via `AnalysisROI.clamped`, reports changes through a callback that emits `roi_changed`. Z-value above measurements.
- [ ] **Step 4:** In `ImageCanvas.mousePressEvent`, when the tool is SELECT and the click lands on a `ROIItem` or handle, call `setDragMode(NoDrag)` before `super()` and restore `ScrollHandDrag` in `mouseReleaseEvent`, so dragging the ROI does not pan the image. With a measuring tool active the ROI ignores mouse buttons.
- [ ] **Step 5:** Implement `ROIDialog` and the Edit menu actions (Create replaces an existing ROI after the dialog; placed centred in the current viewport via `mapToScene(viewport().rect().center())`). Create is disabled-with-message when no image is loaded.
- [ ] **Step 6:** Add the "Analysis Area" card to the side panel (inside the Measurements tab under the table): labels for striations, P1–P4, mean ± SD (unit), area, density, points; "—" when `None`. `_refresh_roi_panel()` runs from `roi_changed`, `_refresh_table()`, tooth-context changes, and `_load()`.
- [ ] **Step 7:** Export: in `_export`, build ROI rows with `roi_export_row` for every image with an ROI (use `_all_rois`, saving the current state first as `_export` already does); xlsx → third sheet "ROI" via the existing `fill_sheet` helper; csv/txt → file `<base>_roi<ext>` next to the summary; skip silently when no ROIs exist.
- [ ] **Step 8:** Run `pytest -v` → PASS. Manual check in the app: create 300×200 μm area on a calibrated image; drag it, resize each handle, draw distances inside/outside and watch counts change; switch to another image and back; export to xlsx and open the ROI sheet; remove the area.
- [ ] **Step 9: Commit** `git add canvas.py dialogs.py main_window.py measurements.py tests/test_roi_state.py` — "feat: manually placed analysis area with live stats and export".

### Task 6: Theme system, SVG icons and restyled UI

**Files:**
- Create: `theme.py`, `icons.py`, `icons/*.svg` (open, pan, distance, area, angle, count, pits, calibrate, zoom-in, zoom-out, fit, labels, palette, roi, export, image, prev, next, theme), `tests/test_theme.py`
- Modify: `style.py` (becomes wrapper), `main_window.py` (toolbar, status bar, inline styles, View → Theme), `canvas.py` (background and ROI colours from theme), `dialogs.py:59-61` (inline preview style), `Wearmap.spec` and `build.bat` (add `icons` directory)

**Interfaces:**
- Produces (theme.py): `LIGHT: dict[str,str]`, `DARK: dict[str,str]` with identical keys (`bg, surface, surface_alt, border, text, text_muted, accent, accent_soft, accent_text, danger, canvas_bg`); `build_qss(tokens: dict[str,str]) -> str`; `current_theme() -> str` and `set_theme(name: str) -> None` (persist in `QSettings`).
- Produces (icons.py): `icon(name: str, color: str, size: int = 24) -> QIcon` (renders `icons/<name>.svg` via `QSvgRenderer`, replaces `currentColor`, caches by `(name,color,size)`, returns an empty `QIcon` if the file is missing); `MainWindow.apply_theme(name: str) -> None` re-tints all toolbar icons and re-applies the QSS.

- [ ] **Step 1: Write failing tests** `tests/test_theme.py`: `test_light_dark_same_keys`; `test_build_qss_has_no_unresolved_tokens` (no `{` placeholders left, contains the accent value); `test_icon_missing_returns_null` (`icon("nope", "#000").isNull()`); `test_icon_renders_nonempty` (offscreen QApplication, `icon("open","#14532D").pixmap(24,24)` is not null).
- [ ] **Step 2:** Run → FAIL. Implement `theme.py` (move the structure of the current QSS from `style.py` into token form: keep the green accent, rounded 8–10 px corners, hover/pressed/checked states, card style for `#card`, pill style for `#pill`); `style.py` keeps `MAIN_STYLE = build_qss(LIGHT)` for backwards compatibility. Draw the SVG icons as 24×24 monochrome strokes using `currentColor`.
- [ ] **Step 3:** Run tests → PASS.
- [ ] **Step 4:** Rewrite `_build_toolbar` to use `icons.icon(...)` with text under icon only for the main tools, grouped by separators (File/Navigate · Tools · View · Output); replace emoji text in menus with icons or plain text. Move every inline `setStyleSheet(...)` in `main_window.py` (nav label, status bar labels, hint) into QSS rules addressed by `setObjectName` (`navLabel`, `pill`, `hint`), remove the same in `dialogs.py`, and take the canvas background from `tokens["canvas_bg"]`.
- [ ] **Step 5:** Add View → Theme (Light / Dark, checkable group) calling `apply_theme`; load the saved theme in `MainWindow.__init__`.
- [ ] **Step 6:** Manual visual check in both themes: main window with and without an image, ROI selected, all dialogs (Calibration, Scale Bar, Rename Types, ROI, About, Landmarking), tables, tooltips. No unreadable text; icons visible in both themes. Take screenshots with the built-in browser/desktop tools if available and report issues found.
- [ ] **Step 7:** Rebuild the exe (`pyinstaller Wearmap.spec`) and confirm icons and theme load from the frozen build.
- [ ] **Step 8: Commit** `git add theme.py icons.py icons style.py main_window.py canvas.py dialogs.py Wearmap.spec build.bat tests/test_theme.py` — "feat: light/dark theme and SVG icon UI".

### Task 7: Docs and final verification

**Files:**
- Modify: `gen_manual.py` (add sections: Analysis Area, Help → Read Manual, Theme), regenerate `Wearmap_Manual.docx`; `README.md` is the user's file and has uncommitted changes — do not edit it, only mention the new features in the final report.

- [ ] **Step 1:** Add the manual sections (Catalan, matching the existing text) and run `python gen_manual.py`.
- [ ] **Step 2:** Run `pytest -v` (all green) and a final app smoke test of every Task's manual check.
- [ ] **Step 3: Commit** `git add gen_manual.py Wearmap_Manual.docx` — "docs: manual covers analysis area and theme".
- [ ] **Step 4:** Use `superpowers:requesting-code-review` / `/code-review` on the branch diff before finishing.

---

## Self-review

- **Spec coverage:** icon → T2; ROI (create, move/resize, stats, per-image state, export, remove) → T4–T5; manual → T3; theme + SVG icons + dark mode → T6; review fixes (flip, export path, clear_all) → T1; manual docs → T7.
- **Types:** `AnalysisROI`, `ROIStats`, `compute_roi_stats`, `roi_export_row`, `ROI_HEADERS`, `flip_points`, `flip_roi`, `summary_path`, `resource_path`, `icon`, `build_qss` are defined once (T1/T3/T4/T6) and used with the same names later.
- **Known assumption to confirm during T5:** the existing filters handler name near `main_window.py:320-346` is reused for re-applying filters after flip; the executor must read it first.
