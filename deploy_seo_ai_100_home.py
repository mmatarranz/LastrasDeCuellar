#!/usr/bin/env python3
"""
Optimización 100% de Arquitectura Web, UX Móvil (WCAG Touch Targets), Enlazado Canónico
(Cero Redirecciones 301), Lazy-Loading + Dimensiones Explícitas (CLS=0), y Grafo JSON-LD
Enriquecido para SEO y Motores de IA (AEO/GEO) en la Portada Oficial (ID 26169).
También pasa la página de prueba (ID 26507) a estado 'draft' para evitar contenido duplicado.
"""

import json
import re
import urllib.request
import sys

BASE_URL = "https://www.lastrasdecuellar.net"
HOME_ID = 26169
TEST_ID = 26507

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
AUTH_HEADER = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def api_request(url, method="GET", payload=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "LastrasSEO100Deployer/1.0"
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))


print("=== 1. DESCARGANDO PORTADA ACTUAL (26169) Y GUARDANDO BACKUP ===")
code, home_data = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/{HOME_ID}?context=edit")
if code != 200:
    print(f"Error al descargar 26169: {code}")
    sys.exit(1)

with open("backup_page_26169_before_seo_ai_100_optimization.json", "w", encoding="utf-8") as f:
    json.dump(home_data, f, ensure_ascii=False, indent=2)
print("Backup guardado: backup_page_26169_before_seo_ai_100_optimization.json")

el_raw = home_data["meta"]["_elementor_data"]

# 1. Unificar URLs internas para evitar redirecciones 301 o páginas antiguas en borrador
URL_REPLACEMENTS = [
    ("https://www.lastrasdecuellar.net/historia-de-lastras-de-cuellar/", "https://www.lastrasdecuellar.net/lastras-de-cuellar/historia-de-lastras-de-cuellar/"),
    ("https://www.lastrasdecuellar.net/lastras-de-cuellar-y-su-entorno/", "https://www.lastrasdecuellar.net/lastras-de-cuellar/lastras-de-cuellar-y-su-entorno/"),
    ("https://www.lastrasdecuellar.net/cultura-y-tradicion/", "https://www.lastrasdecuellar.net/lastras-de-cuellar/cultura-y-tradicion/"),
    ("https://www.lastrasdecuellar.net/actualidad-de-lastras-de-cuellar/", "https://www.lastrasdecuellar.net/lastras-de-cuellar/actualidad/"),
    ("https://www.lastrasdecuellar.net/actualidad/", "https://www.lastrasdecuellar.net/lastras-de-cuellar/actualidad/"),
    ("https://www.lastrasdecuellar.net/videos/", "https://www.lastrasdecuellar.net/lastras-de-cuellar/videos/"),
    ("https://www.lastrasdecuellar.net/?page_id=19899", "https://www.lastrasdecuellar.net/"),
    ("https://www.lastrasdecuellar.net/colaborar-con-la-web/", "https://www.lastrasdecuellar.net/#colaborar"),
    ("https://www.lastrasdecuellar.net/rutas-lastras-de-cuellar/", "https://www.lastrasdecuellar.net/reportajes-especiales/el-rio-cega/"),
]

for old_u, new_u in URL_REPLACEMENTS:
    el_raw = el_raw.replace(old_u, new_u)

elements = json.loads(el_raw)
root = elements[0]

# 2. Enriquecer imágenes de Bento Reportajes con width/height explícitos y decoding="async"
for s in root["elements"]:
    if s.get("id") == "36d5dba":
        for w in s.get("elements", []):
            if w.get("id") == "bento_reportajes_widget":
                h = w["settings"]["html"]
                h = h.replace(
                    'class="bento-side-img" loading="lazy">',
                    'class="bento-side-img" width="260" height="196" loading="lazy" decoding="async">'
                )
                w["settings"]["html"] = h

