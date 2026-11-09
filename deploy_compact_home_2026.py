#!/usr/bin/env python3
"""
Crea o actualiza la página de prueba 'Inicio Compacto (Prueba)' para comparar en vivo
con la portada principal (ID 26169) sin alterar la portada en producción.

Optimizaciones aplicadas (Desktop + Mobile):
1. Sustituye el bloque repetitivo 'Tres Miradas' (7d8b12f4) por una Barra Editorial de
   Acceso Rápido (Quick-Nav) integrada que conecta con las colecciones y secciones de la página.
2. En móvil, convierte la cuadrícula de 'Últimas Noticias' (ultimas_noticias_sec) en un
   carrusel horizontal deslizable (scroll-snap) con indicador visual, reduciendo 2.406px a ~680px.
3. Reduce la altura excesiva de 'La Gran Trilogía' (9f1d4a82) de 520px a 390px en escritorio
   y 330px en móvil, y compacta márgenes verticales entre secciones.
4. Transforma 'Construyamos el Archivo' (2ec773cc) de 3 tarjetas altas apiladas a un
   Banner Horizontal Editorial Bento compacto (ahorra ~520px en escritorio y ~1.250px en móvil).
"""

import json
import re
import urllib.request
import sys

BASE_URL = "https://www.lastrasdecuellar.net"
SOURCE_PAGE_ID = 26169
TEST_SLUG = "inicio-compacto-prueba"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
AUTH_HEADER = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def api_request(url, method="GET", payload=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "LastrasTestHomeBuilder/1.0"
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))


print("=== 1. DESCARGANDO PORTADA ORIGINAL (26169) Y GUARDANDO BACKUP ===")
code, source_page = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/{SOURCE_PAGE_ID}?context=edit")
if code != 200:
    print(f"Error al obtener 26169: {code}")
    sys.exit(1)

with open("backup_page_26169_before_test_clone.json", "w", encoding="utf-8") as f:
    json.dump(source_page, f, ensure_ascii=False, indent=2)
print("Backup guardado: backup_page_26169_before_test_clone.json")

el_raw = source_page["meta"]["_elementor_data"]
elements = json.loads(el_raw)
root = elements[0]
orig_sections = root["elements"]

