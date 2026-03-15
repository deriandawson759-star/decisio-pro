"""
DECISIO PRO - Generateur PDF Premium
Version finale - UTF-8 complet - Score 9/10
DocRaptor (Prince XML) - HTML/CSS -> PDF

Corrections integrees:
- UTF-8 preserve (accents, euro, TM)
- Tableaux jamais coupes (page-break-inside: avoid)
- Header horizontal propre via running()
- Couleur navy + dore dans tout le contenu
- Scores en barres de progression visuelles
- Graphique financier en CSS pur
- Pages separatrices entre D1/D2/D3
"""
import re
import requests
import json
from datetime import datetime

# =============================================================================
# PALETTE DE COULEURS DECISIO
# =============================================================================
NAVY = "#1C2B4A"
GOLD = "#C9A84C"
LIGHT_BG = "#F7F8FA"
BORDER = "#E2E5EB"
TEXT = "#1A1A2E"
MUTED = "#6B7280"
RED_ACC = "#C0392B"
GREEN_ACC = "#1A7A45"
BLUE_ACC = "#2563A8"
ORANGE = "#C4621A"

DOCRAPTOR_API_KEY = "xwOLiOzjmLgknBf9eA8H"

MODE_LABELS = {
    "flash": "AUDIT FLASH - 490 EUR",
    "premium": "AUDIT PREMIUM - 2 490 EUR",
    "transformation": "AUDIT TRANSFORMATION - 6 900 EUR",
    "redressement": "AUDIT REDRESSEMENT - 9 900 EUR",
    "diagnostic": "DIAGNOSTIC",
}

PRICE_MAP = {
    "flash": "490 EUR",
    "premium": "2 490 EUR",
    "transformation": "6 900 EUR",
    "redressement": "9 900 EUR",
    "diagnostic": "Gratuit",
}


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================
def clean_text(s):
    """Nettoie le texte en PRESERVANT UTF-8 (accents, euro, etc.)"""
    if not s:
        return ""
    s = str(s)
    # Remplacer uniquement les caracteres typographiques problematiques
    s = s.replace("\u2014", " - ")   # tiret long
    s = s.replace("\u2013", " - ")   # tiret moyen
    s = s.replace("\u2026", "...")    # points de suspension
    s = s.replace("\u00d7", "x")     # multiplication
    s = s.replace("\u2019", "'")     # apostrophe courbe
    s = s.replace("\u2018", "'")     # apostrophe courbe ouvrante
    s = s.replace("\u201c", '"')     # guillemet courbe
    s = s.replace("\u201d", '"')     # guillemet courbe fermant
    return s.strip()


def escape_html(s):
    """Echappe les caracteres HTML dangereux"""
    if not s:
        return ""
    s = clean_text(s)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    return s


def md_to_html(s):
    """Convertit le markdown basique en HTML"""
    if not s:
        return ""
    s = escape_html(s)
    # **gras** -> <strong>
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    # *italique* -> <em>
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    # Corriger les balises echappees par escape_html
    s = s.replace("&lt;strong&gt;", "<strong>")
    s = s.replace("&lt;/strong&gt;", "</strong>")
    s = s.replace("&lt;em&gt;", "<em>")
    s = s.replace("&lt;/em&gt;", "</em>")
    return s


def section_color(txt):
    """Retourne la couleur selon le type de section"""
    t = txt.upper()
    if any(x in t for x in ["EXEC", "SYNTH"]):
        return GOLD
    if any(x in t for x in ["QUICK", "WIN", "48H"]):
        return GREEN_ACC
    if any(x in t for x in ["DIAG", "PARTIE 1"]):
        return RED_ACC
    if any(x in t for x in ["DECIS", "PARTIE 2"]):
        return ORANGE
    if any(x in t for x in ["DEPLOY", "PARTIE 3"]):
        return GREEN_ACC
    return NAVY


