#!/usr/bin/env python3
"""
build_pdf.py — Fallback academic PDF builder (ReportLab).

Converts a Markdown research paper into a two-column IEEE-style PDF with:
  - Full-width title block + abstract on page 1, two-column body flows below
    on the SAME page (no blank first page)
  - Inline architecture diagram rendered as a styled table when the marker
    <!-- ARCH_DIAGRAM --> appears in the markdown (or auto-inserted before §4)
  - Prismor brand colours (slate / blue)
  - Header/footer with short title and page numbers

Usage:
    python build_pdf.py --input paper.md --output paper.pdf
    python build_pdf.py --input paper.md --output paper.pdf --title-short "Short Title"
    python build_pdf.py --input paper.md --output paper.pdf --no-diagram

Requires: reportlab >= 4.0
"""

import argparse
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line

# ── Page geometry ─────────────────────────────────────────────────────────────

PAGE_W, PAGE_H = letter          # 8.5 × 11 inches
M_TOP    = 0.75 * inch
M_BOTTOM = 0.85 * inch
M_LEFT   = 0.75 * inch
M_RIGHT  = 0.75 * inch
COL_GAP  = 0.25 * inch

BODY_W   = PAGE_W - M_LEFT - M_RIGHT
COL_W    = (BODY_W - COL_GAP) / 2

# Height reserved for title + abstract on page 1 (expands with content)
TITLE_FRAME_H = 2.65 * inch

# ── Brand colours ─────────────────────────────────────────────────────────────

C_DARK    = colors.HexColor("#0f172a")
C_BLUE    = colors.HexColor("#1d4ed8")
C_NAVY    = colors.HexColor("#1e3a5f")
C_RULE    = colors.HexColor("#cbd5e1")
C_MUTED   = colors.HexColor("#64748b")
C_BG_CODE = colors.HexColor("#f8fafc")
C_BG_BOX  = colors.HexColor("#eff6ff")
C_BOX_BDR = colors.HexColor("#bfdbfe")

# ── Styles ────────────────────────────────────────────────────────────────────

def make_styles() -> dict:
    return {
        "title": ParagraphStyle(
            "PTitle", fontName="Times-Bold", fontSize=17, leading=21,
            textColor=C_DARK, alignment=TA_CENTER, spaceAfter=3,
        ),
        "subtitle": ParagraphStyle(
            "PSub", fontName="Times-Italic", fontSize=9.5, leading=12,
            textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=3,
        ),
        "abstract_h": ParagraphStyle(
            "PAbsH", fontName="Times-Bold", fontSize=9, leading=11,
            textColor=C_NAVY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=2,
        ),
        "abstract": ParagraphStyle(
            "PAbs", fontName="Times-Roman", fontSize=8.5, leading=11,
            textColor=C_DARK, alignment=TA_JUSTIFY,
            leftIndent=16, rightIndent=16, spaceAfter=0,
        ),
        "section": ParagraphStyle(
            "PSec", fontName="Times-Bold", fontSize=10, leading=13,
            textColor=C_NAVY, spaceBefore=8, spaceAfter=3, keepWithNext=1,
        ),
        "subsection": ParagraphStyle(
            "PSSec", fontName="Times-BoldItalic", fontSize=9, leading=12,
            textColor=C_DARK, spaceBefore=5, spaceAfter=2, keepWithNext=1,
        ),
        "body": ParagraphStyle(
            "PBody", fontName="Times-Roman", fontSize=9, leading=12,
            textColor=C_DARK, alignment=TA_JUSTIFY,
            spaceAfter=4, firstLineIndent=12,
        ),
        "body_ni": ParagraphStyle(
            "PBodyNI", fontName="Times-Roman", fontSize=9, leading=12,
            textColor=C_DARK, alignment=TA_JUSTIFY, spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "PBul", fontName="Times-Roman", fontSize=9, leading=12,
            textColor=C_DARK, alignment=TA_JUSTIFY,
            leftIndent=12, firstLineIndent=-8, spaceAfter=2,
        ),
        "code": ParagraphStyle(
            "PCode", fontName="Courier", fontSize=7.5, leading=10,
            textColor=C_DARK, leftIndent=8, spaceAfter=4,
            backColor=C_BG_CODE,
        ),
        "ref": ParagraphStyle(
            "PRef", fontName="Times-Roman", fontSize=8, leading=11,
            textColor=C_DARK, leftIndent=14, firstLineIndent=-14, spaceAfter=3,
        ),
        "diagram_label": ParagraphStyle(
            "PDiag", fontName="Helvetica-Bold", fontSize=8, leading=10,
            textColor=C_NAVY, alignment=TA_CENTER,
        ),
        "diagram_body": ParagraphStyle(
            "PDiagB", fontName="Helvetica", fontSize=7.5, leading=10,
            textColor=C_DARK, alignment=TA_CENTER,
        ),
        "diagram_caption": ParagraphStyle(
            "PDiagC", fontName="Times-Italic", fontSize=8, leading=10,
            textColor=C_MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=6,
        ),
    }