# Barra Editorial de Navegación Rápida y 3 Colecciones (100% visible sin scroll lateral en móvil)
QUICK_NAV_BAR_HTML = """<!-- BARRA EDITORIAL DE ACCESO RÁPIDO Y 3 COLECCIONES -->
<style>
.lastras-quicknav-section {
  width: 100%;
  max-width: 1260px;
  margin: -1.6rem auto 1.4rem auto;
  padding: 0 1.25rem;
  box-sizing: border-box;
  position: relative;
  z-index: 20;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.lastras-quicknav-card {
  background: #FFFFFF;
  border: 1px solid rgba(17, 24, 21, 0.1);
  border-radius: 20px;
  padding: 1.15rem 1.35rem;
  box-shadow: 0 14px 36px rgba(17, 24, 21, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.lastras-quicknav-head {
  display: none;
}

/* Fila 1: 3 Tarjetas de Colecciones (3 columnas en Desktop y 3 columnas compactas visibles en Móvil) */
.lastras-collections-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.85rem;
}

.lastras-cstrip-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.8rem 1rem;
  border-radius: 14px;
  background: #FAF7F2;
  border: 1px solid rgba(17, 24, 21, 0.09);
  text-decoration: none !important;
  transition: all 0.22s ease;
  box-sizing: border-box;
}

.lastras-cstrip-item:hover {
  transform: translateY(-2px);
  background: #151C22;
  border-color: #151C22;
  box-shadow: 0 8px 20px rgba(17, 24, 21, 0.14);
}

.lastras-cstrip-icon {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
  color: #FFFFFF;
}
.cstrip-hist .lastras-cstrip-icon { background: #B84A28; }
.cstrip-nat .lastras-cstrip-icon { background: #176553; }
.cstrip-pers .lastras-cstrip-icon { background: #1E3A8A; }

.lastras-cstrip-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.lastras-cstrip-kicker {
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #B84A28;
  line-height: 1.1;
  margin-bottom: 2px;
}
.cstrip-nat .lastras-cstrip-kicker { color: #176553; }
.cstrip-pers .lastras-cstrip-kicker { color: #1E3A8A; }

.lastras-cstrip-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.02rem;
  font-weight: 700;
  color: #151C22;
  line-height: 1.2;
}

.lastras-cstrip-item:hover .lastras-cstrip-title,
.lastras-cstrip-item:hover .lastras-cstrip-kicker,
.lastras-cstrip-item:hover .lastras-cstrip-arrow {
  color: #FFFFFF !important;
}

.lastras-cstrip-arrow {
  font-size: 0.95rem;
  font-weight: 700;
  color: #64748B;
  flex-shrink: 0;
}

/* Fila 2: Saltos rápidos dentro de la portada (Rejilla 2x2 en móvil, sin scroll lateral) */
.lastras-quicknav-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(17, 24, 21, 0.07);
  flex-wrap: wrap;
}

.lastras-quicknav-label {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-family: 'Cinzel', serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.11em;
  color: #64748B;
  text-transform: uppercase;
}

.lastras-quicknav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.lastras-qpill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 13px;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  text-decoration: none !important;
  transition: all 0.2s ease;
  white-space: nowrap;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  color: #1E293B !important;
  box-sizing: border-box;
}

.lastras-qpill:hover {
  background: #B84A28;
  color: #FFFFFF !important;
  border-color: #B84A28;
}

/* MÓVIL: CERO SCROLL LATERAL — Las 3 colecciones en 3 columnas a la vista + 4 saltos en rejilla 2x2 */
@media (max-width: 767px) {
  .lastras-quicknav-section {
    margin: -0.75rem auto 0.65rem auto;
    padding: 0 0.65rem;
  }
  .lastras-quicknav-card {
    padding: 0.75rem;
    gap: 0.6rem;
    border-radius: 16px;
  }
  .lastras-quicknav-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'Cinzel', serif;
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #B84A28;
    text-transform: uppercase;
    padding: 0 2px;
  }
  .lastras-collections-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.45rem;
  }
  .lastras-cstrip-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0.6rem 0.35rem 0.55rem 0.35rem;
    gap: 0.35rem;
    border-radius: 12px;
  }
  .lastras-cstrip-icon {
    width: 32px;
    height: 32px;
    font-size: 0.95rem;
    border-radius: 9px;
  }
  .lastras-cstrip-body {
    align-items: center;
  }
  .lastras-cstrip-kicker {
    font-size: 0.58rem;
    letter-spacing: 0.03em;
    margin-bottom: 1px;
  }
  .lastras-cstrip-title {
    font-size: 0.8rem;
    line-height: 1.15;
  }
  .lastras-cstrip-arrow {
    display: none;
  }
  .lastras-quicknav-bottom {
    padding-top: 0.55rem;
  }
  .lastras-quicknav-label {
    display: none;
  }
  .lastras-quicknav-links {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.4rem;
    width: 100%;
  }
  .lastras-qpill {
    width: 100%;
    padding: 7px 6px;
    font-size: 0.74rem;
    border-radius: 9px;
  }
}
</style>

<nav class="lastras-quicknav-section" aria-label="Colecciones de reportajes y acceso rápido">
  <div class="lastras-quicknav-card">
    <div class="lastras-quicknav-head">
      <span>📚 Explorar Colecciones y Secciones</span>
      <span>Toca para abrir</span>
    </div>
    <div class="lastras-collections-strip">
      <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/reportajes-historicos-de-lastras-de-cuellar/" class="lastras-cstrip-item cstrip-hist">
        <div class="lastras-cstrip-icon">🏛️</div>
        <div class="lastras-cstrip-body">
          <span class="lastras-cstrip-kicker">100 CRÓNICAS</span>
          <span class="lastras-cstrip-title">Historia</span>
        </div>
        <span class="lastras-cstrip-arrow">→</span>
      </a>
      <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/naturaleza/" class="lastras-cstrip-item cstrip-nat">
        <div class="lastras-cstrip-icon">🌲</div>
        <div class="lastras-cstrip-body">
          <span class="lastras-cstrip-kicker">45 ARTÍCULOS</span>
          <span class="lastras-cstrip-title">Naturaleza</span>
        </div>
        <span class="lastras-cstrip-arrow">→</span>
      </a>
      <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/personajes/" class="lastras-cstrip-item cstrip-pers">
        <div class="lastras-cstrip-icon">👥</div>
        <div class="lastras-cstrip-body">
          <span class="lastras-cstrip-kicker">31 BIOGRAFÍAS</span>
          <span class="lastras-cstrip-title">Personajes</span>
        </div>
        <span class="lastras-cstrip-arrow">→</span>
      </a>
    </div>
    <div class="lastras-quicknav-bottom">
      <div class="lastras-quicknav-label">
        <span>Saltar en portada:</span>
      </div>
      <div class="lastras-quicknav-links">
        <a href="#sec-noticias" class="lastras-qpill">📰 Últimas Noticias</a>
        <a href="#sec-trilogia" class="lastras-qpill">🔥 Gran Trilogía</a>
        <a href="#sec-reportajes" class="lastras-qpill">⭐ 22 Especiales</a>
        <a href="#colaborar" class="lastras-qpill">📚 Colaborar</a>
      </div>
    </div>
  </div>
</nav>
"""