# =============================================================================
# COMPOSANTS VISUELS
# =============================================================================
def render_score_bar(score_str):
    """Barre de progression visuelle pour un score /10"""
    try:
        val = float(score_str.replace(",", "."))
        pct = min(int(val * 10), 100)
        if val >= 7:
            color = GREEN_ACC
        elif val >= 5:
            color = ORANGE
        else:
            color = RED_ACC
        return (
            '<div style="display:table;width:100%;margin-top:4px">'
            '<div style="display:table-cell;vertical-align:middle;width:80%">'
            f'<div style="background:{BORDER};height:6px;border-radius:3px;overflow:hidden">'
            f'<div style="background:{color};height:6px;width:{pct}%"></div>'
            "</div></div>"
            f'<div style="display:table-cell;vertical-align:middle;padding-left:6px;'
            f'font-size:9pt;font-weight:700;color:{color}">{score_str}/10</div>'
            "</div>"
        )
    except Exception:
        return f'<span style="font-weight:700;color:{NAVY}">{score_str}/10</span>'


def render_chart(data):
    """Graphique a barres en CSS pur (navy + dore)"""
    if not data:
        return ""
    max_v = max(v for _, a, b in data for v in (a, b)) * 1.15
    if max_v == 0:
        max_v = 1
    cols = ""
    for label, current, projected in data:
        pct_c = round(current / max_v * 100, 1)
        pct_p = round(projected / max_v * 100, 1)
        cols += (
            '<td style="vertical-align:bottom;text-align:center;padding:0 4px">'
            '<div style="display:inline-block;vertical-align:bottom;margin:0 2px">'
            f'<div style="font-size:6pt;font-weight:600;color:{NAVY};margin-bottom:2px">{current}</div>'
            f'<div style="width:12mm;background:{NAVY};height:{pct_c}%;border-radius:2px 2px 0 0;min-height:3px"></div>'
            "</div>"
            '<div style="display:inline-block;vertical-align:bottom;margin:0 2px">'
            f'<div style="font-size:6pt;font-weight:600;color:#7A6020;margin-bottom:2px">{projected}</div>'
            f'<div style="width:12mm;background:{GOLD};height:{pct_p}%;border-radius:2px 2px 0 0;min-height:3px"></div>'
            "</div>"
            f'<div style="font-size:7pt;color:{MUTED};margin-top:3px;padding-top:2px;'
            f'border-top:1px solid {BORDER}">{clean_text(label)}</div>'
            "</td>"
        )
    return (
        f'<div style="page-break-inside:avoid;margin:5mm 0">'
        f'<table style="width:100%;border-bottom:2px solid {NAVY};height:45mm">'
        f"<tr>{cols}</tr></table>"
        f'<div style="text-align:center;font-size:7pt;color:{MUTED};margin-top:2mm">'
        f'<span style="display:inline-block;width:8px;height:8px;background:{NAVY};'
        f'border-radius:50%;margin-right:3px;vertical-align:middle"></span>Actuel'
        f"&nbsp;&nbsp;"
        f'<span style="display:inline-block;width:8px;height:8px;background:{GOLD};'
        f'border-radius:50%;margin-right:3px;vertical-align:middle"></span>Projection'
        f"</div></div>"
    )


def partie_break(num, titre, color):
    """Page de separation pleine page entre les parties D3"""
    return (
        f'<div class="partie-break" style="background:{color}">'
        f'<div class="partie-num">0{num}</div>'
        f'<div class="partie-titre">{titre}</div>'
        f'<div class="partie-rule"></div>'
        f'<div class="partie-sub">METHODE D3 - DECISIO AGENCY</div>'
        f"</div>"
    )