# ── Header / footer ───────────────────────────────────────────────────────────

def on_page(canvas, doc, short_title: str):
    canvas.saveState()
    y_h = PAGE_H - M_TOP + 8
    canvas.setStrokeColor(C_RULE)
    canvas.setLineWidth(0.5)
    canvas.line(M_LEFT, y_h, PAGE_W - M_RIGHT, y_h)
    canvas.setFont("Times-Italic", 7.5)
    canvas.setFillColor(C_MUTED)
    canvas.drawString(M_LEFT, y_h + 2, short_title)
    canvas.drawRightString(PAGE_W - M_RIGHT, y_h + 2,
                           "Prismor Security — Technical Report, April 2026")
    y_f = M_BOTTOM - 12
    canvas.line(M_LEFT, y_f, PAGE_W - M_RIGHT, y_f)
    canvas.drawCentredString(PAGE_W / 2, y_f - 10, str(doc.page))
    canvas.restoreState()


# ── Page templates ────────────────────────────────────────────────────────────

def build_doc(out_path: str, short_title: str) -> BaseDocTemplate:
    doc = BaseDocTemplate(
        out_path, pagesize=letter,
        leftMargin=M_LEFT, rightMargin=M_RIGHT,
        topMargin=M_TOP, bottomMargin=M_BOTTOM,
        title="Prismor Immunity Agent",
        author="Prismor Security",
    )

    cb = lambda c, d: on_page(c, d, short_title)

    body_h   = PAGE_H - M_TOP - M_BOTTOM
    title_y  = PAGE_H - M_TOP - TITLE_FRAME_H        # bottom of title frame
    col_h    = title_y - M_BOTTOM                    # height of column frames on page 1

    # Page 1: title strip (full width) + two columns below, all on the same page
    f_title = Frame(M_LEFT, title_y, BODY_W, TITLE_FRAME_H, id="title")
    f_p1_l  = Frame(M_LEFT,          M_BOTTOM, COL_W, col_h, id="p1_left")
    f_p1_r  = Frame(M_LEFT + COL_W + COL_GAP, M_BOTTOM, COL_W, col_h, id="p1_right")

    # Page 2+: pure two-column
    f_l = Frame(M_LEFT,          M_BOTTOM, COL_W, body_h, id="left")
    f_r = Frame(M_LEFT + COL_W + COL_GAP, M_BOTTOM, COL_W, body_h, id="right")

    pt_first  = PageTemplate(id="First",  frames=[f_title, f_p1_l, f_p1_r], onPage=cb)
    pt_twocol = PageTemplate(id="TwoCol", frames=[f_l, f_r],                 onPage=cb)

    doc.addPageTemplates([pt_first, pt_twocol])
    return doc


# ── Architecture diagram ──────────────────────────────────────────────────────

