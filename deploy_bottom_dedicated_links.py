#!/usr/bin/env python3
"""
Añade en la parte final de las páginas principales de Historia (5459), Naturaleza (392),
Cultura (402) y en el cierre de las páginas de colección (21644, 21678, 21690) un
Banner Editorial Destacado hacia su archivo de reportajes respectivo (Reportajes Históricos,
Reportajes de Naturaleza, Personajes y Biografías) acompañado del bloque de las 3 colecciones.
"""

import json
import urllib.request
import sys

BASE_URL = "https://www.lastrasdecuellar.net"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
AUTH_HEADER = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def api_request(url, method="GET", payload=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "LastrasBottomBanners/1.0"
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))


from deploy_cross_navigation_pillars import (
    CROSS_NAV_CSS,
    BRIDGE_HISTORIA_TOP,
    BRIDGE_NATURALEZA_TOP,
    BRIDGE_CULTURA_TOP,
    build_collections_footer_html,
    build_archive_switcher_html
)

BOTTOM_DEDICATED_CSS = """
/* ===================================================================
   BANNER EDITORIAL DE CIERRE HACIA EL ARCHIVO DE REPORTAJES RESPECTIVO
   =================================================================== */
.lastras-bottom-dedicated-cta {
  width: 100%;
  max-width: 1240px;
  margin: 2.5rem auto 1.5rem auto;
  border-radius: 22px;
  padding: 2.4rem 2.6rem;
  background: linear-gradient(135deg, #17211C 0%, #0F1714 100%);
  border: 1px solid rgba(214, 158, 46, 0.45);
  box-shadow: 0 18px 42px rgba(17, 24, 21, 0.16);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
  box-sizing: border-box;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #FFFFFF;
}
.lastras-bottom-dedicated-cta.theme-historia {
  background: linear-gradient(135deg, #231815 0%, #14100E 100%);
  border-color: rgba(184, 74, 40, 0.55);
}
.lastras-bottom-dedicated-cta.theme-naturaleza {
  background: linear-gradient(135deg, #112620 0%, #0B1915 100%);
  border-color: rgba(23, 101, 83, 0.6);
}
.lastras-bottom-dedicated-cta.theme-personajes {
  background: linear-gradient(135deg, #131F3A 0%, #0D1526 100%);
  border-color: rgba(214, 158, 46, 0.5);
}
.lastras-bdc-content {
  flex: 1;
  min-width: 280px;
}
.lastras-bdc-kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: 'Cinzel', serif;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #F6BE28;
  text-transform: uppercase;
  margin-bottom: 0.6rem;
}
.lastras-bdc-title {
  font-family: 'Playfair Display', Georgia, serif !important;
  font-size: 1.85rem !important;
  font-weight: 700 !important;
  color: #FFFFFF !important;
  line-height: 1.22 !important;
  margin: 0 0 0.65rem 0 !important;
}
.lastras-bdc-desc {
  font-size: 0.98rem !important;
  line-height: 1.6 !important;
  color: rgba(255, 255, 255, 0.86) !important;
  margin: 0 !important;
  max-width: 720px;
}
.lastras-bdc-action {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.6rem;
}
.lastras-bdc-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 26px;
  border-radius: 9999px;
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none !important;
  transition: all 0.25s ease;
  white-space: nowrap;
  background: #B84A28;
  color: #FFFFFF !important;
  box-shadow: 0 8px 22px rgba(184, 74, 40, 0.4);
}
.theme-naturaleza .lastras-bdc-btn {
  background: #176553;
  box-shadow: 0 8px 22px rgba(23, 101, 83, 0.45);
}
.theme-personajes .lastras-bdc-btn {
  background: #D69E2E;
  color: #111815 !important;
  box-shadow: 0 8px 22px rgba(214, 158, 46, 0.35);
}
.lastras-bdc-btn:hover {
  transform: translateY(-3px);
  background: #FFFFFF !important;
  color: #111815 !important;
}
@media (max-width: 860px) {
  .lastras-bottom-dedicated-cta {
    padding: 1.65rem 1.35rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  .lastras-bdc-title {
    font-size: 1.45rem !important;
  }
  .lastras-bdc-action {
    width: 100%;
    align-items: stretch;
  }
  .lastras-bdc-btn {
    width: 100%;
    box-sizing: border-box;
  }
}
"""

FULL_CROSS_CSS = CROSS_NAV_CSS + "\n" + BOTTOM_DEDICATED_CSS

BOTTOM_CTA_HISTORIA = """
<div class="lastras-bottom-dedicated-cta theme-historia">
  <div class="lastras-bdc-content">
    <span class="lastras-bdc-kicker">🏛️ HEMEROTECA Y ARCHIVO DOCUMENTAL · 100 ARTÍCULOS</span>
    <h3 class="lastras-bdc-title">¿Quieres profundizar más? Explora los Reportajes Históricos</h3>
    <p class="lastras-bdc-desc">Accede a la colección completa de reportajes históricos de Lastras de Cuéllar: investigaciones sobre el Catastro de Ensenada, las fábricas de luz y resina, los antiguos molinos del Cega, las bodegas centenarias y las actas concejiles.</p>
  </div>
  <div class="lastras-bdc-action">
    <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/reportajes-historicos-de-lastras-de-cuellar/" class="lastras-bdc-btn">
      <span>Ir a Reportajes Históricos (100)</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
    </a>
  </div>
</div>
"""

