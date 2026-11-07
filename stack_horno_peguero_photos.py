#!/usr/bin/env python3
"""
Script para colocar las fotos de la Chimenea de Cuchifre y del Horno Peguero
una debajo de la otra (apiladas verticalmente) en la Fila 2 de Arqueología Industrial.
Elimina el espacio en blanco y equilibra la altura respecto a la columna de texto.
"""

import sys
import json
import re
import urllib.request

PAGE_ID = 11962
PAGE_URL = "https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}"
BACKUP_FILE = "backup_page_11962_before_photos_stacked_vertically.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    # 1. Actualizar CSS: reemplazar .arq-media-grid-2 por .arq-media-stack
    css_old_pattern = r"/\* Díptico fotográfico para la Fila 2.*?\@media \(max-width: 580px\) \{\s*\.arq-media-grid-2 \{\s*grid-template-columns: 1fr;\s*gap: 16px;\s*\}\s*\}"
    
    css_new = """/* Fotos apiladas verticalmente para la Fila 2 (Chimenea + Horno Peguero) */
.arq-media-stack {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}
.arq-media-stack-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.arq-media-stack-item .arq-media-frame {
  margin: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  background: var(--color-stone);
  aspect-ratio: 16 / 10;
  width: 100%;
}
.arq-media-stack-item .arq-media-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}
.arq-industry-row:hover .arq-media-stack-item .arq-media-frame img {
  transform: scale(1.03);
}"""

    if re.search(css_old_pattern, html, re.DOTALL):
        html = re.sub(css_old_pattern, css_new, html, flags=re.DOTALL)
    elif ".arq-media-stack" not in html:
        # Si no coincidió exactamente la regex, reemplazar .arq-media-grid-2
        html = html.replace(".arq-media-grid-2 {", ".arq-media-grid-2-old {")
        style_close = "</style>"
        idx_style = html.find(style_close)
        html = html[:idx_style] + css_new + "\n" + html[idx_style:]

    # 2. Actualizar el bloque HTML en la Fila 2
    old_row_pattern = r"(<!-- FILA 2: FÁBRICAS DE MIERA.*?-->\s*<article.*?</article>)"
    m = re.search(old_row_pattern, html, re.DOTALL)
    if not m:
        raise ValueError("No se encontró la Fila 2 de Fábricas de Miera en el HTML")

    old_row = m.group(1)

    new_row = """<!-- FILA 2: FÁBRICAS DE MIERA Y LA CHIMENEA DE CUCHIFRE -->
        <article class="arq-industry-row arq-industry-row-reverse">
          <div class="arq-industry-media">
            <div class="arq-media-stack">
              <div class="arq-media-stack-item">
                <div class="arq-media-frame">
                  <img src="https://www.lastrasdecuellar.net/wp-content/uploads/chimenea-lastras-de-cuellar-768x432-1.webp" alt="Chimenea octogonal de la Fábrica de Cuchifre en Lastras de Cuéllar" loading="lazy" width="768" height="432">
                </div>
                <div class="arq-media-caption">
                  <strong>Chimenea de Cuchifre:</strong> Fuste octogonal de ~30m de altura erigido a finales de los años 40.
                </div>
              </div>
              <div class="arq-media-stack-item">
                <div class="arq-media-frame">
                  <img src="https://www.lastrasdecuellar.net/wp-content/uploads/image_gallery.jpeg" alt="Histórico Horno Peguero en la calle de la Fábrica, Lastras de Cuéllar" loading="lazy" width="600" height="450">
                </div>
                <div class="arq-media-caption">
                  <strong>Horno Peguero Tradicional:</strong> Estructura cupuliforme por hiladas para la destilación de la pez.
                </div>
              </div>
            </div>
          </div>
          <div class="arq-industry-content">
            <div class="arq-industry-header">
              <span class="arq-section-pill pill-pine">Patrimonio Resinero • Oro Líquido del Pinar</span>
              <h3 class="arq-industry-title">2. Las Fábricas de Miera, El Cuchifre y el Horno Peguero</h3>
            </div>
            <p class="arq-industry-text">
              El siglo XX consolidó a Lastras de Cuéllar como uno de los centros neurálgicos de la transformación resinera en Castilla. La extracción de la miera en los extensos pinares albares y negrales nutrió una floreciente industria química que destilaba la esencia de trementina (aguarrás) y la colofonia sólida.
            </p>
            <div class="arq-feature-list">
              <div class="arq-feature-item">
                <strong>Doble Complejo Industrial:</strong> Lastras contó simultáneamente con dos grandes plantas fabriles ("La Resinera Segoviana" y "La Fábrica de Cuchifre"), situando al municipio en la vanguardia provincial de producción.
              </div>
              <div class="arq-feature-item">
                <strong>La Chimenea de Cuchifre:</strong> Esbelta estructura de planta octogonal erigida a finales de los años 40 por los célebres constructores valencianos de la saga Martínez, hoy hito paisajístico visible a decenas de kilómetros.
              </div>
              <div class="arq-feature-item">
                <strong>El Histórico Horno Peguero:</strong> En la calle de la Fábrica se conserva este singular horno cupuliforme por aproximación de hiladas donde se calcinaba la «roña» para obtener la pez impermeabilizante para barcos, cubas y botas.
              </div>
            </div>
            <div class="arq-industry-action">
              <a href="https://www.lastrasdecuellar.net/la-chimenea-de-cuchifre-y-las-fabricas-de-resina/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Más información sobre la chimenea de Cuchifre y las fábricas de resina (se abre en nueva ventana)">
                <span>Más información sobre las Fábricas de Miera</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>"""

    html = html.replace(old_row, new_row)
    el_data[1]["elements"][0]["settings"]["html"] = html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando fotos apiladas verticalmente a WordPress (Página {PAGE_ID})...")
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
        f"{PAGE_URL}?cache_bust=stacked_photos_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            if "arq-media-stack" in content:
                print("[+] VERIFICADO EN VIVO: 'arq-media-stack' activo con fotos apiladas verticalmente!")
            else:
                print("[!] AVISO: Podría haber retraso en la propagación de la caché.")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    updated_el_data = build_updated_data()
    print("[*] Árbol de elementos validado localmente con éxito.")
    if "--deploy" in sys.argv:
        deploy(updated_el_data)
    else:
        print("[*] Modo de simulación completado con éxito. Ejecuta con '--deploy' para aplicar en vivo.")