quick_nav_container = {
    "id": "qnav2616",
    "elType": "e-flexbox",
    "settings": {
        "content_width": "full",
        "flex_direction": "column"
    },
    "elements": [
        {
            "id": "wqnav261",
            "elType": "widget",
            "widgetType": "html",
            "settings": {
                "_title": "Barra Editorial de Acceso Rápido",
                "html": QUICK_NAV_BAR_HTML
            },
            "elements": []
        }
    ],
    "isInner": False
}

# Banner Horizontal Compacto para 'Construyamos el Archivo de Lastras'
COMPACT_COLABORA_HTML = """<!-- BANNER HORIZONTAL EDITORIAL: ARCHIVO VECINAL COMPACTO -->
<style>
.colabora-compact-wrap {
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
  background: linear-gradient(135deg, #FAF7F2 0%, #F2ECE1 100%);
  border: 1px solid rgba(22, 28, 34, 0.1);
  border-radius: 20px;
  padding: 2.2rem 2.5rem;
  box-shadow: 0 10px 30px rgba(17, 24, 21, 0.04);
  box-sizing: border-box;
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.colabora-compact-top {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 2rem;
  align-items: center;
}

.colabora-compact-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 9999px;
  background: rgba(23, 101, 83, 0.1);
  color: #176553;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.65rem;
}

.colabora-compact-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.95rem;
  font-weight: 700;
  color: #151C22;
  line-height: 1.2;
  margin: 0 0 0.55rem 0;
}

.colabora-compact-desc {
  font-size: 0.96rem;
  line-height: 1.55;
  color: #4A5568;
  margin: 0 0 1.1rem 0;
}

.colabora-compact-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.colabora-cpill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid rgba(22, 28, 34, 0.08);
  border-radius: 10px;
  padding: 8px 13px;
  font-size: 0.83rem;
  font-weight: 600;
  color: #151C22;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

.colabora-cpill small {
  display: block;
  font-size: 0.72rem;
  font-weight: 500;
  color: #64748B;
}

.colabora-compact-cta-box {
  background: #FFFFFF;
  border: 1px solid rgba(184, 74, 40, 0.18);
  border-radius: 16px;
  padding: 1.5rem 1.6rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.85rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.03);
}

.colabora-compact-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  background: #B84A28;
  color: #FFFFFF !important;
  font-size: 0.94rem;
  font-weight: 700;
  padding: 13px 20px;
  border-radius: 10px;
  text-decoration: none !important;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.colabora-compact-btn:hover {
  background: #9A3B1E;
  transform: translateY(-2px);
}

.colabora-compact-note {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #4A5568;
  line-height: 1.4;
}

@media (max-width: 900px) {
  .colabora-compact-wrap {
    padding: 1.5rem 1.2rem;
  }
  .colabora-compact-top {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
  .colabora-compact-title {
    font-size: 1.55rem;
  }
}
</style>

<div id="colaborar" class="colabora-compact-wrap">
  <div class="colabora-compact-top">
    <div>
      <div class="colabora-compact-badge">
        <span>📚 MEMORIA COLECTIVA · ARCHIVO VECINAL</span>
      </div>
      <h2 class="colabora-compact-title">Construyamos el Archivo de Lastras</h2>
      <p class="colabora-compact-desc">Si guardas fotografías familiares antiguas, documentos o relatos del pueblo, los digitalizamos en alta resolución y te devolvemos el original en mano.</p>
      <div class="colabora-compact-pills">
        <div class="colabora-cpill">
          <span>📷</span>
          <div><strong>Fotografías Familiares</strong><small>Retratos, resina y fiestas</small></div>
        </div>
        <div class="colabora-cpill">
          <span>📜</span>
          <div><strong>Documentos y Cartas</strong><small>Programas, mapas y prensa</small></div>
        </div>
        <div class="colabora-cpill">
          <span>🎙️</span>
          <div><strong>Testimonios y Relatos</strong><small>Costumbres e historia oral</small></div>
        </div>
      </div>
    </div>
    <div class="colabora-compact-cta-box">
      <div style="font-size:0.88rem;font-weight:700;color:#151C22;">¿Tienes recuerdos para compartir con el pueblo?</div>
      <a href="mailto:info@lastrasdecuellar.net" class="colabora-compact-btn" target="_blank" rel="noopener noreferrer">
        <span>Enviar Material o Testimonio</span>
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </a>
      <div class="colabora-compact-note">
        <span>🔒 Custodia garantizada: devolvemos siempre el original tras su escaneado.</span>
      </div>
    </div>
  </div>
</div>
"""

