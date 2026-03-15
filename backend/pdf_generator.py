"""
DECISIO PRO - Generateur PDF Premium
Version finale - UTF-8 complet - WeasyPrint (gratuit)
IA -> Markdown -> HTML -> PDF

Corrections integrees:
- UTF-8 preserve (accents, euro, TM)
- Tableaux jamais coupes (page-break-inside: avoid)
- Header/footer via @page margin boxes
- Couleur navy + dore dans tout le contenu
- Scores en barres de progression visuelles
- Graphique financier en CSS pur
- Pages separatrices entre D1/D2/D3
"""
import re
from io import BytesIO
from datetime import datetime
from weasyprint import HTML

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

MODE_LABELS = {
    "flash": "AUDIT FLASH \u2014 490 \u20ac",
    "premium": "AUDIT PREMIUM \u2014 2 490 \u20ac",
    "transformation": "AUDIT TRANSFORMATION \u2014 6 900 \u20ac",
    "redressement": "AUDIT REDRESSEMENT \u2014 9 900 \u20ac",
    "diagnostic": "DIAGNOSTIC",
}

PRICE_MAP = {
    "flash": "490 \u20ac",
    "premium": "2 490 \u20ac",
    "transformation": "6 900 \u20ac",
    "redressement": "9 900 \u20ac",
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
    s = s.replace("\u2014", " \u2014 ")
    s = s.replace("\u2013", " \u2013 ")
    s = s.replace("\u2026", "...")
    s = s.replace("\u2019", "\u2019")
    s = s.replace("\u2018", "\u2018")
    s = s.replace("\u201c", "\u00ab")
    s = s.replace("\u201d", "\u00bb")
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
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
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
            f'<div style="display:flex;align-items:center;gap:6px;margin-top:4px">'
            f'<div style="flex:1;background:{BORDER};height:6px;border-radius:3px;overflow:hidden">'
            f'<div style="background:{color};height:6px;width:{pct}%;border-radius:3px"></div>'
            f'</div>'
            f'<span style="font-size:9pt;font-weight:700;color:{color};white-space:nowrap">{score_str}/10</span>'
            f'</div>'
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

    bars_html = ""
    for label, current, projected in data:
        h_c = max(round(current / max_v * 120), 4)
        h_p = max(round(projected / max_v * 120), 4)
        bars_html += (
            f'<div style="display:inline-block;text-align:center;margin:0 8px;vertical-align:bottom">'
            f'<div style="display:flex;align-items:flex-end;justify-content:center;gap:3px;height:130px">'
            f'<div style="width:20px">'
            f'<div style="font-size:7pt;font-weight:600;color:{NAVY};margin-bottom:2px">{current:,}</div>'
            f'<div style="width:20px;background:{NAVY};height:{h_c}px;border-radius:2px 2px 0 0"></div>'
            f'</div>'
            f'<div style="width:20px">'
            f'<div style="font-size:7pt;font-weight:600;color:{GOLD};margin-bottom:2px">{projected:,}</div>'
            f'<div style="width:20px;background:{GOLD};height:{h_p}px;border-radius:2px 2px 0 0"></div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:8pt;color:{MUTED};margin-top:4px;border-top:1px solid {BORDER};padding-top:2px">{clean_text(label)}</div>'
            f'</div>'
        )

    return (
        f'<div style="page-break-inside:avoid;margin:16px 0;text-align:center">'
        f'{bars_html}'
        f'<div style="text-align:center;font-size:8pt;color:{MUTED};margin-top:8px">'
        f'<span style="display:inline-block;width:10px;height:10px;background:{NAVY};border-radius:50%;margin-right:4px;vertical-align:middle"></span>Actuel'
        f'&nbsp;&nbsp;&nbsp;'
        f'<span style="display:inline-block;width:10px;height:10px;background:{GOLD};border-radius:50%;margin-right:4px;vertical-align:middle"></span>Projection'
        f'</div></div>'
    )


def partie_break(num, titre, color):
    """Page de separation pleine page entre les parties D3"""
    return (
        f'<div style="page-break-before:always;page-break-after:always;'
        f'background:{color};width:100%;height:100%;display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;min-height:250mm;padding:40mm 20mm">'
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:80pt;'
        f'font-weight:900;color:rgba(255,255,255,0.12);line-height:1">0{num}</div>'
        f'<div style="font-family:Playfair Display,Georgia,serif;font-size:30pt;'
        f'font-weight:700;color:white;letter-spacing:0.05em;margin-top:-10mm">{titre}</div>'
        f'<div style="width:18mm;height:3px;background:rgba(255,255,255,0.4);margin:5mm 0"></div>'
        f'<div style="font-size:8pt;font-weight:600;color:rgba(255,255,255,0.4);'
        f'letter-spacing:0.15em">M\u00c9THODE D3\u2122 \u2014 DECISIO AGENCY</div>'
        f'</div>'
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

        if not line:
            i += 1
            continue

        if line == "---":
            out.append(f'<hr style="border:none;border-top:1px solid {BORDER};margin:16px 0">')
            i += 1
            continue

        # H1
        m = re.match(r"^#\s+(.+)", line)
        if m:
            txt = clean_text(m.group(1)).upper()
            if "PARTIE 1" in txt or "DIAGNOSTIC" in txt:
                out.append(partie_break(1, "DIAGNOSTIC", RED_ACC))
            elif "PARTIE 2" in txt or "DECISION" in txt:
                out.append(partie_break(2, "D\u00c9CISION", ORANGE))
            elif "PARTIE 3" in txt or "DEPLOIEMENT" in txt:
                out.append(partie_break(3, "D\u00c9PLOIEMENT", GREEN_ACC))
            else:
                out.append(f'<h1 style="font-family:Playfair Display,Georgia,serif;font-size:14pt;font-weight:700;color:{NAVY};margin:24px 0 8px;page-break-after:avoid">{clean_text(m.group(1))}</h1>')
            i += 1
            continue

        # H2
        m = re.match(r"^##\s+(.+)", line)
        if m:
            txt = md_to_html(m.group(1).upper())
            color = section_color(txt)
            out.append(
                f'<div style="background:{LIGHT_BG};border-left:6px solid {color};'
                f'padding:10px 14px;margin:24px 0 12px;page-break-after:avoid">'
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
                f'margin:18px 0 6px;padding-bottom:4px;border-bottom:2px solid {GOLD};'
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
                f'margin:12px 0 4px;page-break-after:avoid">{txt}</div>'
            )
            i += 1
            continue

        # Verite fondamentale
        if re.search(r"v[e\u00e9]rit[e\u00e9] fondamentale", line, re.I):
            txt = re.sub(r".*?v[e\u00e9]rit[e\u00e9] fondamentale\s*:?\s*", "", line, flags=re.I)
            txt = re.sub(r"^[#*>\[\]! ]+", "", txt).strip()
            if not txt and i + 1 < len(lines):
                i += 1
                txt = lines[i].strip()
            txt = md_to_html(txt)
            out.append(
                f'<div style="background:{NAVY};border-left:5px solid {GOLD};'
                f'padding:14px 18px;margin:16px 0;page-break-inside:avoid">'
                f'<div style="font-size:7pt;font-weight:700;color:{GOLD};'
                f'letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px">'
                f'V\u00c9RIT\u00c9 FONDAMENTALE</div>'
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
                f'<div style="display:flex;padding:8px 10px;background:{LIGHT_BG};'
                f'border-bottom:1px solid {BORDER};border-left:3px solid {GOLD};'
                f'page-break-inside:avoid">'
                f'<span style="min-width:140px;font-size:9pt;font-weight:700;color:{NAVY}">{key}</span>'
                f'<span style="font-size:9.5pt;color:{TEXT}">{val}</span></div>'
            )
            i += 1
            continue

        # Blockquote
        if line.startswith(">") or line.startswith("->"):
            txt = re.sub(r"^-?>?\s*", "", line).strip()
            txt = md_to_html(txt)
            out.append(
                f'<div style="background:{LIGHT_BG};border-left:3px solid {BLUE_ACC};'
                f'padding:8px 14px;margin:8px 0;font-size:9.5pt;font-style:italic;'
                f'color:#333;page-break-inside:avoid">\u00ab {txt} \u00bb</div>'
            )
            i += 1
            continue

        # OPTIONS A/B/C
        opt = re.match(r"^OPTION\s+([A-C])\s*[-\u2013\u2014]?\s*(.{5,})", line, re.I)
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
                f'<div style="display:flex;background:{LIGHT_BG};border:1px solid {BORDER};'
                f'border-left:6px solid {color};margin:8px 0;page-break-inside:avoid">'
                f'<div style="min-width:36px;background:{color};display:flex;align-items:center;'
                f'justify-content:center;font-weight:700;font-size:14pt;color:white;padding:10px">{letter}</div>'
                f'<div style="padding:10px 14px;flex:1">'
                f'<div style="font-size:9.5pt;font-weight:700;color:{NAVY};margin-bottom:4px">{title}</div>'
                f'<div style="font-size:8pt;color:{MUTED};margin-bottom:6px">{clean_text(detail.strip())}</div>'
                f'{bar_html}</div></div>'
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
                f'border-left:4px solid {BLUE_ACC};border-radius:6px;'
                f'padding:10px 14px;margin:8px 0;page-break-inside:avoid">'
                f'<div style="font-size:7pt;font-weight:700;color:{BLUE_ACC};'
                f'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px">'
                f'{label}</div>'
                f'<div style="font-size:9.5pt;font-style:italic;color:{TEXT};'
                f'line-height:1.6">\u00ab {rest} \u00bb</div></div>'
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
                    f'margin-bottom:6px;padding-left:12px;position:relative">'
                    f'<span style="position:absolute;left:0;top:7px;display:inline-block;'
                    f'width:5px;height:5px;border-radius:50%;background:{GOLD}"></span>'
                    f'{it}</li>'
                    for it in items
                )
                out.append(f'<ul style="list-style:none;padding:0;margin:6px 0 12px">{li_html}</ul>')
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
                    f'<li style="font-size:9.5pt;line-height:1.7;color:{TEXT};margin-bottom:6px">{it}</li>'
                    for it in items
                )
                out.append(f'<ol style="padding-left:16px;margin:6px 0 12px">{li_html}</ol>')
            continue

        # Tableau markdown
        if line.startswith("|") and i + 1 < len(lines):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row_line = lines[i].strip()
                if re.match(r"^\|[-| :]+\|$", row_line):
                    i += 1
                    continue
                cells = [md_to_html(c.strip()) for c in row_line.strip("|").split("|")]
                rows.append(cells)
                i += 1
            if rows:
                html_rows = ""
                for idx, cells in enumerate(rows):
                    if idx == 0:
                        tds = "".join(
                            f'<th style="background:{NAVY};color:white;font-weight:700;'
                            f'padding:8px 10px;text-align:left;border-top:2.5px solid {GOLD}">{c}</th>'
                            for c in cells
                        )
                    else:
                        tds = "".join(
                            f'<td style="padding:7px 10px;border-bottom:1px solid {BORDER};'
                            f'color:{TEXT};line-height:1.5">{c}</td>'
                            for c in cells
                        )
                    html_rows += f"<tr>{tds}</tr>"
                out.append(
                    f'<table style="width:100%;border-collapse:collapse;margin:10px 0;'
                    f'font-size:9pt;page-break-inside:avoid">{html_rows}</table>'
                )
            continue

        # Paragraphe normal
        txt = md_to_html(line)
        out.append(
            f'<p style="font-size:9.5pt;color:{TEXT};line-height:1.8;'
            f'text-align:justify;margin-bottom:8px;orphans:3;widows:3">{txt}</p>'
        )
        i += 1

    return "\n".join(out)


