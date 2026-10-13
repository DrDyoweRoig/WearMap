from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2.5)

GREEN_DARK  = RGBColor(0x14, 0x53, 0x2D)
GREEN_MED   = RGBColor(0x16, 0xA3, 0x4A)
GREY        = RGBColor(0x4B, 0x7A, 0x5A)
BLACK       = RGBColor(0x1A, 0x1A, 0x1A)

def fmt(run, bold=False, size=11, color=BLACK):
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.color.rgb = color

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    fmt(r, bold=True, size=16, color=GREEN_DARK)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"), "single")
    bot.set(qn("w:sz"), "6")
    bot.set(qn("w:space"), "4")
    bot.set(qn("w:color"), "16A34A")
    pBdr.append(bot)
    pPr.append(pBdr)

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    fmt(r, bold=True, size=12, color=GREEN_MED)

def body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    fmt(r, size=11)

def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    if bold_prefix and text.startswith(bold_prefix):
        rb = p.add_run(bold_prefix)
        fmt(rb, bold=True, size=11, color=GREEN_DARK)
        rr = p.add_run(text[len(bold_prefix):])
        fmt(rr, size=11)
    else:
        fmt(p.add_run(text), size=11)

# ── TITLE
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(60)
r = p.add_run("WEARMAP")
r.bold = True; r.font.name = "Calibri"; r.font.size = Pt(36)
r.font.color.rgb = GREEN_DARK

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("User Manual  ·  Version 1.0")
r.font.name = "Calibri"; r.font.size = Pt(14); r.font.color.rgb = GREEN_MED

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Image analysis software for dental wear research")
r.font.name = "Calibri"; r.font.size = Pt(11); r.font.color.rgb = GREY

doc.add_page_break()

# ── 1
h1("1. Introduction")
body("Wearmap is an image analysis program designed specifically for dental wear research. It lets you measure distances, areas and angles on microscope images, classify wear following the Puech (1983) model, and export all data to Excel or CSV.")
body("No installation is required: simply run the Wearmap.exe file.")

# ── 2
h1("2. System requirements")
bullet("Operating system: Windows 10 or Windows 11 (64-bit)", "Operating system:")
bullet("Memory: at least 4 GB of RAM", "Memory:")
bullet("Disk space: about 150 MB for the executable", "Disk space:")
bullet("Screen resolution: at least 1280 × 800 px", "Screen resolution:")

# ── 3
h1("3. Getting started")
h2("3.1 Opening an image")
body("There are three ways to open an image:")
bullet("Click the Open button on the toolbar.")
bullet("Use the menu File → Open Image.")
bullet("Drag and drop an image file onto the window.")
body("Supported formats: PNG, JPG, JPEG, TIF, TIFF, BMP, GIF, WEBP.")

h2("3.2 Browsing images")
body("If the open image is in a folder with more images, the Prev and Next buttons on the toolbar (or the left and right arrow keys) let you move between them. Each image keeps its own measurements, calibration and analysis area.")

h2("3.3 Zoom and panning")
bullet("Mouse wheel: zoom in and out.")
bullet("Pan tool (S) active + drag: move around the image.")
bullet("Zoom in / Zoom out / Fit buttons: manual zoom and fit to window.")

# ── 4
h1("4. Tooth context")
body("Before measuring distances, set the tooth context in the side panel on the right. This information is used to compute the Puech classification automatically.")
h2("4.1 Parameters")
bullet("Tooth: I1, I2, C, Pm3, Pm4, M1, M2, M3", "Tooth:")
bullet("Jaw: Upper (maxilla) or Lower (mandible)", "Jaw:")
bullet("Side: Right or Left", "Side:")
body("Any change to these parameters is applied immediately to all measurements of the current image.")

# ── 5
h1("5. Measurement tools")
body("Choose a tool from the toolbar or with its keyboard shortcut.")

h2("5.1 Pan  [S]")
body("Selection and panning mode. Click existing measurements to select them.")

h2("5.2 Distance  [D]")
body("Measures the distance between two points. Click the start point and then the end point. The result shows the distance, the slope (angle in degrees) and the Puech class (P1–P4), computed automatically.")
body("Puech classification:")
bullet("P1 — Horizontal (angle ≤ 22.5° or ≥ 157.5°)")
bullet("P2 — Vertical (angle between 67.5° and 112.5°)")
bullet("P3 — Mesial")
bullet("P4 — Distal")

h2("5.3 Area  [A]")
body("Draw a polygon to measure an area. Click to add vertices. Close the polygon with a right-click or a double-click. At least 3 points are required.")

h2("5.4 Angle  [G]")
body("Measures the angle formed by three points. Click the first end, the vertex and the second end.")

h2("5.5 Count  [C]")
body("Counts objects. Click to mark each object (a numbered circle appears). Finish the count with a right-click.")

h2("5.6 Pits  [P]")
body("Marks pits or points of interest with a small dot. It works like Count but without numbering. The coordinates of each pit are exported in the Points (px) column.")