def make_arch_diagram(styles: dict, col_width: float) -> list:
    """
    Render the Prismor three-layer architecture as a styled ReportLab Table
    that fits inside a single column width.
    """
    S = styles
    W = col_width - 4  # slight inset

    # Row data: each cell is a Paragraph or string
    def box(title, lines, bg=C_BG_BOX, bdr=C_BOX_BDR):
        content = [Paragraph(title, S["diagram_label"])]
        for l in lines:
            content.append(Paragraph(l, S["diagram_body"]))
        return content

    warden_lines = [
        "PreToolUse / PostToolUse hooks",
        "YAML policy engine  •  25+ rules",
        "Shell · File · Network · MCP · Prompt",
        "Observe mode  |  Enforce mode",
        "SQLite + JSONL audit trail",
    ]
    sweep_lines = [
        "Gitleaks-powered residue scan",
        "AI tool caches: Claude · Cursor · Windsurf",
        "AES-256-CBC vault  •  Redact / Restore",
        "Run on-demand or via Stop hook",
    ]
    cloak_lines = [
        "@@SECRET:name@@ placeholder convention",
        "PreToolUse: decloak at execution time",
        "sed-wrap scrubs stdout before recording",
        "UserPromptSubmit: auto-detects pasted keys",
        "PostToolUse: scrubs MCP responses",
    ]

    def cell(title, lines, bg):
        inner = [[Paragraph(title, S["diagram_label"])]] + \
                [[Paragraph(l, S["diagram_body"])] for l in lines]
        t = Table(inner, colWidths=[W - 12])
        t.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (0, 0), bg),
            ("BACKGROUND",  (0, 1), (-1, -1), colors.white),
            ("BOX",         (0, 0), (-1, -1), 0.75, C_BOX_BDR),
            ("INNERGRID",   (0, 0), (-1, -1), 0.3, C_RULE),
            ("TOPPADDING",  (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING",(0,0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING",(0, 0), (-1, -1), 4),
        ]))
        return t

    warden_cell = cell("Warden — Runtime Monitor",  warden_lines, colors.HexColor("#dbeafe"))
    sweep_cell  = cell("Sweep — Secret Cleanup",    sweep_lines,  colors.HexColor("#dcfce7"))
    cloak_cell  = cell("Cloak — Secret Prevention", cloak_lines,  colors.HexColor("#fef9c3"))

    # Agent row at top
    agent_row = Table(
        [[Paragraph("IDE / Agent\n(Claude Code · Cursor · Windsurf)", S["diagram_body"])]],
        colWidths=[W - 12],
    )
    agent_row.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX",        (0, 0), (-1, -1), 1.0, C_NAVY),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))

    arrow = Paragraph("↓  PreToolUse / PostToolUse hooks  ↓", S["diagram_body"])

    outer = Table(
        [[agent_row], [arrow], [warden_cell], [arrow], [cloak_cell], [arrow], [sweep_cell]],
        colWidths=[W],
    )
    outer.setStyle(TableStyle([
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ]))

    return [
        Spacer(1, 6),
        outer,
        Paragraph(
            "Figure 1. Prismor Immunity Agent — three-layer defense architecture.",
            styles["diagram_caption"],
        ),
        Spacer(1, 4),
    ]


# ── Inline markdown → ReportLab XML ──────────────────────────────────────────

