#!/usr/bin/env python3
"""
Despliegue de Accesos Directos y Navegación Cruzada para los Reportajes de
Historia, Naturaleza y Personajes dentro de sus páginas pilar y sus archivos monográficos:
- 5459: Historia de Lastras de Cuéllar (Pilar) -> acceso directo arriba y al final a Reportajes Históricos + Trilogía/Colecciones
- 392: Naturaleza y Entorno (Pilar) -> acceso directo arriba y al final a Reportajes de Naturaleza + Trilogía/Colecciones
- 402: Cultura y Tradiciones (Pilar) -> acceso directo arriba y al final a Personajes, Historia y Naturaleza
- 21644: Reportajes Históricos -> conmutador de las 3 colecciones + enlace a Historia Pilar
- 21678: Reportajes de Naturaleza -> conmutador de las 3 colecciones + enlace a Naturaleza Pilar
- 21690: Personajes y Oficios -> conmutador de las 3 colecciones + enlace a Cultura Pilar
- 26507: Inicio Compacto (Prueba) -> refuerzo visual de las 3 colecciones en la barra Quick-Nav bajo el Hero
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
        "User-Agent": "LastrasCrossNavDeployer/1.0"
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))


# CSS compartido para los bloques de acceso directo y navegación cruzada
CROSS_NAV_CSS = """
/* ===================================================================
   NAVEGACIÓN CRUZADA DE COLECCIONES (HISTORIA, NATURALEZA, PERSONAJES)
   =================================================================== */
.lastras-hub-bridge-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.25rem;
  background: linear-gradient(135deg, #17211C 0%, #111815 100%);
  color: #FFFFFF;
  border: 1px solid rgba(214, 158, 46, 0.38);
  border-radius: 16px;
  padding: 1.15rem 1.5rem;
  margin: 0 auto 1.8rem auto;
  max-width: 1240px;
  box-shadow: 0 10px 28px rgba(17, 24, 21, 0.12);
  flex-wrap: wrap;
  box-sizing: border-box;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}
.lastras-hub-bridge-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 260px;
}
.lastras-hub-bridge-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(214, 158, 46, 0.16);
  border: 1px solid rgba(214, 158, 46, 0.4);
  font-size: 1.3rem;
  flex-shrink: 0;
}
.lastras-hub-bridge-text h3 {
  font-family: 'Playfair Display', Georgia, serif !important;
  font-size: 1.18rem !important;
  font-weight: 700 !important;
  color: #FFFFFF !important;
  margin: 0 0 0.2rem 0 !important;
  line-height: 1.25 !important;
}
.lastras-hub-bridge-text p {
  font-size: 0.88rem !important;
  color: rgba(255, 255, 255, 0.82) !important;
  margin: 0 !important;
  line-height: 1.45 !important;
}
.lastras-hub-bridge-actions {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-wrap: wrap;
}
.lastras-hub-btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #B84A28;
  color: #FFFFFF !important;
  font-size: 0.86rem;
  font-weight: 700;
  padding: 10px 18px;
  border-radius: 9999px;
  text-decoration: none !important;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(184, 74, 40, 0.35);
  white-space: nowrap;
}
.lastras-hub-btn-primary:hover {
  background: #D69E2E;
  color: #111815 !important;
  transform: translateY(-2px);
}
.lastras-hub-btn-primary.forest-theme {
  background: #176553;
  box-shadow: 0 4px 14px rgba(23, 101, 83, 0.35);
}
.lastras-hub-btn-primary.forest-theme:hover {
  background: #D69E2E;
  color: #111815 !important;
}
.lastras-hub-btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.22);
  color: #F8FAFC !important;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 9px 15px;
  border-radius: 9999px;
  text-decoration: none !important;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.lastras-hub-btn-secondary:hover {
  background: #FFFFFF;
  color: #111815 !important;
}

