"""
Stamps a play button image + large visible label on every page of the PDF.
Each button is a clickable link opening the GitHub Pages viewer for that slide.
"""

import pymupdf as fitz
import shutil

PDF_IN   = "original_clean.pdf"
PDF_OUT  = "The Algo Trading Innovation Challenge.pdf"
BTN_IMG  = "play button.jpeg"
BASE_URL = "https://preenithi-15.github.io/algo/?slide="

# Button dimensions (points; 1 inch = 72 pts)
BTN_W    = 70
BTN_H    = 70
MARGIN   = 20
PAD      = 6

doc = fitz.open(PDF_IN)
total = len(doc)

for page_num in range(total):
    page  = doc[page_num]
    pw, ph = page.rect.width, page.rect.height

    # ── Play button position (bottom-right corner) ──────────────────────────
    btn_x0 = pw - MARGIN - BTN_W
    btn_y1 = ph - MARGIN
    btn_y0 = btn_y1 - BTN_H
    btn_x1 = pw - MARGIN
    btn_rect = fitz.Rect(btn_x0, btn_y0, btn_x1, btn_y1)

    page.insert_image(btn_rect, filename=BTN_IMG)

    # ── Label text ──────────────────────────────────────────────────────────
    label     = "Click to listen to the team explain"
    font_size = 11.5
    font_name = "helv"

    text_w = fitz.get_text_length(label, fontname=font_name, fontsize=font_size)

    # Right-align the label with the right edge of the button
    text_x = btn_x1 - text_w
    text_y = btn_y0 - 10          # just above the button

    # Semi-transparent white background pill
    bg = fitz.Rect(
        text_x - PAD,
        text_y - font_size - PAD,
        btn_x1 + PAD,
        text_y + PAD
    )
    page.draw_rect(bg,
                   color=(0.18, 0.37, 0.80),   # blue border
                   fill=(1, 1, 1),
                   fill_opacity=0.90,
                   width=1.5)

    # Main label text (dark navy)
    page.insert_text(
        (text_x, text_y),
        label,
        fontname=font_name,
        fontsize=font_size,
        color=(0.07, 0.20, 0.55),
    )

    # Arrow indicator pointing right toward the button ──────────────────────
    arrow_label = "▶"
    arrow_w     = fitz.get_text_length(arrow_label, fontname=font_name, fontsize=font_size + 1)
    arrow_x     = btn_x0 - arrow_w - 4
    arrow_y     = btn_y0 + BTN_H / 2 + (font_size + 1) / 3   # vertically centred on button
    page.insert_text(
        (arrow_x, arrow_y),
        arrow_label,
        fontname=font_name,
        fontsize=font_size + 1,
        color=(0.18, 0.37, 0.80),
    )

    # ── Clickable area covers label + button ────────────────────────────────
    link_rect = fitz.Rect(bg.x0, bg.y0, btn_x1, btn_y1)
    page.insert_link({
        "kind": fitz.LINK_URI,
        "from": link_rect,
        "uri" : f"{BASE_URL}{page_num + 1}"
    })

    print(f"  Slide {page_num+1}/{total} done")

# Save to temp then rename to avoid pymupdf in-place restriction
tmp = "tmp_output.pdf"
doc.save(tmp, garbage=4, deflate=True)
doc.close()
shutil.move(tmp, PDF_OUT)
print(f"\nSaved: {PDF_OUT}")