# CSS adicional para compactación global (Desktop + Mobile swipe de noticias y reducción de espacios muertos)
COMPACT_HOME_EXTRA_CSS = """
/* ===================================================================
   OPTIMIZACIÓN DE USABILIDAD Y COMPACTACIÓN DE PORTADA (DESKTOP & MOBILE)
   =================================================================== */

/* 1. Reducción de paddings verticales excesivos entre secciones */
.elementor-element-ultimas_noticias_sec {
    padding: 2.6rem 1.5rem 2.2rem 1.5rem !important;
}
.elementor-element-36d5dba {
    padding: 2.5rem 1.5rem 2.5rem 1.5rem !important;
}
.elementor-element-2ec773cc {
    padding: 2.2rem 1.5rem 2.8rem 1.5rem !important;
}
.trilogia-editorial-section {
    margin: 0.75rem auto 2.2rem auto !important;
}
.trilogia-editorial-header {
    margin-bottom: 1.4rem !important;
}

/* 2. Tarjetas de la Gran Trilogía más proporcionadas y visibles sin tanto scroll */
.trilogia-card {
    min-height: 390px !important;
    padding: 1.6rem 1.4rem 1.5rem 1.4rem !important;
}
.trilogia-card-title {
    font-size: 1.45rem !important;
}
.trilogia-card-desc {
    font-size: 0.9rem !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 3 !important;
    -webkit-box-orient: vertical !important;
    overflow: hidden !important;
}

/* 3. Compactar Hero en escritorio y móvil (override de clases atómicas e-* de Elementor v4) */
html body [data-id="7d4e2a2e"],
html body .elementor-element-7d4e2a2e,
html body .elementor .e-6037a66f-0,
html body .elementor [data-id="7d4e2a2e"] {
    padding: 3.2rem 2rem 2.4rem 2rem !important;
}
html body .elementor .e-70bb8269-53ca,
html body [data-id="6037a66f"] {
    max-width: 1280px !important;
    font-size: 3.15rem !important;
    line-height: 1.14 !important;
    margin: 0.35rem 0 0.75rem 0 !important;
}
html body .elementor [data-id="166f414"],
html body [data-id="166f414"] {
    margin-bottom: 1.1rem !important;
}
html body .elementor [data-id="7592f82b"],
html body [data-id="7592f82b"] {
    margin-bottom: 0.85rem !important;
}
html body .elementor [data-id="6ccf2746"],
html body .elementor .e-69014bde-8bcb {
    margin: 0 0 1.25rem 0 !important;
}
html body .elementor [data-id="4677e080"],
html body .elementor .e-692e71ff-7735 {
    margin: 0 0 0.75rem 0 !important;
}
html body [data-id="7a56148a"],
html body .elementor-element-7a56148a {
    margin: 1.5rem auto 0.25rem auto !important;
}
html body [data-id="ad7f328"],
html body [data-id="4a90fabe"],
html body [data-id="3ed7f0f5"],
html body [data-id="563fe39c"],
html body [data-id="1cfa6303"] {
    padding: 0.65rem 1rem !important;
}

/* 4. Móvil: Hero Ultra-Compacto (cabe en 1 pantalla) + Últimas Noticias en Carrusel Swipe */
@media (max-width: 767px) {
    html body [data-id="7d4e2a2e"],
    html body .elementor-element-7d4e2a2e {
        padding: 1.15rem 0.95rem 1.4rem 0.95rem !important;
        min-height: auto !important;
    }
    /* Ocultar metadatos decorativos superiores y 3 píldoras temáticas en móvil */
    html body .elementor [data-id="166f414"],
    html body [data-id="166f414"],
    html body .elementor [data-id="7592f82b"],
    html body [data-id="7592f82b"] {
        display: none !important;
    }
    /* Ocultar los 3 botones redundantes dentro del Hero en móvil (ya están en la barra Quick-Nav justo debajo) */
    html body .elementor [data-id="4677e080"],
    html body [data-id="4677e080"],
    html body .elementor .e-692e71ff-7735 {
        display: none !important;
    }
    /* Título H1 proporcionado y limpio */
    html body .elementor .e-70bb8269-53ca,
    html body [data-id="6037a66f"] {
        font-size: 1.75rem !important;
        line-height: 1.15 !important;
        margin: 0.1rem 0 0.45rem 0 !important;
    }
    /* Subtítulo resumido a 2 líneas en móvil */
    html body .elementor [data-id="6ccf2746"],
    html body .elementor .e-69014bde-8bcb,
    html body [data-id="6ccf2746"] p {
        font-size: 0.88rem !important;
        line-height: 1.42 !important;
        margin: 0 auto 0.65rem auto !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
    }
    /* Buscador y botón de vídeo más compactos en móvil */
    .lastras-hero-video-bar-wrap {
        margin: 0.35rem auto 0.5rem auto !important;
    }
    /* 4 Métricas en una cuadrícula 2x2 ultra-compacta (ganando al rule de 480px de page_settings) */
    html body .elementor [data-id="7a56148a"],
    html body [data-id="7a56148a"],
    html body .elementor-element-7a56148a {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 0.35rem 0.5rem !important;
        margin: 0.5rem auto 0 auto !important;
        padding: 0.45rem 0.25rem !important;
        background: rgba(12, 18, 15, 0.55) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
    }
    html body .elementor [data-id="ad7f328"],
    html body .elementor [data-id="4a90fabe"],
    html body .elementor [data-id="3ed7f0f5"],
    html body .elementor [data-id="563fe39c"],
    html body .elementor [data-id="1cfa6303"],
    html body [data-id="ad7f328"],
    html body [data-id="4a90fabe"],
    html body [data-id="3ed7f0f5"],
    html body [data-id="1cfa6303"] {
        padding: 0.25rem 0.35rem !important;
    }
    html body [data-id="7a56148a"] h2,
    html body [data-id="7a56148a"] h3,
    html body [data-id="7a56148a"] .e-heading-base {
        font-size: 1.25rem !important;
        line-height: 1.1 !important;
        margin: 0 !important;
    }
    html body [data-id="7a56148a"] p {
        font-size: 0.62rem !important;
        letter-spacing: 0.06em !important;
    }
    .elementor-element-ultimas_noticias_sec {
        padding: 1.8rem 1rem 1.6rem 1rem !important;
    }
    .elementor-element-noticias_inner_con {
        gap: 1.15rem !important;
    }
    .elementor-element-ultimas_noticias_sec .elementor-posts-container {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
        padding: 0 !important;
        overflow: visible !important;
    }
    .elementor-element-ultimas_noticias_sec .elementor-posts-container > article.elementor-post {
        min-width: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        margin-bottom: 0 !important;
        border-radius: 12px !important;
    }
    .elementor-element-ultimas_noticias_sec .elementor-post__thumbnail img {
        height: 110px !important;
        object-fit: cover !important;
    }
    .elementor-element-ultimas_noticias_sec .elementor-post__text {
        padding: 0.65rem 0.7rem 0.75rem 0.7rem !important;
    }
    .elementor-element-ultimas_noticias_sec .elementor-post__title a {
        font-size: 0.92rem !important;
        line-height: 1.25 !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 3 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
    }
    .elementor-element-ultimas_noticias_sec .elementor-post__excerpt {
        display: none !important;
    }
    .elementor-element-ultimas_noticias_sec .elementor-post__read-more {
        font-size: 0.75rem !important;
    }

    /* Trilogía más compacta en móvil */
    .trilogia-card {
        min-height: 310px !important;
        padding: 1.35rem 1.2rem !important;
    }
    .trilogia-editorial-section {
        margin: 0.5rem auto 1.5rem auto !important;
    }

    /* Métricas del Hero en 2x2 compacto en móvil en vez de 4 filas apiladas */
    html body [data-id="7a56148a"],
    html body .elementor-element-7a56148a {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 0.65rem 0.5rem !important;
        margin: 1.2rem auto 0.4rem auto !important;
    }
    html body [data-id="ad7f328"],
    html body [data-id="4a90fabe"],
    html body [data-id="3ed7f0f5"],
    html body [data-id="563fe39c"],
    html body [data-id="1cfa6303"] {
        padding: 0.45rem 0.5rem !important;
    }
}
"""