BOTTOM_CTA_NATURALEZA = """
<div class="lastras-bottom-dedicated-cta theme-naturaleza">
  <div class="lastras-bdc-content">
    <span class="lastras-bdc-kicker">🌲 ARCHIVO AMBIENTAL Y BIODIVERSIDAD · 45 ARTÍCULOS</span>
    <h3 class="lastras-bdc-title">Continúa el recorrido en los Reportajes de Naturaleza</h3>
    <p class="lastras-bdc-desc">Descubre todos nuestros reportajes sobre naturaleza en Lastras de Cuéllar: el curso vivo del río Cega estación a estación, las lagunas del Bodón y humedales ZEPA, la riqueza micológica de los pinares y la fauna ibérica.</p>
  </div>
  <div class="lastras-bdc-action">
    <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/naturaleza/" class="lastras-bdc-btn">
      <span>Ir a Reportajes de Naturaleza (45)</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
    </a>
  </div>
</div>
"""

BOTTOM_CTA_PERSONAJES = """
<div class="lastras-bottom-dedicated-cta theme-personajes">
  <div class="lastras-bdc-content">
    <span class="lastras-bdc-kicker">👥 MEMORIA HUMANA Y BIOGRAFÍAS · 31 SEMBLANZAS</span>
    <h3 class="lastras-bdc-title">Conoce a nuestra gente en Personajes y Biografías</h3>
    <p class="lastras-bdc-desc">Adéntrate en los retratos, entrevistas, oficios tradicionales y semblanzas biográficas de los vecinos, resineros, maestros, cacharreros y mayores que dejaron huella en la historia viva de Lastras de Cuéllar.</p>
  </div>
  <div class="lastras-bdc-action">
    <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/personajes/" class="lastras-bdc-btn">
      <span>Ir a Personajes y Biografías (31)</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
    </a>
  </div>
</div>
"""


# 1. PÁGINA 5459 (HISTORIA PILAR)
print("=== 1. ACTUALIZANDO FINAL DE HISTORIA PILAR (5459) ===")
with open("backup_page_5459_before_crossnav_historia_pilar.json", "r", encoding="utf-8") as f:
    p5459 = json.load(f)
el5459 = json.loads(p5459["meta"]["_elementor_data"])
for root_node in el5459:
    for child in root_node.get("elements", []):
        for w in child.get("elements", []):
            if w.get("id") == "historia_content_html":
                html = w["settings"]["html"]
                html = html.replace(
                    '<!-- NAVEGACIÓN CRONOLÓGICA (TIMELINE QUICK-LINKS) -->',
                    BRIDGE_HISTORIA_TOP + '\n  <!-- NAVEGACIÓN CRONOLÓGICA (TIMELINE QUICK-LINKS) -->'
                )
                html = html.replace(
                    '<div class="historia-cta-box">',
                    BOTTOM_CTA_HISTORIA + "\n" + build_collections_footer_html("historia") + '\n    <div class="historia-cta-box">'
                )
                w["settings"]["html"] = html
            elif w.get("id") == "historia_styles_widget":
                w["settings"]["html"] = w["settings"]["html"].replace("</style>", FULL_CROSS_CSS + "\n</style>")

code, _ = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/5459", method="POST", payload={"meta": {"_elementor_data": json.dumps(el5459, ensure_ascii=False)}})
print(f"5459 HTTP {code}")


# 2. PÁGINA 392 (NATURALEZA PILAR)
print("=== 2. ACTUALIZANDO FINAL DE NATURALEZA PILAR (392) ===")
with open("backup_page_392_before_crossnav_naturaleza_pilar.json", "r", encoding="utf-8") as f:
    p392 = json.load(f)
el392 = json.loads(p392["meta"]["_elementor_data"])
for root_node in el392:
    for child in root_node.get("elements", []):
        for w in child.get("elements", []):
            if w.get("id") == "nat_content_html":
                html = w["settings"]["html"]
                html = html.replace(
                    '<!-- NAVEGACIÓN RÁPIDA POR ECOSISTEMAS -->',
                    BRIDGE_NATURALEZA_TOP + '\n  <!-- NAVEGACIÓN RÁPIDA POR ECOSISTEMAS -->'
                )
                last_div_idx = html.rfind("</div>")
                if last_div_idx != -1:
                    html = html[:last_div_idx] + BOTTOM_CTA_NATURALEZA + "\n" + build_collections_footer_html("naturaleza") + "\n</div>"
                w["settings"]["html"] = html
            elif w.get("id") == "nat_styles_widget":
                w["settings"]["html"] = w["settings"]["html"].replace("</style>", FULL_CROSS_CSS + "\n</style>")

code, _ = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/392", method="POST", payload={"meta": {"_elementor_data": json.dumps(el392, ensure_ascii=False)}})
print(f"392 HTTP {code}")