# =============================================================================
# CONSTRUCTION DU HTML COMPLET
# =============================================================================
def build_html(report_text, nom, secteur, mode, date_str):
    """Construit le document HTML complet pour WeasyPrint"""
    mode_label = MODE_LABELS.get(mode, MODE_LABELS["premium"])
    price = PRICE_MAP.get(mode, "2 490 \u20ac")
    content_html = parse_report(report_text)

    nom_c = clean_text(nom)
    secteur_c = clean_text(secteur)
    date_c = clean_text(date_str)
    mode_c = clean_text(mode_label)

    # CSS adapte pour WeasyPrint
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

@page {{
    size: A4;
    margin: 20mm 22mm 18mm 22mm;
    @bottom-left {{
        content: "CONFIDENTIEL \u00b7 DECISIO AGENCY";
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

@page cover {{
    margin: 0;
    @bottom-left {{ content: none; }}
    @bottom-right {{ content: none; }}
}}

@page partie {{
    margin: 0;
    @bottom-left {{ content: none; }}
    @bottom-right {{ content: none; }}
}}

body {{
    font-family: 'Source Sans 3', Arial, sans-serif;
    font-size: 10pt;
    color: {TEXT};
    line-height: 1.7;
    background: white;
}}

.cover-page {{
    page: cover;
    page-break-after: always;
}}

table {{
    page-break-inside: avoid;
}}
tr {{
    page-break-inside: avoid;
}}
"""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>DECISIO \u2014 Audit {nom_c}</title>
<style>{css}</style>
</head>
<body>

<!-- ============================== PAGE DE GARDE ============================== -->
<div class="cover-page" style="width:210mm;height:297mm;display:flex">
  <div style="width:40%;background:{NAVY};padding:12mm 7mm 10mm 9mm;display:flex;flex-direction:column;justify-content:space-between;position:relative">
    <div style="position:absolute;right:0;top:0;bottom:0;width:4px;background:{GOLD}"></div>
    <div>
      <div style="font-family:Playfair Display,Georgia,serif;font-size:28pt;font-weight:900;color:white;line-height:1">DECISIO</div>
      <div style="font-size:6pt;font-weight:700;color:{GOLD};letter-spacing:0.18em;text-transform:uppercase;margin-top:3mm">M\u00c9THODE D3\u2122</div>
      <div style="font-size:5.5pt;color:rgba(255,255,255,0.35);letter-spacing:0.07em;margin-top:2mm">FIRST PRINCIPLES \u00b7 AI-POWERED \u00b7 48H</div>
    </div>
    <div style="margin-top:auto;padding-top:7mm">
      <div style="display:flex;align-items:flex-start;gap:4mm;margin-bottom:5mm">
        <div style="width:7mm;height:7mm;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;font-size:6pt;font-weight:700;color:{NAVY};flex-shrink:0">01</div>
        <div><div style="font-size:8pt;font-weight:700;color:white">DIAGNOSTIC</div><div style="font-size:6.5pt;color:{GOLD};opacity:0.8">Analyse compl\u00e8te</div></div>
      </div>
      <div style="display:flex;align-items:flex-start;gap:4mm;margin-bottom:5mm">
        <div style="width:7mm;height:7mm;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;font-size:6pt;font-weight:700;color:{NAVY};flex-shrink:0">02</div>
        <div><div style="font-size:8pt;font-weight:700;color:white">D\u00c9CISION</div><div style="font-size:6.5pt;color:{GOLD};opacity:0.8">Options scor\u00e9es</div></div>
      </div>
      <div style="display:flex;align-items:flex-start;gap:4mm;margin-bottom:5mm">
        <div style="width:7mm;height:7mm;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;font-size:6pt;font-weight:700;color:{NAVY};flex-shrink:0">03</div>
        <div><div style="font-size:8pt;font-weight:700;color:white">D\u00c9PLOIEMENT</div><div style="font-size:6.5pt;color:{GOLD};opacity:0.8">Plan d'action</div></div>
      </div>
    </div>
    <div style="font-size:6pt;color:rgba(255,255,255,0.3)">decisio.pro \u00b7 contact@decisio.pro</div>
  </div>
  <div style="flex:1;padding:10mm 8mm 10mm 10mm;display:flex;flex-direction:column">
    <div style="align-self:flex-end;background:{NAVY};color:{GOLD};font-size:6pt;font-weight:700;letter-spacing:0.1em;padding:2mm 4mm;border-radius:4px">{mode_c}</div>
    <div style="font-family:Playfair Display,Georgia,serif;font-size:24pt;font-weight:700;color:{NAVY};line-height:1.1;margin-top:14mm">{nom_c}</div>
    <div style="width:18mm;height:2px;background:{GOLD};margin:3mm 0"></div>
    <div style="font-size:12pt;color:#444;font-weight:300">{secteur_c}</div>
    <div style="font-size:8.5pt;color:{MUTED};margin-top:2mm">{date_c}</div>
    <hr style="border:none;border-top:1px solid {BORDER};margin:6mm 0">
    <div style="background:{LIGHT_BG};border:1px solid {BORDER};border-left:3px solid {GOLD};border-radius:6px;padding:5mm 6mm;margin-top:auto">
      <div style="font-size:7pt;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:{NAVY};margin-bottom:2mm">Audit Strat\u00e9gique</div>
      <div style="font-family:Playfair Display,Georgia,serif;font-size:22pt;font-weight:700;color:{NAVY};line-height:1">{price}</div>
      <div style="font-size:7pt;color:{MUTED};margin-top:2mm">Livraison 48h \u00b7 M\u00e9thode D3\u2122 \u00b7 Confidentiel</div>
    </div>
    <div style="font-size:6pt;color:{MUTED};margin-top:6mm;line-height:1.6">
      Ce rapport est strictement confidentiel et destin\u00e9 au seul usage du client d\u00e9sign\u00e9 ci-dessus.
      Toute reproduction est interdite sans autorisation \u00e9crite de DECISIO AGENCY.
    </div>
  </div>
</div>

<!-- ============================== CONTENU ============================== -->
<div>

  <div style="display:flex;justify-content:space-between;border-bottom:1.5px solid {NAVY};padding-bottom:6px;margin-bottom:16px">
    <span style="font-family:Arial,sans-serif;font-size:7pt;font-weight:700;color:{NAVY};letter-spacing:0.06em">DECISIO \u00b7 M\u00c9THODE D3\u2122</span>
    <span style="font-family:Arial,sans-serif;font-size:7pt;color:{MUTED}">{nom_c} \u00b7 {secteur_c}</span>
  </div>

  <div style="font-family:Playfair Display,Georgia,serif;font-size:16pt;font-weight:700;color:{NAVY};text-align:center;line-height:1.25;margin-bottom:8px">
    RAPPORT D'AUDIT STRAT\u00c9GIQUE \u2014 M\u00c9THODE D3\u2122
  </div>
  <div style="font-size:8.5pt;color:{MUTED};text-align:center;margin-bottom:6px">{nom_c} \u00b7 {secteur_c} \u00b7 {date_c}</div>
  <hr style="border:none;border-top:2px solid {NAVY};margin:6px 0 3px">
  <hr style="border:none;border-top:1px solid {GOLD};margin-bottom:24px">

  {content_html}

  <div style="margin-top:30px;padding-top:8px;border-top:2px solid {NAVY};font-size:7.5pt;color:{MUTED};text-align:center;line-height:1.6">
    Rapport strictement confidentiel \u00b7 DECISIO AGENCY \u00b7 M\u00e9thode D3\u2122 \u00b7 contact@decisio.pro
  </div>

</div>

</body>
</html>"""


# =============================================================================
# GENERATION PDF VIA WEASYPRINT
# =============================================================================
def generate_pdf(report_text, nom, secteur, mode, date_str=None):
    """Genere le PDF via WeasyPrint (gratuit, local)"""
    if not date_str:
        date_str = datetime.now().strftime("%d %B %Y")

    html_content = build_html(report_text, nom, secteur, mode, date_str)

    # WeasyPrint genere le PDF directement depuis le HTML
    html_doc = HTML(string=html_content)
    pdf_bytes = html_doc.write_pdf()

    return pdf_bytes