# =============================================================================
# PARSER MARKDOWN -> HTML
# =============================================================================
def parse_report(text):
    """Convertit le texte brut du rapport en HTML structure"""
    if not text:
        return '<p style="color:red">Aucun contenu</p>'

    lines = text.split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Ligne vide
        if not line:
            i += 1
            continue

        # Separateur ---
        if line == "---":
            out.append(f'<hr style="border:none;border-top:1px solid {BORDER};margin:5mm 0">')
            i += 1
            continue

        # H1 - Pages separatrices
        m = re.match(r"^#\s+(.+)", line)
        if m:
            txt = clean_text(m.group(1)).upper()
            if "PARTIE 1" in txt or "DIAGNOSTIC" in txt:
                out.append(partie_break(1, "DIAGNOSTIC", RED_ACC))
            elif "PARTIE 2" in txt or "DECISION" in txt:
                out.append(partie_break(2, "DECISION", ORANGE))
            elif "PARTIE 3" in txt or "DEPLOIEMENT" in txt:
                out.append(partie_break(3, "DEPLOIEMENT", GREEN_ACC))
            else:
                out.append(f'<h1 class="h1">{clean_text(m.group(1))}</h1>')
            i += 1
            continue

        # H2 - Section header avec couleur
        m = re.match(r"^##\s+(.+)", line)
        if m:
            txt = md_to_html(m.group(1).upper())
            color = section_color(txt)
            out.append(
                f'<div style="background:{LIGHT_BG};border-left:6px solid {color};'
                f'padding:4mm 5mm;margin:8mm 0 4mm;page-break-after:avoid">'
                f'<span style="font-size:10pt;font-weight:700;letter-spacing:0.04em;'
                f'color:{color}">{txt}</span></div>'
            )
            i += 1
            continue

        # H3
        m = re.match(r"^###\s+(.+)", line)
        if m:
            txt = md_to_html(m.group(1))
            out.append(
                f'<div style="font-size:10pt;font-weight:700;color:{NAVY};'
                f'margin:6mm 0 2mm;padding-bottom:1.5mm;border-bottom:2px solid {GOLD};'
                f'page-break-after:avoid">{txt}</div>'
            )
            i += 1
            continue

        # H4
        m = re.match(r"^####\s+(.+)", line)
        if m:
            txt = md_to_html(m.group(1))
            out.append(
                f'<div style="font-size:9.5pt;font-weight:600;color:{NAVY};'
                f'margin:4mm 0 1.5mm;page-break-after:avoid">{txt}</div>'
            )
            i += 1
            continue

        # Verite fondamentale (encadre navy + dore)
        if re.search(r"v[eé]rit[eé] fondamentale", line, re.I):
            txt = re.sub(r".*?v[eé]rit[eé] fondamentale\s*:?\s*", "", line, flags=re.I)
            txt = re.sub(r"^[#*>\[\]! ]+", "", txt).strip()
            if not txt and i + 1 < len(lines):
                i += 1
                txt = lines[i].strip()
            txt = md_to_html(txt)
            out.append(
                f'<div style="background:{NAVY};border-left:5px solid {GOLD};'
                f'padding:5mm 7mm;margin:6mm 0;page-break-inside:avoid">'
                f'<div style="font-size:7pt;font-weight:700;color:{GOLD};'
                f'letter-spacing:0.15em;text-transform:uppercase;margin-bottom:3mm">'
                f"VERITE FONDAMENTALE</div>"
                f'<div style="font-size:10.5pt;font-weight:600;font-style:italic;'
                f'color:white;line-height:1.6">{txt}</div></div>'
            )
            i += 1
            continue

        # KEY :: VALUE
        kv = re.match(r"\*\*(.+?)\*\*\s*::\s*(.*)", line)
        if kv:
            key = md_to_html(kv.group(1))
            val = md_to_html(kv.group(2))
            out.append(
                f'<div style="display:table;width:100%;padding:3mm 4mm;'
                f'background:{LIGHT_BG};border-bottom:1px solid {BORDER};'
                f'border-left:3px solid {GOLD};page-break-inside:avoid">'
                f'<span style="display:table-cell;width:50mm;font-size:9pt;'
                f'font-weight:700;color:{NAVY}">{key}</span>'
                f'<span style="display:table-cell;font-size:9.5pt;color:{TEXT}">{val}</span>'
                f"</div>"
            )
            i += 1
            continue

        # Blockquote
        if line.startswith(">") or line.startswith("->"):
            txt = re.sub(r"^-?>?\s*", "", line).strip()
            txt = md_to_html(txt)
            out.append(
                f'<div style="background:{LIGHT_BG};border-left:3px solid {BLUE_ACC};'
                f'padding:3mm 5mm;margin:3mm 0;font-size:9.5pt;font-style:italic;'
                f'color:#333;page-break-inside:avoid">&laquo; {txt} &raquo;</div>'
            )
            i += 1
            continue

        # OPTIONS A/B/C
        opt = re.match(r"^OPTION\s+([A-C])\s*[-\u2013]?\s*(.{5,})", line, re.I)
        if opt:
            letter = opt.group(1).upper()
            title = clean_text(opt.group(2).strip()[:80])
            score_val = "?"
            detail = ""
            j = i + 1
            while j < len(lines) and j < i + 6:
                nl = lines[j].strip()
                sm = re.search(r"Score\s*[:\-]?\s*([\d,.]+)", nl, re.I)
                if sm:
                    score_val = sm.group(1)
                    detail = re.sub(r"Score\s*[:\-]?.*", "", nl).strip()
                    break
                if nl and not nl.startswith("#") and not nl.startswith("-"):
                    detail += clean_text(nl[:100]) + " "
                j += 1
            color = ORANGE if letter == "A" else (BLUE_ACC if letter == "B" else MUTED)
            bar_html = render_score_bar(score_val)
            out.append(
                f'<div style="display:table;width:100%;background:{LIGHT_BG};'
                f'border:1px solid {BORDER};border-left:6px solid {color};'
                f'margin:3mm 0;page-break-inside:avoid">'
                f'<div style="display:table-cell;width:12mm;background:{color};'
                f'text-align:center;vertical-align:middle;font-weight:700;'
                f'font-size:12pt;color:white;padding:4mm 3mm">{letter}</div>'
                f'<div style="display:table-cell;padding:4mm 5mm;vertical-align:top">'
                f'<div style="font-size:9.5pt;font-weight:700;color:{NAVY};'
                f'margin-bottom:1.5mm">{title}</div>'
                f'<div style="font-size:8pt;color:{MUTED};margin-bottom:2mm">'
                f"{clean_text(detail.strip())}</div>"
                f"{bar_html}</div></div>"
            )
            i += 1
            continue

        # Message / SMS
        mm = re.match(r"^(Message|SMS)\s+(\d+)[^:]*:\s*(.*)", line, re.I)
        if mm:
            label = f"Message {mm.group(2)}"
            rest = mm.group(3).strip()
            if not rest and i + 1 < len(lines):
                i += 1
                rest = lines[i].strip()
            rest = md_to_html(rest)
            out.append(
                f'<div style="background:#EEF4FF;border:1px solid #C7D9F5;'
                f'border-left:4px solid {BLUE_ACC};border-radius:2mm;'
                f'padding:3mm 5mm;margin:3mm 0;page-break-inside:avoid">'
                f'<div style="font-size:7pt;font-weight:700;color:{BLUE_ACC};'
                f'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2mm">'
                f"{label}</div>"
                f'<div style="font-size:9.5pt;font-style:italic;color:{TEXT};'
                f'line-height:1.6">&laquo; {rest} &raquo;</div></div>'
            )
            i += 1
            continue

        # CHART_BAR:
        if line.upper().startswith("CHART_BAR:"):
            raw_data = line.split(":", 1)[1] if ":" in line else ""
            chart_rows = []
            for seg in raw_data.split("|"):
                parts = seg.split(":")
                if len(parts) == 3:
                    try:
                        chart_rows.append(
                            (parts[0].strip(), int(parts[1].strip()), int(parts[2].strip()))
                        )
                    except Exception:
                        pass
            if chart_rows:
                out.append(render_chart(chart_rows))
            i += 1
            continue

        # Liste a puces
        if re.match(r"^[-*]\s", line):
            items = []
            while i < len(lines):
                l = lines[i].strip()
                if re.match(r"^[-*]\s", l):
                    items.append(md_to_html(re.sub(r"^[-*]\s", "", l)))
                    i += 1
                else:
                    break
            if items:
                li_html = "".join(
                    f'<li style="font-size:9.5pt;line-height:1.7;color:{TEXT};'
                    f'margin-bottom:2.5mm;padding-left:4mm;position:relative">'
                    f'<span style="position:absolute;left:0;top:5pt;display:inline-block;'
                    f'width:4px;height:4px;border-radius:50%;background:{GOLD}"></span>'
                    f"{it}</li>"
                    for it in items
                )
                out.append(
                    f'<ul style="list-style:none;padding:0;margin:2mm 0 4mm">{li_html}</ul>'
                )
            continue

        # Liste numerotee
        if re.match(r"^\d+\.\s", line):
            items = []
            while i < len(lines):
                l = lines[i].strip()
                if re.match(r"^\d+\.\s", l):
                    items.append(md_to_html(re.sub(r"^\d+\.\s", "", l)))
                    i += 1
                else:
                    break
            if items:
                li_html = "".join(
                    f'<li style="font-size:9.5pt;line-height:1.7;color:{TEXT};'
                    f'margin-bottom:2.5mm">{it}</li>'
                    for it in items
                )
                out.append(
                    f'<ol style="padding-left:5mm;margin:2mm 0 4mm">{li_html}</ol>'
                )
            continue

        # Tableau markdown
        if line.startswith("|") and i + 1 < len(lines):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row_line = lines[i].strip()
                if re.match(r"^\|[-| :]+\|$", row_line):
                    i += 1
                    continue
                cells = [
                    md_to_html(c.strip())
                    for c in row_line.strip("|").split("|")
                ]
                rows.append(cells)
                i += 1
            if rows:
                html_rows = ""
                for idx, cells in enumerate(rows):
                    if idx == 0:
                        tds = "".join(
                            f'<th style="background:{NAVY};color:white;font-weight:700;'
                            f'padding:3mm 4mm;text-align:left;border-top:2.5px solid {GOLD}">'
                            f"{c}</th>"
                            for c in cells
                        )
                    else:
                        tds = "".join(
                            f'<td style="padding:2.5mm 4mm;border-bottom:1px solid {BORDER};'
                            f'color:{TEXT};line-height:1.5">{c}</td>'
                            for c in cells
                        )
                    html_rows += f"<tr>{tds}</tr>"
                out.append(
                    f'<table style="width:100%;border-collapse:collapse;margin:4mm 0;'
                    f'font-size:9pt;page-break-inside:avoid">{html_rows}</table>'
                )
            continue

        # Paragraphe normal
        txt = md_to_html(line)
        out.append(
            f'<p style="font-size:9.5pt;color:{TEXT};line-height:1.8;'
            f'text-align:justify;margin-bottom:3mm;orphans:3;widows:3">{txt}</p>'
        )
        i += 1

    return "\n".join(out)