def md_inline(text: str) -> str:
    """
    Convert inline markdown to ReportLab paragraph XML.
    Processes backtick code spans first to avoid italic regex firing on
    underscores inside code text (e.g. LD_PRELOAD, NODE_OPTIONS).
    """
    parts = re.split(r'`([^`]+)`', text)
    out = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            # Inside backtick span — XML-escape only, no further markdown
            safe = (part.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"))
            out.append(f'<font name="Courier" size="8">{safe}</font>')
        else:
            safe = (part.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"))
            # Links: keep display text only
            safe = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', safe)
            # Bold-italic
            safe = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', safe)
            # Bold
            safe = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', safe)
            # Italic (asterisk form only — avoid matching asterisks in bullets)
            safe = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', safe)
            out.append(safe)
    return "".join(out)


# ── Markdown → flowable list ──────────────────────────────────────────────────

def parse_markdown(md_text: str, styles: dict, col_width: float,
                   inject_diagram: bool = True) -> list:
    lines = md_text.splitlines()
    S = styles
    flowables = []

    in_abstract = False
    in_refs = False
    abstract_buf: list[str] = []
    diagram_injected = False

    def flush_abstract():
        nonlocal abstract_buf
        text = " ".join(abstract_buf).strip()
        if text:
            flowables.append(Paragraph(md_inline(text), S["abstract"]))
        abstract_buf = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # H1 title — skip (rendered in title block separately)
        if line.startswith("# ") and not line.startswith("## "):
            i += 1
            continue

        # Byline / date line
        if line.startswith("**Prismor Security"):
            i += 1
            continue

        # Explicit diagram marker
        if line.strip() == "<!-- ARCH_DIAGRAM -->":
            flowables.extend(make_arch_diagram(S, col_width))
            diagram_injected = True
            i += 1
            continue

        # Horizontal rule
        if line.strip() in ("---", "***", "___"):
            if not in_abstract:
                flowables.append(HRFlowable(
                    width="100%", thickness=0.5, color=C_RULE,
                    spaceAfter=4, spaceBefore=4,
                ))
            i += 1
            continue

        # H2 section heading
        if line.startswith("## "):
            if in_abstract:
                flush_abstract()
                in_abstract = False
            txt = line[3:].strip()
            if txt.lower() == "abstract":
                in_abstract = True
                in_refs = False
                flowables.append(Paragraph("Abstract", S["abstract_h"]))
                i += 1
                continue
            if txt.lower().startswith("reference"):
                in_refs = True
            else:
                in_refs = False

            # Auto-inject diagram before section 4 if not yet inserted
            if inject_diagram and not diagram_injected:
                num_match = re.match(r'^(\d+)\.', txt)
                if num_match and int(num_match.group(1)) >= 4:
                    flowables.extend(make_arch_diagram(S, col_width))
                    diagram_injected = True

            flowables.append(Paragraph(md_inline(txt), S["section"]))
            i += 1
            continue

        # H3 subsection
        if line.startswith("### "):
            if in_abstract:
                flush_abstract()
                in_abstract = False
            txt = line[4:].strip()
            flowables.append(Paragraph(md_inline(txt), S["subsection"]))
            i += 1
            continue

        # H4
        if line.startswith("#### "):
            txt = line[5:].strip()
            flowables.append(Paragraph(f"<b>{md_inline(txt)}</b>", S["body_ni"]))
            i += 1
            continue

        # Blank line
        if not line.strip():
            if in_abstract and abstract_buf:
                flush_abstract()
            i += 1
            continue

        # Bullet
        if line.strip().startswith(("- ", "* ", "• ")):
            if in_abstract:
                flush_abstract()
                in_abstract = False
            txt = re.sub(r'^[\s\-\*•]+', '', line)
            flowables.append(Paragraph("• " + md_inline(txt), S["bullet"]))
            i += 1
            continue

        # Numbered list
        if re.match(r'^\d+\.\s', line.strip()):
            if in_abstract:
                flush_abstract()
                in_abstract = False
            txt = re.sub(r'^\d+\.\s+', '', line.strip())
            flowables.append(Paragraph("• " + md_inline(txt), S["bullet"]))
            i += 1
            continue

        # Fenced code block
        if line.strip().startswith("```"):
            if in_abstract:
                flush_abstract()
                in_abstract = False
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                escaped = (lines[i]
                           .replace("&", "&amp;")
                           .replace("<", "&lt;")
                           .replace(">", "&gt;"))
                code_lines.append(escaped)
                i += 1
            i += 1  # skip closing ```
            if code_lines:
                xml = "<br/>".join(
                    f'<font name="Courier" size="7">{l}</font>'
                    for l in code_lines[:25]
                )
                flowables.append(Paragraph(xml, S["code"]))
            continue

        # Reference line [N] ...
        if in_refs and re.match(r'^\[(\d+)\]', line.strip()):
            flowables.append(Paragraph(md_inline(line.strip()), S["ref"]))
            i += 1
            continue

        # Abstract accumulation
        if in_abstract:
            abstract_buf.append(line.strip())
            i += 1
            continue

        # Normal body paragraph
        if line.strip():
            flowables.append(Paragraph(md_inline(line.strip()), S["body"]))
        i += 1

    if abstract_buf:
        flush_abstract()

    return flowables


# ── Title block (goes into the full-width title frame on page 1) ──────────────

def build_title_block(styles: dict, title_text: str) -> list:
    S = styles
    return [
        Spacer(1, 0.08 * inch),
        Paragraph(md_inline(title_text), S["title"]),
        Spacer(1, 0.04 * inch),
        HRFlowable(width="55%", thickness=1.5, color=C_BLUE,
                   hAlign="CENTER", spaceBefore=2, spaceAfter=3),
        Paragraph(
            "Prismor Security · Technical Report, April 2026",
            S["subtitle"],
        ),
        Spacer(1, 0.05 * inch),
    ]


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input",      required=True, help="Input Markdown file")
    p.add_argument("--output",     required=True, help="Output PDF path")
    p.add_argument("--title",      default=None,
                   help="Full paper title (read from first # heading if omitted)")
    p.add_argument("--title-short", dest="title_short", default=None,
                   help="Short title for header (truncated from --title if omitted)")
    p.add_argument("--no-diagram", dest="no_diagram", action="store_true",
                   help="Skip auto-inserting the architecture diagram")
    args = p.parse_args()

    md_path = Path(args.input)
    if not md_path.exists():
        print(f"ERROR: {md_path} not found", file=sys.stderr)
        return 1

    md_text = md_path.read_text(encoding="utf-8")

    # Extract title from first H1 if not supplied
    title = args.title
    if not title:
        m = re.search(r'^# (.+)', md_text, re.MULTILINE)
        title = m.group(1).strip() if m else md_path.stem

    short_title = args.title_short or (title[:60] + "…" if len(title) > 60 else title)

    styles  = make_styles()
    doc     = build_doc(args.output, short_title)

    title_block  = build_title_block(styles, title)
    body_flows   = parse_markdown(
        md_text, styles, col_width=COL_W,
        inject_diagram=not args.no_diagram,
    )

    # Story: title block fills the title frame, then body flows into the
    # two column frames below — all on page 1, no blank first page.
    story = (
        title_block
        + [NextPageTemplate("TwoCol")]
        + body_flows
    )

    doc.build(story)
    size_kb = Path(args.output).stat().st_size // 1024
    print(f"PDF written → {args.output}  ({size_kb} KB, page size: letter)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