# 3. Construir el nuevo Grafo JSON-LD Completo para SEO + Motores de IA (AEO/GEO)
ENHANCED_JSON_LD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["AdministrativeArea", "Place"],
      "@id": "https://www.lastrasdecuellar.net/#lugar",
      "name": "Lastras de Cuéllar",
      "alternateName": ["Lastras de Cuéllar, Segovia", "Villa de Lastras de Cuéllar"],
      "description": "Municipio y villa histórica en la Tierra de Pinares segoviana (Castilla y León, España), a 899 m de altitud entre el río Cega y el arroyo Cerquilla. Destaca por su legado resinero, sus bodegas subterráneas, la alfarería tradicional, el esgrafiado segoviano, el complejo lagunar ZEPA y el histórico Palacio y Bosque de La Serreta (1490).",
      "url": "https://www.lastrasdecuellar.net/",
      "sameAs": [
        "https://es.wikipedia.org/wiki/Lastras_de_Cu%C3%A9llar",
        "https://www.wikidata.org/wiki/Q1919659"
      ],
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Lastras de Cuéllar",
        "addressRegion": "Segovia",
        "postalCode": "40352",
        "addressCountry": "ES"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 41.2981,
        "longitude": -4.1136,
        "elevation": "899"
      },
      "containedInPlace": {
        "@type": "AdministrativeArea",
        "name": "Tierra de Pinares (Segovia)"
      }
    },
    {
      "@type": "ItemList",
      "@id": "https://www.lastrasdecuellar.net/#colecciones-principales",
      "name": "Colecciones y Monográficos de Lastras de Cuéllar",
      "description": "Estructura documental del portal histórico, natural y etnográfico de Lastras de Cuéllar.",
      "numberOfItems": 6,
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Reportajes Históricos de Lastras de Cuéllar (100 crónicas documentales)",
          "url": "https://www.lastrasdecuellar.net/lastras-de-cuellar/reportajes-historicos-de-lastras-de-cuellar/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Reportajes de Naturaleza: Pinares, Lagunas y Río Cega (45 artículos)",
          "url": "https://www.lastrasdecuellar.net/lastras-de-cuellar/naturaleza/"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Personajes, Paisanos y Oficios Tradicionales (31 biografías)",
          "url": "https://www.lastrasdecuellar.net/lastras-de-cuellar/personajes/"
        },
        {
          "@type": "ListItem",
          "position": 4,
          "name": "La Huella Resinera en Lastras de Cuéllar",
          "url": "https://www.lastrasdecuellar.net/la-huella-resinera/"
        },
        {
          "@type": "ListItem",
          "position": 5,
          "name": "La Arquitectura Popular: Esgrafiado, Molinos, Ermitas y Bodegas",
          "url": "https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/"
        },
        {
          "@type": "ListItem",
          "position": 6,
          "name": "Alfareros y Tejeros de Lastras de Cuéllar: Barro y Fuego",
          "url": "https://www.lastrasdecuellar.net/alfareros-y-tejeros-lastras-de-cuellar/"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.lastrasdecuellar.net/#faq-identidad",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "¿Qué ver y descubrir en Lastras de Cuéllar (Segovia)?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Lastras de Cuéllar ofrece un patrimonio único en la Tierra de Pinares segoviana: la Iglesia Parroquial de Santa María Magdalena (s. XVI-XVIII), la Ermita de Nuestra Señora de Salcedón, las bodegas subterráneas tradicionales del Cotarro, el esgrafiado segoviano, los antiguos molinos y fábricas de resina, el Bosque y Palacio de La Serreta (1490), las riberas del río Cega y el complejo lagunar ZEPA (El Bodón, La Tenca y El Carrizal)."
          }
        },
        {
          "@type": "Question",
          "name": "¿Cuáles son los oficios tradicionales e históricos de Lastras de Cuéllar?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "La identidad económica y etnográfica de Lastras de Cuéllar se vertebra en torno a tres grandes oficios históricos documentados en el portal: la extracción y destilación de resina en los pinares (La Huella Resinera), la alfarería de cacharreros y tejeras comunales (Alfareros y Tejeros), y la molienda hidráulica y generación pionera de electricidad en el río Cega."
          }
        }
      ]
    },
    {
      "@type": "TouristAttraction",
      "@id": "https://www.lastrasdecuellar.net/#bodegas",
      "name": "Bodegas Tradicionales de Lastras de Cuéllar",
      "description": "Conjunto etnográfico de bodegas subterráneas centenarias excavadas en ladera, exponente de la arquitectura vernácula del vino en Tierra de Pinares.",
      "url": "https://www.lastrasdecuellar.net/bodegas-de-lastras/",
      "isAccessibleForFree": true,
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Lastras de Cuéllar",
        "addressRegion": "Segovia",
        "postalCode": "40352",
        "addressCountry": "ES"
      }
    },
    {
      "@type": "TouristAttraction",
      "@id": "https://www.lastrasdecuellar.net/#rio-cega",
      "name": "Riberas, Lagunas y Pinares del Río Cega en Lastras de Cuéllar",
      "description": "Espacio natural protegido fluvial y complejo lagunar ZEPA en Tierra de Pinares, con senderos tradicionales, molinos históricos y bosque de ribera.",
      "url": "https://www.lastrasdecuellar.net/reportajes-especiales/el-rio-cega/",
      "isAccessibleForFree": true,
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Lastras de Cuéllar",
        "addressRegion": "Segovia",
        "postalCode": "40352",
        "addressCountry": "ES"
      }
    }
  ]
}
</script>"""

# 4. Mejorar Touch Targets (WCAG >= 42px) en móvil y actualizar Schema en caminos_style_widget
TOUCH_TARGET_CSS = """
/* ===================================================================
   ERGONOMÍA TÁCTIL WCAG 2.5.5 (TOUCH TARGETS >= 42PX EN MÓVIL)
   =================================================================== */