# =============================================================================
# CONSTRUCTION DU HTML COMPLET
# =============================================================================
def build_html(report_text, nom, secteur, mode, date_str):
    """Construit le document HTML complet pour DocRaptor"""
    mode_label = MODE_LABELS.get(mode, MODE_LABELS["premium"])
    price = PRICE_MAP.get(mode, "2 490 EUR")
    content_html = parse_report(report_text)

    nom_c = clean_text(nom)
    secteur_c = clean_text(secteur)
    date_c = clean_text(date_str)
    mode_c = clean_text(mode_label)

    # =========================================================================
    # CSS COMPLET
    # =========================================================================
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

@page {{ size: A4; margin: 0; }}

@page content {{
    size: A4;
    margin: 20mm 24mm 18mm 24mm;
    @top-center {{
        content: element(pageHeader);
        width: 100%;
    }}
    @bottom-left {{
        content: "CONFIDENTIEL - DECISIO AGENCY";
        font-family: Arial, sans-serif;
        font-size: 7pt;
        color: {MUTED};
    }}
    @bottom-right {{
        content: counter(page);
        font-family: Arial, sans-serif;
        font-size: 8pt;
        font-weight: 700;
        color: {NAVY};
    }}
}}

@page partie {{ size: A4; margin: 0; }}

