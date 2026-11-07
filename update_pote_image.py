#!/usr/bin/env python3
"""
Actualización de la imagen del Pote de Barro en la página de La Huella Resinera (ID 26397):
- Reemplaza la imagen moderna del pote de plástico por la imagen auténtica del pote tradicional de barro cocido / cerámica resinera:
  https://www.lastrasdecuellar.net/wp-content/uploads/pote-de-barro-resinero-tradicional.jpg
- Despliega a WordPress REST API.
- Purga LiteSpeed Cache.
"""

import sys
import json
import urllib.request

PAGE_ID = 26397
PAGE_URL = "https://www.lastrasdecuellar.net/la-huella-resinera/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}?context=edit"
BACKUP_FILE = "backup_page_26397_before_ceramic_pote_update.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

OLD_IMG = "https://www.lastrasdecuellar.net/wp-content/uploads/pote-resina-scaled.jpg"
NEW_IMG = "https://www.lastrasdecuellar.net/wp-content/uploads/pote-de-barro-resinero-tradicional.jpg"


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    if OLD_IMG not in html:
        raise ValueError(f"No se encontró la imagen antigua '{OLD_IMG}' en el HTML")

    html = html.replace(OLD_IMG, NEW_IMG)
    html = html.replace('alt="Pote tradicional de resina de barro cocido de Lastras"', 'alt="Pote tradicional de resina de barro cocido y cerámica"')

    el_data[1]["elements"][0]["settings"]["html"] = html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando imagen de pote de cerámica a WordPress: Página {PAGE_ID}...")
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
        f"{PAGE_URL}?cache_bust=pote_ceramica_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            if "pote-de-barro-resinero-tradicional.jpg" in content:
                print("[+] VERIFICADO EN VIVO: La imagen del pote de cerámica y barro cocido se muestra correctamente!")
            else:
                print("[!] AVISO: No se detectó la nueva imagen en la respuesta en vivo (posible caché intermedia).")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    updated_el_data = build_updated_data()
    print("[*] Árbol de datos validado correctamente con la nueva imagen de pote de cerámica.")
    if "--deploy" in sys.argv:
        deploy(updated_el_data)
    else:
        print("[*] Modo simulación completado. Ejecuta con '--deploy' para aplicar en vivo.")