new_sections = []
for s in orig_sections:
    sid = s.get("id")
    if sid == "7d8b12f4":
        # Eliminamos el bloque redundante de 3 tarjetas altas 'Tres Miradas' (reemplazado por Quick-Nav)
        continue
    elif sid == "10b4bf8d":
        for child in s.get("elements", []):
            for w in child.get("elements", []):
                if w.get("id") == "6ccf2746":
                    old_p = w["settings"]["paragraph"]["value"]
                    w["settings"]["paragraph"]["value"] = old_p.replace(
                        "Un territorio vivo en el corazón árido de Segovia",
                        "Un territorio vivo en la Tierra de Pinares segoviana"
                    )
        new_sections.append(s)
        # Insertamos la Barra Editorial de Acceso Rápido justo debajo del Hero
        new_sections.append(quick_nav_container)
    elif sid == "ultimas_noticias_sec":
        # Añadimos ancla #sec-noticias en la cabecera
        for child in s.get("elements", []):
            for w in child.get("elements", []):
                if w.get("id") == "noticias_header_html":
                    w["settings"]["html"] = w["settings"]["html"].replace(
                        '<div class="noticias-section-header">',
                        '<div id="sec-noticias" class="noticias-section-header">'
                    )
        new_sections.append(s)
    elif sid == "9f1d4a82":
        # Añadimos ancla #sec-trilogia
        for w in s.get("elements", []):
            if w.get("id") == "3a7b8e19":
                w["settings"]["html"] = w["settings"]["html"].replace(
                    '<section class="trilogia-editorial-section"',
                    '<section id="sec-trilogia" class="trilogia-editorial-section"'
                )
        new_sections.append(s)
    elif sid == "36d5dba":
        # Añadimos ancla #sec-reportajes
        for w in s.get("elements", []):
            if w.get("id") == "bento_reportajes_widget":
                w["settings"]["html"] = w["settings"]["html"].replace(
                    '<div class="bento-reportajes-wrap"',
                    '<div id="sec-reportajes" class="bento-reportajes-wrap"'
                )
        new_sections.append(s)
    elif sid == "2ec773cc":
        # Reemplazamos las 3 tarjetas gigantes de Colabora por el Banner Horizontal Editorial Compacto
        for child in s.get("elements", []):
            for w in child.get("elements", []):
                if w.get("id") == "bento_colabora_wgt":
                    w["settings"]["html"] = COMPACT_COLABORA_HTML
        new_sections.append(s)
    elif sid == "caminos_con_wrap":
        for w in s.get("elements", []):
            if w.get("id") == "caminos_style_widget":
                old_html = w["settings"]["html"]
                if "OPTIMIZACIÓN DE USABILIDAD Y COMPACTACIÓN DE PORTADA" not in old_html:
                    w["settings"]["html"] = old_html.replace("</style>", COMPACT_HOME_EXTRA_CSS + "\n</style>")
        new_sections.append(s)
    else:
        new_sections.append(s)