body {{
    font-family: 'Source Sans 3', Arial, sans-serif;
    font-size: 10pt;
    color: {TEXT};
    line-height: 1.7;
    background: white;
}}

/* PAGE DE GARDE */
.cover {{
    page: cover;
    width: 210mm;
    height: 297mm;
    display: flex;
    page-break-after: always;
}}
.cover-left {{
    width: 40%;
    background: {NAVY};
    padding: 12mm 7mm 10mm 9mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
}}
.cover-left::after {{
    content: '';
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 4px;
    background: {GOLD};
}}
.cover-right {{
    flex: 1;
    padding: 10mm 8mm 10mm 10mm;
    display: flex;
    flex-direction: column;
}}

/* PAGES SEPARATRICES */
.partie-break {{
    page: partie;
    width: 210mm;
    height: 297mm;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    page-break-before: always;
    page-break-after: always;
}}
.partie-num {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 80pt;
    font-weight: 900;
    color: rgba(255,255,255,0.12);
    line-height: 1;
}}
.partie-titre {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 30pt;
    font-weight: 700;
    color: white;
    letter-spacing: 0.05em;
    margin-top: -8mm;
}}
.partie-rule {{
    width: 18mm;
    height: 3px;
    background: rgba(255,255,255,0.4);
    margin: 5mm 0;
}}
.partie-sub {{
    font-size: 8pt;
    font-weight: 600;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.15em;
}}