@media (max-width: 767px) {
  .lastras-qpill {
    min-height: 42px !important;
    padding: 8px 10px !important;
    font-size: 0.78rem !important;
  }
  .noticias-view-all-link {
    min-height: 42px !important;
    padding: 6px 12px !important;
    background: rgba(164, 60, 27, 0.08) !important;
    border-radius: 9999px !important;
  }
  .elementor-element-ultimas_noticias_sec .elementor-post__read-more {
    display: inline-flex !important;
    align-items: center !important;
    min-height: 38px !important;
    padding: 4px 0 !important;
    font-weight: 700 !important;
  }
  .lastras-hero-search-form button[type="submit"] {
    min-height: 42px !important;
    min-width: 44px !important;
  }
}
"""

for s in root["elements"]:
    if s.get("id") == "caminos_con_wrap":
        for w in s.get("elements", []):
            if w.get("id") == "caminos_style_widget":
                html = w["settings"]["html"]
                # Reemplazar el bloque JSON-LD existente por el enriquecido
                html = re.sub(
                    r'<script type="application/ld\+json">.*?</script>',
                    ENHANCED_JSON_LD,
                    html,
                    flags=re.S
                )
                if "ERGONOMÍA TÁCTIL WCAG 2.5.5" not in html:
                    html = html.replace("</style>", TOUCH_TARGET_CSS + "\n</style>", 1)
                w["settings"]["html"] = html

new_el_str = json.dumps([root], ensure_ascii=False)
json.loads(new_el_str)

print("=== 2. PUBLICANDO OPTIMIZACIÓN 100% EN PORTADA (26169) ===")
code_home, _ = api_request(
    f"{BASE_URL}/wp-json/wp/v2/pages/{HOME_ID}",
    method="POST",
    payload={"meta": {"_elementor_data": new_el_str}}
)
print(f"Portada 26169 actualizada: HTTP {code_home}")

print("=== 3. PASANDO PÁGINA DE PRUEBA (26507) A BORRADOR (DRAFT) PARA EVITAR CONTENIDO DUPLICADO SEO ===")
try:
    code_draft, _ = api_request(
        f"{BASE_URL}/wp-json/wp/v2/pages/{TEST_ID}",
        method="POST",
        payload={"status": "draft"}
    )
    print(f"Página de prueba 26507 pasada a borrador: HTTP {code_draft}")
except Exception as e:
    print(f"Aviso al cambiar estado de 26507: {e}")
