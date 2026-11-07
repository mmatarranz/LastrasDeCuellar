#!/usr/bin/env python3
"""
Script de actualización para configurar la grilla de los 4 molinos en formato 2 a 2 (2x2):
- Evita el desbalance de 3 tarjetas arriba y 1 abajo con hueco en blanco.
- Define .arq-molinos-grid-2x2 con grid-template-columns: repeat(2, 1fr) estricto.
- Mantiene diseño mobile-first y adaptativo (<860px a 1 columna).
- Realiza backup, actualiza _elementor_data y purga LiteSpeed Cache.
"""

import sys
import json
import re
import urllib.request

PAGE_ID = 11962
PAGE_URL = "https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}"
BACKUP_FILE = "backup_page_11962_before_molinos_2x2_fix.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    # 1. Añadir regla CSS .arq-molinos-grid-2x2 si no existe
    css_start = "/* --- MOLINOS & DESARROLLO INDUSTRIAL STYLES --- */"
    css_end = "</style>"
    idx_start = html.find(css_start)
    idx_end = html.find(css_end, idx_start)
    if idx_start == -1 or idx_end == -1:
        raise ValueError("Bloque CSS de molinos o cierre de style no encontrado")

    molinos_grid_css = """
/* Grilla 2 a 2 balanceada para los 4 molinos */
.arq-molinos-grid-2x2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
}
@media (max-width: 860px) {
  .arq-molinos-grid-2x2 {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
"""

    old_css_block = html[idx_start:idx_end]
    if ".arq-molinos-grid-2x2" not in old_css_block:
        new_css_block = old_css_block + "\n" + molinos_grid_css
        html = html[:idx_start] + new_css_block + html[idx_end:]

    # 2. Reemplazar la clase en la sección molinos
    m = re.search(r"(<section id=[\"']molinos[\"'].*?</section>)", html, re.DOTALL)
    if not m:
        raise ValueError("Sección molinos no encontrada")

    old_molinos_section = m.group(1)
    if 'class="arq-cards-grid-2"' in old_molinos_section:
        new_molinos_section = old_molinos_section.replace('class="arq-cards-grid-2"', 'class="arq-molinos-grid-2x2"')
        html = html.replace(old_molinos_section, new_molinos_section)
    elif 'class="arq-molinos-grid-2x2"' in old_molinos_section:
        print("[*] La clase .arq-molinos-grid-2x2 ya estaba aplicada en el HTML.")
    else:
        raise ValueError("No se encontró el contenedor de tarjetas en la sección molinos")

    el_data[1]["elements"][0]["settings"]["html"] = html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando grilla 2x2 a WordPress: Página {PAGE_ID}...")
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
        f"{PAGE_URL}?cache_bust=2x2_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            if "arq-molinos-grid-2x2" in content:
                print("[+] VERIFICADO: 'arq-molinos-grid-2x2' desplegado y visible en vivo!")
            else:
                print("[!] AVISO: No se detectó arq-molinos-grid-2x2 en la respuesta en vivo (posible caché intermedia).")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    updated_el_data = build_updated_data()
    print("[*] Árbol de elementos validado correctamente.")
    if "--deploy" in sys.argv:
        deploy(updated_el_data)
    else:
        print("[*] Modo de simulación completado. Ejecuta con '--deploy' para aplicar en vivo.")