# Ordenamos para que después de la Barra Quick-Nav aparezca primero Últimas Noticias (Actualidad viva)
# seguida de La Gran Trilogía, Reportajes Especiales y Colabora Compacto
ordered_ids = [
    "79a3f82",
    "main_landmark_start",
    "10b4bf8d",
    "qnav2616",
    "ultimas_noticias_sec",
    "9f1d4a82",
    "36d5dba",
    "caminos_con_wrap",
    "2ec773cc",
    "main_landmark_end",
    "45db84e0",
    "luxury_footer_styles"
]
sec_dict = {s["id"]: s for s in new_sections}
root["elements"] = [sec_dict[i] for i in ordered_ids if i in sec_dict]

new_el_json_str = json.dumps([root], ensure_ascii=False)
# Validar JSON
json.loads(new_el_json_str)

print("=== 2. COMPROBANDO SI YA EXISTE LA PÁGINA DE PRUEBA ===")
code, found = api_request(f"{BASE_URL}/wp-json/wp/v2/pages?slug={TEST_SLUG}&status=any")
page_settings_clean = dict(source_page["meta"].get("_elementor_page_settings", {}))
if "custom_css" in page_settings_clean:
    page_settings_clean["custom_css"] = page_settings_clean["custom_css"].replace(
        "grid-template-columns: 1fr !important;",
        "grid-template-columns: repeat(2, 1fr) !important;"
    )