/* Bloque Inferior de 3 Colecciones (Cross-Nav Footer Card) */
.lastras-collections-crossnav {
  width: 100%;
  max-width: 1240px;
  margin: 2.8rem auto 1rem auto;
  background: #FAF7F2;
  border: 1px solid rgba(17, 24, 21, 0.1);
  border-radius: 20px;
  padding: 2rem 2rem;
  box-sizing: border-box;
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.lastras-collections-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}
.lastras-collections-kicker {
  font-family: 'Cinzel', serif;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #B84A28;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.25rem;
}
.lastras-collections-title {
  font-family: 'Playfair Display', Georgia, serif !important;
  font-size: 1.55rem !important;
  font-weight: 700 !important;
  color: #111815 !important;
  margin: 0 !important;
}
.lastras-collections-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.15rem;
}
.lastras-col-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #FFFFFF;
  border: 1px solid rgba(17, 24, 21, 0.08);
  border-radius: 14px;
  padding: 1.35rem 1.35rem;
  text-decoration: none !important;
  transition: all 0.25s ease;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
}
.lastras-col-card:hover {
  transform: translateY(-4px);
  border-color: rgba(184, 74, 40, 0.4);
  box-shadow: 0 12px 26px rgba(17, 24, 21, 0.08);
}
.lastras-col-card.is-active-col {
  border: 2px solid #B84A28;
  background: #FFFDF9;
}
.lastras-col-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 10px;
  border-radius: 9999px;
  width: fit-content;
  margin-bottom: 0.65rem;
}
.lastras-col-pill.hist { background: rgba(184, 74, 40, 0.12); color: #B84A28; }
.lastras-col-pill.nat { background: rgba(23, 101, 83, 0.12); color: #176553; }
.lastras-col-pill.pers { background: rgba(30, 58, 138, 0.12); color: #1E3A8A; }
.lastras-col-card h4 {
  font-family: 'Playfair Display', Georgia, serif !important;
  font-size: 1.18rem !important;
  font-weight: 700 !important;
  color: #151C22 !important;
  margin: 0 0 0.45rem 0 !important;
  line-height: 1.3 !important;
}
.lastras-col-card p {
  font-size: 0.86rem !important;
  color: #4A5568 !important;
  line-height: 1.5 !important;
  margin: 0 0 0.9rem 0 !important;
}
.lastras-col-link {
  font-size: 0.83rem;
  font-weight: 700;
  color: #B84A28;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

@media (max-width: 860px) {
  .lastras-hub-bridge-bar {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.1rem 1.15rem;
  }
  .lastras-hub-bridge-actions {
    width: 100%;
  }
  .lastras-hub-btn-primary, .lastras-hub-btn-secondary {
    flex: 1;
    justify-content: center;
    text-align: center;
  }
  .lastras-collections-grid {
    grid-template-columns: 1fr;
  }
  .lastras-collections-crossnav {
    padding: 1.4rem 1.15rem;
  }
}
"""


def build_collections_footer_html(active_key=""):
    hist_cls = "lastras-col-card is-active-col" if active_key == "historia" else "lastras-col-card"
    nat_cls = "lastras-col-card is-active-col" if active_key == "naturaleza" else "lastras-col-card"
    pers_cls = "lastras-col-card is-active-col" if active_key == "personajes" else "lastras-col-card"
    return f"""
<aside class="lastras-collections-crossnav" aria-label="Explorar las tres colecciones de reportajes">
  <div class="lastras-collections-head">
    <div>
      <span class="lastras-collections-kicker">HEMEROTECA Y ARCHIVO VIVO DE LASTRAS DE CUÉLLAR</span>
      <h3 class="lastras-collections-title">Explora las Tres Colecciones de Reportajes</h3>
    </div>
    <a href="https://www.lastrasdecuellar.net/reportajes-especiales/" style="font-size:0.86rem;font-weight:700;color:#B84A28;text-decoration:none;">Ver los 22 Monográficos Especiales →</a>
  </div>
  <div class="lastras-collections-grid">
    <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/reportajes-historicos-de-lastras-de-cuellar/" class="{hist_cls}">
      <div>
        <span class="lastras-col-pill hist">🏛️ 100 Crónicas y Artículos</span>
        <h4>Reportajes de Historia y Patrimonio</h4>
        <p>Investigaciones documentales, Catastro de Ensenada, molinos, bodegas, luz eléctrica y memoria de los siglos.</p>
      </div>
      <span class="lastras-col-link">Abrir colección de Historia →</span>
    </a>
    <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/naturaleza/" class="{nat_cls}">
      <div>
        <span class="lastras-col-pill nat">🌲 45 Reportajes y Rutas</span>
        <h4>Reportajes de Naturaleza y Entorno</h4>
        <p>El curso vivo del río Cega, las lagunas y humedales ZEPA, los pinares resineros, micología y fauna salvaje.</p>
      </div>
      <span class="lastras-col-link" style="color:#176553;">Abrir colección de Naturaleza →</span>
    </a>
    <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/personajes/" class="{pers_cls}">
      <div>
        <span class="lastras-col-pill pers">👥 31 Semblanzas y Biografías</span>
        <h4>Personajes, Paisanos y Oficios</h4>
        <p>Homenaje a los mayores, maestros, resineros, cacharreros y vecinos que forjaron la identidad de nuestro pueblo.</p>
      </div>
      <span class="lastras-col-link" style="color:#1E3A8A;">Abrir colección de Personajes →</span>
    </a>
  </div>
</aside>
"""


# ==============================================================================
# 1. ACTUALIZAR PÁGINA PILAR DE HISTORIA (5459)
# ==============================================================================
print("=== 1. ACTUALIZANDO PÁGINA PILAR HISTORIA (5459) ===")
with open("backup_page_5459_before_crossnav_historia_pilar.json", "r", encoding="utf-8") as f:
    p5459 = json.load(f)
el5459 = json.loads(p5459["meta"]["_elementor_data"])

BRIDGE_HISTORIA_TOP = """
  <!-- ACCESO DIRECTO A LA COLECCIÓN DE 100 REPORTAJES HISTÓRICOS -->
  <div class="lastras-hub-bridge-bar">
    <div class="lastras-hub-bridge-info">
      <div class="lastras-hub-bridge-badge">📜</div>
      <div class="lastras-hub-bridge-text">
        <h3>Hemeroteca Histórica: 100 Reportajes y Crónicas Documentales</h3>
        <p>Además de esta síntesis histórica, explora todos los artículos a fondo sobre linajes, molinos, bodegas, el Catastro de Ensenada y nuestros antepasados.</p>
      </div>
    </div>
    <div class="lastras-hub-bridge-actions">
      <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/reportajes-historicos-de-lastras-de-cuellar/" class="lastras-hub-btn-primary">
        <span>Explorar los 100 Reportajes Históricos →</span>
      </a>
      <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/personajes/" class="lastras-hub-btn-secondary">
        <span>👥 Ver Personajes y Biografías</span>
      </a>
    </div>
  </div>
"""

for root_node in el5459:
    for child in root_node.get("elements", []):
        for w in child.get("elements", []):
            if w.get("id") == "historia_content_html":
                html = w["settings"]["html"]
                if "lastras-hub-bridge-bar" not in html:
                    html = html.replace(
                        '<!-- NAVEGACIÓN CRONOLÓGICA (TIMELINE QUICK-LINKS) -->',
                        BRIDGE_HISTORIA_TOP + '\n  <!-- NAVEGACIÓN CRONOLÓGICA (TIMELINE QUICK-LINKS) -->'
                    )
                if "lastras-collections-crossnav" not in html:
                    html = html.replace(
                        '<div class="historia-cta-box">',
                        build_collections_footer_html("historia") + '\n    <div class="historia-cta-box">'
                    )
                w["settings"]["html"] = html
            elif w.get("id") == "historia_styles_widget":
                css = w["settings"]["html"]
                if "lastras-hub-bridge-bar" not in css:
                    w["settings"]["html"] = css.replace("</style>", CROSS_NAV_CSS + "\n</style>")

code, _ = api_request(
    f"{BASE_URL}/wp-json/wp/v2/pages/5459",
    method="POST",
    payload={"meta": {"_elementor_data": json.dumps(el5459, ensure_ascii=False)}}
)
print(f"Página 5459 actualizada: HTTP {code}")


# ==============================================================================
# 2. ACTUALIZAR PÁGINA PILAR DE NATURALEZA (392)
# ==============================================================================
print("=== 2. ACTUALIZANDO PÁGINA PILAR NATURALEZA (392) ===")
with open("backup_page_392_before_crossnav_naturaleza_pilar.json", "r", encoding="utf-8") as f:
    p392 = json.load(f)
el392 = json.loads(p392["meta"]["_elementor_data"])

BRIDGE_NATURALEZA_TOP = """
  <!-- ACCESO DIRECTO A LA COLECCIÓN DE 45 REPORTAJES DE NATURALEZA -->
  <div class="lastras-hub-bridge-bar">
    <div class="lastras-hub-bridge-info">
      <div class="lastras-hub-bridge-badge">🌲</div>
      <div class="lastras-hub-bridge-text">
        <h3>Archivo Natural: 45 Reportajes sobre el Río Cega, Lagunas y Pinares</h3>
        <p>Accede a todas las crónicas ambientales, rutas fluviales, estudios ornitológicos de los humedales ZEPA y defensa de nuestros acuíferos.</p>
      </div>
    </div>
    <div class="lastras-hub-bridge-actions">
      <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/naturaleza/" class="lastras-hub-btn-primary forest-theme">
        <span>Explorar los 45 Reportajes de Naturaleza →</span>
      </a>
      <a href="https://www.lastrasdecuellar.net/reportajes-especiales/lagunas-de-lastras-de-cuellar/" class="lastras-hub-btn-secondary">
        <span>🦆 Especial Lagunas</span>
      </a>
    </div>
  </div>
"""

for root_node in el392:
    for child in root_node.get("elements", []):
        for w in child.get("elements", []):
            if w.get("id") == "nat_content_html":
                html = w["settings"]["html"]
                if "lastras-hub-bridge-bar" not in html:
                    html = html.replace(
                        '<!-- NAVEGACIÓN RÁPIDA POR ECOSISTEMAS -->',
                        BRIDGE_NATURALEZA_TOP + '\n  <!-- NAVEGACIÓN RÁPIDA POR ECOSISTEMAS -->'
                    )
                if "lastras-collections-crossnav" not in html:
                    # Insertar justo antes del cierre de .naturaleza-wrapper
                    last_div_idx = html.rfind("</div>")
                    if last_div_idx != -1:
                        html = html[:last_div_idx] + build_collections_footer_html("naturaleza") + "\n</div>"
                w["settings"]["html"] = html
            elif w.get("id") == "nat_styles_widget":
                css = w["settings"]["html"]
                if "lastras-hub-bridge-bar" not in css:
                    w["settings"]["html"] = css.replace("</style>", CROSS_NAV_CSS + "\n</style>")

code, _ = api_request(
    f"{BASE_URL}/wp-json/wp/v2/pages/392",
    method="POST",
    payload={"meta": {"_elementor_data": json.dumps(el392, ensure_ascii=False)}}
)
print(f"Página 392 actualizada: HTTP {code}")


# ==============================================================================
# 3. ACTUALIZAR PÁGINA PILAR DE CULTURA Y TRADICIONES (402)
# ==============================================================================
print("=== 3. ACTUALIZANDO PÁGINA PILAR CULTURA (402) ===")
with open("backup_page_402_before_crossnav_cultura_pilar.json", "r", encoding="utf-8") as f:
    p402 = json.load(f)
el402 = json.loads(p402["meta"]["_elementor_data"])

BRIDGE_CULTURA_TOP = """
    <!-- ACCESO DIRECTO A PERSONAJES Y COLECCIONES ETNOGRÁFICAS -->
    <div class="lastras-hub-bridge-bar" style="margin-top: 1.5rem;">
      <div class="lastras-hub-bridge-info">
        <div class="lastras-hub-bridge-badge">👥</div>
        <div class="lastras-hub-bridge-text">
          <h3>Memoria Humana y Etnografía: Personajes, Oficios y Tradiciones</h3>
          <p>Conoce las biografías de nuestros paisanos ilustres, maestros, resineros y alfareros, o explora las crónicas históricas del pueblo.</p>
        </div>
      </div>
      <div class="lastras-hub-bridge-actions">
        <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/personajes/" class="lastras-hub-btn-primary">
          <span>👥 Explorar Personajes de Lastras (31) →</span>
        </a>
        <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/reportajes-historicos-de-lastras-de-cuellar/" class="lastras-hub-btn-secondary">
          <span>🏛️ Reportajes Históricos</span>
        </a>
      </div>
    </div>
"""

for root_node in el402:
    for w in root_node.get("elements", []):
        if w.get("id") == "cul_hero_widget":
            html = w["settings"]["html"]
            if "lastras-hub-bridge-bar" not in html:
                html = html.replace("</style>", CROSS_NAV_CSS + "\n</style>", 1)
                html = html.replace(
                    '<!-- Ficha AEO de Datos Clave Culturales -->',
                    BRIDGE_CULTURA_TOP + '\n    <!-- Ficha AEO de Datos Clave Culturales -->'
                )
            if "lastras-collections-crossnav" not in html:
                html = html.replace(
                    '<!-- SECCIÓN 06: Conexión con Personajes Ilustres -->',
                    build_collections_footer_html("personajes") + '\n    <!-- SECCIÓN 06: Conexión con Personajes Ilustres -->'
                )
            w["settings"]["html"] = html

code, _ = api_request(
    f"{BASE_URL}/wp-json/wp/v2/pages/402",
    method="POST",
    payload={"meta": {"_elementor_data": json.dumps(el402, ensure_ascii=False)}}
)
print(f"Página 402 actualizada: HTTP {code}")


# ==============================================================================
# 4. ACTUALIZAR ARCHIVOS MONOGRÁFICOS: HISTORIA (21644), NATURALEZA (21678), PERSONAJES (21690)
# ==============================================================================
print("=== 4. ACTUALIZANDO PÁGINAS DE COLECCIÓN (21644, 21678, 21690) ===")


def build_archive_switcher_html(current_tab):
    tabs = [
        ("historia", "🏛️ Reportajes Históricos (100)", "https://www.lastrasdecuellar.net/lastras-de-cuellar/reportajes-historicos-de-lastras-de-cuellar/"),
        ("naturaleza", "🌲 Reportajes de Naturaleza (45)", "https://www.lastrasdecuellar.net/lastras-de-cuellar/naturaleza/"),
        ("personajes", "👥 Personajes y Biografías (31)", "https://www.lastrasdecuellar.net/lastras-de-cuellar/personajes/"),
    ]
    pills_html = ""
    for key, label, url in tabs:
        if key == current_tab:
            pills_html += f'<a href="{url}" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:9999px;background:#151C22;color:#FFFFFF !important;font-size:0.84rem;font-weight:700;text-decoration:none !important;box-shadow:0 4px 12px rgba(0,0,0,0.12);">{label}</a>'
        else:
            pills_html += f'<a href="{url}" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:9999px;background:#FFFFFF;color:#151C22 !important;border:1px solid rgba(21,28,34,0.14);font-size:0.84rem;font-weight:600;text-decoration:none !important;">{label}</a>'

    pilar_links = {
        "historia": ("📖 Leer Síntesis Histórica de Lastras (s. XII–XX) →", "https://www.lastrasdecuellar.net/lastras-de-cuellar/historia-de-lastras-de-cuellar/"),
        "naturaleza": ("🌿 Ver Guía de Ecosistemas (Pinares, Lagunas y Cega) →", "https://www.lastrasdecuellar.net/lastras-de-cuellar/lastras-de-cuellar-y-su-entorno/"),
        "personajes": ("🎭 Ir a Cultura, Fiestas y Tradiciones →", "https://www.lastrasdecuellar.net/lastras-de-cuellar/cultura-y-tradicion/"),
    }
    p_label, p_url = pilar_links[current_tab]

    return f"""
<div class="lastras-archive-switcher" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.85rem;margin-top:1.35rem;padding-top:1.15rem;border-top:1px solid rgba(21,28,34,0.08);font-family:'Plus Jakarta Sans',sans-serif;">
  <div style="display:flex;align-items:center;gap:0.55rem;flex-wrap:wrap;">
    <span style="font-size:0.76rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#64748B;margin-right:4px;">Colecciones:</span>
    {pills_html}
  </div>
  <a href="{p_url}" style="font-size:0.85rem;font-weight:700;color:#B84A28 !important;text-decoration:none !important;">{p_label}</a>
</div>
"""


# 4.1: 21644 (Reportajes Históricos)
with open("backup_page_21644_before_crossnav_reportajes_historicos.json", "r", encoding="utf-8") as f:
    p21644 = json.load(f)
el21644 = json.loads(p21644["meta"]["_elementor_data"])
for r in el21644:
    for c in r.get("elements", []):
        for w in c.get("elements", []):
            if w.get("id") == "historia_header_html":
                h = w["settings"]["html"]
                if "lastras-archive-switcher" not in h:
                    last_div = h.rfind("</div>")
                    w["settings"]["html"] = h[:last_div] + build_archive_switcher_html("historia") + "\n</div>"

code, _ = api_request(
    f"{BASE_URL}/wp-json/wp/v2/pages/21644",
    method="POST",
    payload={"meta": {"_elementor_data": json.dumps(el21644, ensure_ascii=False)}}
)
print(f"Página 21644 actualizada: HTTP {code}")

# 4.2: 21678 (Reportajes Naturaleza)
with open("backup_page_21678_before_crossnav_reportajes_naturaleza.json", "r", encoding="utf-8") as f:
    p21678 = json.load(f)
el21678 = json.loads(p21678["meta"]["_elementor_data"])
for r in el21678:
    for c in r.get("elements", []):
        for w in c.get("elements", []):
            if w.get("id") == "naturaleza_header_html":
                h = w["settings"]["html"]
                if "lastras-archive-switcher" not in h:
                    last_div = h.rfind("</div>")
                    w["settings"]["html"] = h[:last_div] + build_archive_switcher_html("naturaleza") + "\n</div>"

code, _ = api_request(
    f"{BASE_URL}/wp-json/wp/v2/pages/21678",
    method="POST",
    payload={"meta": {"_elementor_data": json.dumps(el21678, ensure_ascii=False)}}
)
print(f"Página 21678 actualizada: HTTP {code}")

# 4.3: 21690 (Personajes)
with open("backup_page_21690_before_crossnav_personajes.json", "r", encoding="utf-8") as f:
    p21690 = json.load(f)
el21690 = json.loads(p21690["meta"]["_elementor_data"])
# Insertar un widget HTML con el conmutador de colecciones dentro de 27d046fd (cabecera de Personajes)
for r in el21690:
    for c in r.get("elements", []):
        if c.get("id") == "27d046fd":
            existing_ids = [x.get("id") for x in c.get("elements", [])]
            switcher_widget = {
                "id": "persnav1",
                "elType": "widget",
                "widgetType": "html",
                "settings": {
                    "_title": "Conmutador de Colecciones en Personajes",
                    "html": build_archive_switcher_html("personajes")
                },
                "elements": []
            }
            if "persnav1" not in existing_ids:
                c["elements"].append(switcher_widget)
            else:
                for idx, x in enumerate(c["elements"]):
                    if x.get("id") == "persnav1":
                        c["elements"][idx] = switcher_widget

code, _ = api_request(
    f"{BASE_URL}/wp-json/wp/v2/pages/21690",
    method="POST",
    payload={"meta": {"_elementor_data": json.dumps(el21690, ensure_ascii=False)}}
)
print(f"Página 21690 actualizada: HTTP {code}")