# 3. PÁGINA 402 (CULTURA PILAR)
print("=== 3. ACTUALIZANDO FINAL DE CULTURA PILAR (402) ===")
with open("backup_page_402_before_crossnav_cultura_pilar.json", "r", encoding="utf-8") as f:
    p402 = json.load(f)
el402 = json.loads(p402["meta"]["_elementor_data"])
for root_node in el402:
    for w in root_node.get("elements", []):
        if w.get("id") == "cul_hero_widget":
            html = w["settings"]["html"]
            html = html.replace("</style>", FULL_CROSS_CSS + "\n</style>", 1)
            html = html.replace(
                '<!-- Sticky Navigation Bar -->',
                BRIDGE_CULTURA_TOP + '\n    <!-- Sticky Navigation Bar -->'
            )
            html = html.replace(
                '<div class="cul-personajes-banner"',
                BOTTOM_CTA_PERSONAJES + "\n" + build_collections_footer_html("personajes") + '\n    <div class="cul-personajes-banner"'
            )
            w["settings"]["html"] = html

code, _ = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/402", method="POST", payload={"meta": {"_elementor_data": json.dumps(el402, ensure_ascii=False)}})
print(f"402 HTTP {code}")


# 4. PÁGINAS DE COLECCIÓN (21644, 21678, 21690): AÑADIR TAMBIÉN EN LA PARTE FINAL EL BLOQUE DE LAS 3 COLECCIONES
print("=== 4. AÑADIENDO NAVEGACIÓN FINAL EN 21644, 21678 Y 21690 ===")

# 4.1: 21644 (Reportajes Históricos)
with open("backup_page_21644_before_crossnav_reportajes_historicos.json", "r", encoding="utf-8") as f:
    p21644 = json.load(f)
el21644 = json.loads(p21644["meta"]["_elementor_data"])
for r in el21644:
    for c in r.get("elements", []):
        for w in c.get("elements", []):
            if w.get("id") == "historia_header_html":
                h = w["settings"]["html"]
                last_div = h.rfind("</div>")
                w["settings"]["html"] = h[:last_div] + build_archive_switcher_html("historia") + "\n</div>"
            elif w.get("id") == "historia_styles_widget":
                w["settings"]["html"] = w["settings"]["html"].replace("</style>", FULL_CROSS_CSS + "\n</style>")
        c["elements"].append({
            "id": "hbotnav1",
            "elType": "widget",
            "widgetType": "html",
            "settings": {
                "_title": "Navegación Final a Colecciones y Reportajes",
                "html": build_collections_footer_html("historia")
            },
            "elements": []
        })

code, _ = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/21644", method="POST", payload={"meta": {"_elementor_data": json.dumps(el21644, ensure_ascii=False)}})
print(f"21644 HTTP {code}")

# 4.2: 21678 (Reportajes Naturaleza)
with open("backup_page_21678_before_crossnav_reportajes_naturaleza.json", "r", encoding="utf-8") as f:
    p21678 = json.load(f)
el21678 = json.loads(p21678["meta"]["_elementor_data"])
for r in el21678:
    for c in r.get("elements", []):
        for w in c.get("elements", []):
            if w.get("id") == "naturaleza_header_html":
                h = w["settings"]["html"]
                last_div = h.rfind("</div>")
                w["settings"]["html"] = h[:last_div] + build_archive_switcher_html("naturaleza") + "\n</div>"
            elif w.get("id") == "naturaleza_styles_widget":
                w["settings"]["html"] = w["settings"]["html"].replace("</style>", FULL_CROSS_CSS + "\n</style>")
        c["elements"].append({
            "id": "nbotnav1",
            "elType": "widget",
            "widgetType": "html",
            "settings": {
                "_title": "Navegación Final a Colecciones y Reportajes",
                "html": build_collections_footer_html("naturaleza")
            },
            "elements": []
        })

code, _ = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/21678", method="POST", payload={"meta": {"_elementor_data": json.dumps(el21678, ensure_ascii=False)}})
print(f"21678 HTTP {code}")

# 4.3: 21690 (Personajes)
with open("backup_page_21690_before_crossnav_personajes.json", "r", encoding="utf-8") as f:
    p21690 = json.load(f)
el21690 = json.loads(p21690["meta"]["_elementor_data"])
for r in el21690:
    for c in r.get("elements", []):
        if c.get("id") == "27d046fd":
            c["elements"].append({
                "id": "persnav1",
                "elType": "widget",
                "widgetType": "html",
                "settings": {
                    "_title": "Conmutador de Colecciones en Personajes",
                    "html": build_archive_switcher_html("personajes")
                },
                "elements": []
            })
    r["elements"].append({
        "id": "pbotnav1",
        "elType": "widget",
        "widgetType": "html",
        "settings": {
            "_title": "Navegación Final de Personajes hacia Reportajes",
            "html": f"<style>{FULL_CROSS_CSS}</style>\n" + build_collections_footer_html("personajes")
        },
        "elements": []
    })

code, _ = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/21690", method="POST", payload={"meta": {"_elementor_data": json.dumps(el21690, ensure_ascii=False)}})
print(f"21690 HTTP {code}")