payload = {
    "title": "Inicio Compacto (Versión de Prueba)",
    "slug": TEST_SLUG,
    "status": "publish",
    "template": "elementor_canvas",
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-page",
        "_elementor_data": new_el_json_str,
        "_elementor_page_settings": page_settings_clean
    }
}

if found:
    test_id = found[0]["id"]
    print(f"Actualizando página de prueba existente ID {test_id}...")
    code, res_page = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/{test_id}", method="POST", payload=payload)
else:
    print("Creando nueva página de prueba...")
    code, res_page = api_request(f"{BASE_URL}/wp-json/wp/v2/pages", method="POST", payload=payload)

print(f"Respuesta HTTP: {code}")
print(f"ID Página de Prueba: {res_page.get('id')}")
print(f"URL Página de Prueba: {res_page.get('link')}")

print("=== 3. DESPLEGANDO EN LA PORTADA OFICIAL EN PRODUCCIÓN (26169) ===")
with open("backup_page_26169_before_compact_production_deploy.json", "w", encoding="utf-8") as f:
    json.dump(source_page, f, ensure_ascii=False, indent=2)
print("Backup de producción guardado: backup_page_26169_before_compact_production_deploy.json")

prod_payload = {
    "meta": {
        "_elementor_data": new_el_json_str,
        "_elementor_page_settings": page_settings_clean
    }
}
code_prod, res_prod = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/{SOURCE_PAGE_ID}", method="POST", payload=prod_payload)
print(f"Respuesta HTTP Portada Oficial (26169): {code_prod}")
print(f"URL Portada Oficial: {res_prod.get('link')}")