h2("5.7 Calibrate  [K]")
body("Sets the real-world scale of the image. Draw a line over a feature of known size, enter its real length and unit (pm, nm, Å, μm, mm, cm…). Once calibrated, all measurements are shown in real units.")

h2("5.8 Labels  [L]")
body("Toggle button that shows or hides the text labels on the image. Measurements stay active.")

h2("5.9 Analysis area")
body("Lets you delimit a rectangular region of the image and count only the striations and parameters that fall inside it.")
bullet("Edit → Create Analysis Area… (or the Area box button): enter the width and height in calibrated units (in px if the image is not calibrated).")
bullet("The area appears in the centre of the view. Drag it to position it and use the handles on its edges and corners to resize it (with the Pan tool active).")
bullet("The Analysis Area box in the side panel updates live: number of striations, count per Puech class (P1–P4), mean length ± standard deviation, area, density (striations/mm²) and points (Count/Pits).")
bullet("Hold Ctrl and drag to pan the image even when the pointer is over the area.")
bullet("A striation counts as inside the area when its midpoint is inside.")
bullet("Each image has its own area. Edit → Remove Analysis Area deletes it.")

# ── 6
h1("6. Image filters")
body("The side panel has a Filters tab with the following controls:")
bullet("Brightness / Contrast / Sharpness: sliders from −100 to +100.", "Brightness / Contrast / Sharpness:")
bullet("Blur: Gaussian blur.", "Blur:")
bullet("Grayscale: converts to grayscale.", "Grayscale:")
bullet("Invert: inverts the colours.", "Invert:")
bullet("Special filters: Auto Levels, Equalize, Edge Detect, Sharpen.", "Special filters:")
bullet("Reset: restores the original image.", "Reset:")
body("Filters are non-destructive: they never modify the original file.")

# ── 7
h1("7. Exporting data")
body("Click the Export button (or press Ctrl+E). A dialog opens to choose the format and location.")

h2("7.1 Available formats")
bullet("Excel (.xlsx): recommended. A single file with separate sheets.", "Excel (.xlsx):")
bullet("CSV (.csv): produces separate files (_summary, and _roi when an analysis area exists).", "CSV (.csv):")
bullet("Tab-separated (.txt): same as CSV but tab-delimited.", "Tab-separated (.txt):")

h2("7.2 “Detail” sheet — individual data")
body("One row per measurement with the columns: Image, ID, Type, Tooth, Jaw, Side, Unit, Value, Slope (°), Puech, Striation Type, Points (px).")

h2("7.3 “Summary” sheet — statistics per Puech class")
body("One row per Puech category (1–4) per image, plus a TOTAL row at the end of each image with the overall count, mean and standard deviation of all distances.")

h2("7.4 “ROI” sheet — analysis area")
body("If any image has an analysis area, the Excel file includes a third sheet, ROI, with one row per image: size, area, striation count, count per Puech class, mean length and standard deviation, density and points. For CSV or TXT an additional file with the suffix _roi is created.")

# ── 8
h1("8. Keyboard shortcuts")
table = doc.add_table(rows=1, cols=2)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].paragraphs[0].add_run("Key").bold = True
hdr[1].paragraphs[0].add_run("Action").bold = True
shortcuts = [
    ("S", "Pan tool"),
    ("D", "Distance tool"),
    ("A", "Area tool"),
    ("G", "Angle tool"),
    ("C", "Count tool"),
    ("P", "Pits tool"),
    ("K", "Calibrate tool"),
    ("L", "Show / hide labels"),
    ("Ctrl+O", "Open image"),
    ("Ctrl+E", "Export measurements"),
    ("Delete", "Delete selected measurement"),
    ("← →", "Previous / next image"),
    ("Ctrl + =", "Zoom in"),
    ("Ctrl + -", "Zoom out"),
    ("Ctrl + 0", "Fit to window"),
    ("F1", "Open this manual"),
]
for k, d in shortcuts:
    row = table.add_row()
    rb = row.cells[0].paragraphs[0].add_run(k)
    fmt(rb, bold=True, size=11, color=GREEN_DARK)
    fmt(row.cells[1].paragraphs[0].add_run(d), size=11)

h2("8.1 Help and appearance")
bullet("F1 (Help → Read Manual): opens this manual.", "F1 (Help → Read Manual):")
bullet("View → Theme: switches between the light and dark theme. Your choice is remembered.", "View → Theme:")

# ── 9
h1("9. Troubleshooting")
h2("The image does not open")
body("Check that the format is supported. Large TIFF files may take a few seconds to load.")
h2("Labels cover the image")
body("Press L or click the Labels button to hide them temporarily.")
h2("The Summary sheet is empty")
body("The Summary sheet only includes Distance measurements with a valid Puech class (1–4). Check that Jaw and Side are set.")
h2("The Puech value is always “-”")
body("Set the Jaw and Side drop-downs in the Tooth Context panel before drawing distances.")

# ── END
doc.add_page_break()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(60)
r = p.add_run("Wearmap v1.0  ·  Dental wear analysis software")
r.font.name = "Calibri"; r.font.size = Pt(10); r.font.color.rgb = GREY

doc.save("Wearmap_Manual.docx")
print("Done")