/* CONTENU */
.content {{ page: content; }}

.page-header {{
    position: running(pageHeader);
    display: table;
    width: 100%;
    border-bottom: 1.5px solid {NAVY};
    padding-bottom: 2mm;
}}
.page-header-left {{
    display: table-cell;
    font-family: Arial, sans-serif;
    font-size: 7pt;
    font-weight: 700;
    color: {NAVY};
    letter-spacing: 0.06em;
}}
.page-header-right {{
    display: table-cell;
    text-align: right;
    font-family: Arial, sans-serif;
    font-size: 7pt;
    color: {MUTED};
}}

h1.h1 {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 14pt;
    font-weight: 700;
    color: {NAVY};
    margin: 8mm 0 3mm;
    page-break-after: avoid;
}}
"""

    # =========================================================================
    # HTML COMPLET
    # =========================================================================
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>DECISIO - Audit {nom_c}</title>
<style>{css}</style>
</head>
<body>

<!-- ============================== PAGE DE GARDE ============================== -->
<div class="cover">
  <div class="cover-left">
    <div>
      <div style="font-family:'Playfair Display',Georgia,serif;font-size:28pt;font-weight:900;color:white;line-height:1">DECISIO</div>
      <div style="font-size:6pt;font-weight:700;color:{GOLD};letter-spacing:0.18em;text-transform:uppercase;margin-top:3mm">M&Eacute;THODE D3&trade;</div>
      <div style="font-size:5.5pt;color:rgba(255,255,255,0.35);letter-spacing:0.07em;margin-top:2mm">FIRST PRINCIPLES &middot; AI-POWERED &middot; 48H</div>
    </div>
    <div style="margin-top:auto;padding-top:7mm">
      <div style="display:flex;align-items:flex-start;gap:4mm;margin-bottom:5mm">
        <div style="width:7mm;height:7mm;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;font-size:6pt;font-weight:700;color:{NAVY};flex-shrink:0">01</div>
        <div><div style="font-size:8pt;font-weight:700;color:white">DIAGNOSTIC</div><div style="font-size:6.5pt;color:{GOLD};opacity:0.8">Analyse compl&egrave;te</div></div>
      </div>
      <div style="display:flex;align-items:flex-start;gap:4mm;margin-bottom:5mm">
        <div style="width:7mm;height:7mm;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;font-size:6pt;font-weight:700;color:{NAVY};flex-shrink:0">02</div>
        <div><div style="font-size:8pt;font-weight:700;color:white">D&Eacute;CISION</div><div style="font-size:6.5pt;color:{GOLD};opacity:0.8">Options scor&eacute;es</div></div>
      </div>
      <div style="display:flex;align-items:flex-start;gap:4mm;margin-bottom:5mm">
        <div style="width:7mm;height:7mm;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;font-size:6pt;font-weight:700;color:{NAVY};flex-shrink:0">03</div>
        <div><div style="font-size:8pt;font-weight:700;color:white">D&Eacute;PLOIEMENT</div><div style="font-size:6.5pt;color:{GOLD};opacity:0.8">Plan d'action</div></div>
      </div>
    </div>
    <div style="font-size:6pt;color:rgba(255,255,255,0.3)">decisio.pro &middot; contact@decisio.pro</div>
  </div>
  <div class="cover-right">
    <div style="align-self:flex-end;background:{NAVY};color:{GOLD};font-size:6pt;font-weight:700;letter-spacing:0.1em;padding:2mm 4mm;border-radius:1.5mm">{mode_c}</div>
    <div style="font-family:'Playfair Display',Georgia,serif;font-size:24pt;font-weight:700;color:{NAVY};line-height:1.1;margin-top:14mm">{nom_c}</div>
    <div style="width:18mm;height:2px;background:{GOLD};margin:3mm 0"></div>
    <div style="font-size:12pt;color:#444;font-weight:300">{secteur_c}</div>
    <div style="font-size:8.5pt;color:{MUTED};margin-top:2mm">{date_c}</div>
    <hr style="border:none;border-top:1px solid {BORDER};margin:6mm 0">
    <div style="background:{LIGHT_BG};border:1px solid {BORDER};border-left:3px solid {GOLD};border-radius:3mm;padding:5mm 6mm;margin-top:auto">
      <div style="font-size:7pt;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:{NAVY};margin-bottom:2mm">Audit Strat&eacute;gique</div>
      <div style="font-family:'Playfair Display',Georgia,serif;font-size:22pt;font-weight:700;color:{NAVY};line-height:1">{clean_text(price)}</div>
      <div style="font-size:7pt;color:{MUTED};margin-top:2mm">Livraison 48h &middot; M&eacute;thode D3&trade; &middot; Confidentiel</div>
    </div>
    <div style="font-size:6pt;color:{MUTED};margin-top:6mm;line-height:1.6">
      Ce rapport est strictement confidentiel et destin&eacute; au seul usage du client d&eacute;sign&eacute; ci-dessus.
      Toute reproduction est interdite sans autorisation &eacute;crite de DECISIO AGENCY.
    </div>
  </div>
</div>

<!-- ============================== CONTENU ============================== -->
<div class="content">

  <div class="page-header">
    <span class="page-header-left">DECISIO &middot; M&Eacute;THODE D3&trade;</span>
    <span class="page-header-right">{nom_c} &middot; {secteur_c}</span>
  </div>

  <div style="font-family:'Playfair Display',Georgia,serif;font-size:16pt;font-weight:700;color:{NAVY};text-align:center;line-height:1.25;margin-bottom:3mm">
    RAPPORT D'AUDIT STRAT&Eacute;GIQUE &mdash; M&Eacute;THODE D3&trade;
  </div>
  <div style="font-size:8.5pt;color:{MUTED};text-align:center;margin-bottom:2mm">{nom_c} &middot; {secteur_c} &middot; {date_c}</div>
  <hr style="border:none;border-top:2px solid {NAVY};margin:2mm 0 1mm">
  <hr style="border:none;border-top:1px solid {GOLD};margin-bottom:8mm">

  {content_html}

  <div style="margin-top:10mm;padding-top:3mm;border-top:2px solid {NAVY};font-size:7.5pt;color:{MUTED};text-align:center;line-height:1.6">
    Rapport strictement confidentiel &middot; DECISIO AGENCY &middot; M&eacute;thode D3&trade; &middot; contact@decisio.pro
  </div>

</div>

</body>
</html>"""


# =============================================================================
# GENERATION PDF VIA DOCRAPTOR
# =============================================================================
def generate_pdf(report_text, nom, secteur, mode, date_str=None):
    """Genere le PDF via DocRaptor avec encodage UTF-8 correct"""
    if not date_str:
        date_str = datetime.now().strftime("%d %B %Y")

    html_content = build_html(report_text, nom, secteur, mode, date_str)

    # Appel API DocRaptor - IMPORTANT: ensure_ascii=False pour garder UTF-8
    payload = {
        "doc": {
            "document_content": html_content,
            "document_type": "pdf",
            "test": False,
            "prince_options": {
                "media": "print",
                "baseurl": "https://decisio.pro",
            },
        }
    }

    response = requests.post(
        "https://docraptor.com/docs",
        auth=(DOCRAPTOR_API_KEY, ""),
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/pdf",
        },
        timeout=90,
    )

    response.raise_for_status()
    return response.content
