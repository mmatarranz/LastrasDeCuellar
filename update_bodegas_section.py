#!/usr/bin/env python3
"""
Script para corregir y actualizar el bloque de las Bodegas en la sección
'Arqueología Industrial y Espacios Productivos' (Página 11962).

Sustituye la información genérica errónea (zarceras troncocónicas de Ribera del Duero)
por las características reales y singulares de las Bodegas de Lastras de Cuéllar
extraídas de la investigación monográfica (https://www.lastrasdecuellar.net/bodegas-de-lastras/):
- Cerca de 170 bodegas y una veintena de lagares en el barrio norte (c/ Pozo, c/ Fuente, Barreros).
- Tipología adosada, muros de mampostería y barro, teja curva segoviana a 'torta y lomo'.
- Distribución en 2 niveles: planta superior (merendero con chimenea y lagar) y sotarrizo excavado.
- El Lagar de Viga tradicional (viga de roble/encina, husillo, piedra de contrapeso, poyo y reguera).
- Dimensión social según el etnógrafo Ignacio Sanz: charlas en el sotarrizo, rito de entrega de la llave
  al nuevo mozo y hospitalidad con el forastero.
"""

import sys
import json
import re
import urllib.request

PAGE_ID = 11962
PAGE_URL = "https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}"
BACKUP_FILE = "backup_page_11962_before_bodegas_accurate_revamp.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

NEW_BODEGAS_HTML = """        <!-- FILA 1: BODEGAS DE LASTRAS -->
        <article class="arq-industry-row arq-industry-row-normal">
          <div class="arq-industry-media">
            <div class="arq-media-frame">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/bodegas-de-lastras-1536x864-1.jpeg" alt="Barrio de las bodegas tradicionales de Lastras de Cuéllar" loading="lazy" width="768" height="480">
            </div>
            <div class="arq-media-caption">
              <strong>Arquitectura Vernácula Vinícola:</strong> Fachadas adosadas de mampostería y barro con cubiertas a «torta y lomo» en el barrio norte de Lastras.
            </div>
          </div>
          <div class="arq-industry-content">
            <div class="arq-industry-header">
              <span class="arq-section-pill pill-wine">Cultura del Vino • Patrimonio Etnográfico</span>
              <h3 class="arq-industry-title">1. Las Bodegas de Lastras: Tipología Singular y Cinco Siglos de Historia</h3>
            </div>
            <p class="arq-industry-text">
              A diferencia de las bodegas excavadas en taludes de otros puntos de Castilla, Lastras de Cuéllar atesora un conjunto excepcional de unas <strong>170 bodegas y una veintena de lagares</strong> con una tipología vernácula propia: construcciones adosadas de planta rectangular, muros de mampostería y barro, orientadas al norte y cubiertas con teja curva segoviana colocada <em>«a torta y lomo»</em>. Documentadas desde mediados del siglo XVI y censadas en el Catastro de Ensenada de 1752, conforman un barrio vivo articulado entre la calle del Pozo, la calle de la Fuente y los Barreros.
            </p>
            <div class="arq-feature-list">
              <div class="arq-feature-item">
                <strong>Estructura en Dos Niveles (Merendero y Sotarrizo):</strong> La planta superior alberga el merendero con chimenea para la reunión y a veces el lagar; en el subsuelo, el <em>sotarrizo</em> excavado en roca y arcilla conserva el vino en cubas con temperatura y humedad naturales estables, provisto de hornacina en la pared para posar el porrón y las velas.
              </div>
              <div class="arq-feature-item">
                <strong>El Tradicional Lagar de Viga:</strong> Una veintena de lagares históricos conservan la monumental viga de roble como palanca, el husillo de presión, la piedra de contrapeso y la reguera de piedra que canaliza el mosto virgen hacia las cubas de fermentación.
              </div>
              <div class="arq-feature-item">
                <strong>El Sotarrizo como Alma Social:</strong> Como documenta el etnógrafo lastreño Ignacio Sanz, las bodegas son el gran espacio de sociabilidad de peñas y cuadrillas al pie de las cubas: escenario de charlas y rondas, del rito de paso juvenil con la entrega paterna de la llave al nuevo «mozo», y del honor hospitalario de abrir la bodega al forastero.
              </div>
            </div>
            <div class="arq-industry-action">
              <a href="https://www.lastrasdecuellar.net/bodegas-de-lastras/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Leer la investigación monográfica completa sobre las bodegas de Lastras de Cuéllar (se abre en nueva ventana)">
                <span>Leer monografía completa de las Bodegas</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>"""


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    # Reemplazar el bloque de la Fila 1 de Bodegas
    pattern = r"(        <!-- FILA 1: BODEGAS.*?)(?=        <!-- FILA 2:)"
    new_html, num_subs = re.subn(pattern, NEW_BODEGAS_HTML + "\n\n", html, flags=re.DOTALL)
    if num_subs != 1:
        raise ValueError(f"Se esperaba 1 reemplazo para la fila de bodegas, pero se hicieron {num_subs}")

    el_data[1]["elements"][0]["settings"]["html"] = new_html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando corrección de bodegas a WordPress: Página {PAGE_ID}...")
    headers = {
        "Authorization": AUTH_HEADER,
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "meta": {
            "_elementor_data": json.dumps(el_data, ensure_ascii=False)
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(REST_ENDPOINT, data=data_bytes, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        print(f"[+] Estado de respuesta HTTP: {resp.status}")
        resp_json = json.loads(resp.read().decode("utf-8"))
        print(f"[+] Página actualizada correctamente: '{resp_json.get('title', {}).get('rendered')}'")

    # Purga de LiteSpeed Cache
    print(f"[*] Purgando LiteSpeed Cache para: {PAGE_URL}...")
    purge_req = urllib.request.Request(
        PAGE_URL,
        headers={
            "User-Agent": "LastrasAntigravityCacheAgent/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-LiteSpeed-Purge": PAGE_URL,
            "Authorization": AUTH_HEADER
        }
    )
    try:
        with urllib.request.urlopen(purge_req) as p_resp:
            print(f"[+] Estado purga LiteSpeed: {p_resp.status}")
            print(f"[+] Cabecera X-LiteSpeed-Cache: {p_resp.headers.get('X-LiteSpeed-Cache', 'None')}")
    except Exception as e:
        print(f"[!] Aviso durante la purga LiteSpeed: {e}")

    # Verificación en vivo
    print(f"[*] Verificando contenido en vivo...")
    verify_req = urllib.request.Request(
        f"{PAGE_URL}?cache_bust=bodegas_fix_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            if "sotarrizo" in content and "torta y lomo" in content:
                print("[+] VERIFICADO: El contenido de las bodegas de Lastras con 'sotarrizo' y 'torta y lomo' está presente en vivo!")
            else:
                print("[!] AVISO: No se detectaron los términos en vivo (posible caché intermedia).")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    updated_el_data = build_updated_data()
    print("[*] Árbol de elementos validado correctamente.")
    if "--deploy" in sys.argv:
        deploy(updated_el_data)
    else:
        print("[*] Modo de simulación completado. Ejecuta con '--deploy' para aplicar en vivo.")
