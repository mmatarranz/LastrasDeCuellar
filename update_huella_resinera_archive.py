#!/usr/bin/env python3
"""
Script de actualización para la página 'La Huella Resinera' (ID 26397):
1. Configura la sección 'Artículos y Testimonios en el Archivo' (.archive-grid) en 2 filas de 2 tarjetas (repeat(2, 1fr)).
2. Configura breakpoint mobile (<860px) para colapsar fluidamente a 1 columna.
3. Añade target="_blank" y rel="noopener noreferrer" a cada una de las 4 tarjetas de archivo para abrir en pestaña/ventana nueva.
4. Realiza el despliegue a la REST API de WordPress y purga la caché de LiteSpeed.
"""

import sys
import json
import re
import urllib.request

PAGE_ID = 26397
PAGE_URL = "https://www.lastrasdecuellar.net/la-huella-resinera/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}?context=edit"
BACKUP_FILE = "backup_page_26397_before_articles_2x2.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    # 1. Modificar CSS de .archive-grid
    old_css = """.archive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-top: 36px;
}"""

    new_css = """.archive-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
  margin-top: 36px;
}

@media (max-width: 860px) {
  .archive-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}"""

    if old_css not in html:
        raise ValueError("No se encontró el bloque CSS original de .archive-grid")

    html = html.replace(old_css, new_css)

    # Mejorar la altura del thumbnail para el layout de 2 columnas (de 170px a 200px)
    old_thumb_css = """.archive-card-thumb {
  height: 170px;"""
    new_thumb_css = """.archive-card-thumb {
  height: 200px;"""
    if old_thumb_css in html:
        html = html.replace(old_thumb_css, new_thumb_css)

    # 2. Modificar los enlaces de las tarjetas para que se abran en ventana nueva (target="_blank" rel="noopener noreferrer")
    # Buscar el contenedor <div class="archive-grid">...</div>
    archive_grid_match = re.search(r'(<div class="archive-grid">.*?</div>\s*</div>)', html, re.DOTALL)
    if not archive_grid_match:
        raise ValueError("No se encontró el bloque HTML de .archive-grid")

    old_grid_html = archive_grid_match.group(1)

    # Reemplazar <a href="..." class="archive-card"> por <a href="..." class="archive-card" target="_blank" rel="noopener noreferrer">
    def add_target_blank(match):
        attrs = match.group(0)
        if 'target=' in attrs:
            return attrs
        return attrs[:-1] + ' target="_blank" rel="noopener noreferrer">'

    new_grid_html = re.sub(r'<a\s+href="[^"]+"\s+class="archive-card">', add_target_blank, old_grid_html)

    # Verificar que se modificaron exactamente 4 tarjetas
    count_blank = new_grid_html.count('target="_blank"')
    if count_blank != 4:
        raise ValueError(f"Se esperaban 4 tarjetas con target='_blank', se encontraron {count_blank}")

    html = html.replace(old_grid_html, new_grid_html)

    el_data[1]["elements"][0]["settings"]["html"] = html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando cambios a WordPress: Página {PAGE_ID} ({PAGE_URL})...")
    headers = {
        "Authorization": AUTH_HEADER,
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "LastrasAntigravityDeploy/1.0"
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
    print(f"[*] Verificando contenido en vivo con cache-busting...")
    verify_req = urllib.request.Request(
        f"{PAGE_URL}?cache_bust=archive_2x2_blank",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            has_grid_2 = "grid-template-columns: repeat(2, 1fr);" in content
            blank_count = content.count('class="archive-card" target="_blank"')
            print(f"[+] Verificación CSS 2x2: {'SÍ' if has_grid_2 else 'NO'}")
            print(f"[+] Verificación target='_blank' en tarjetas: {blank_count} encontradas")
            if has_grid_2 and blank_count == 4:
                print("[+] ÉXITO TOTAL: Grilla 2x2 y apertura en nueva ventana verificadas en vivo!")
            else:
                print("[!] AVISO: Comprobar si LiteSpeed sigue sirviendo HTML en caché.")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    updated_el_data = build_updated_data()
    print("[*] Árbol de elementos validado correctamente (CSS 2x2 y 4 enlaces con target='_blank').")
    if "--deploy" in sys.argv:
        deploy(updated_el_data)
    else:
        print("[*] Modo de simulación completado. Ejecuta con '--deploy' para aplicar en vivo.")
