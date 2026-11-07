#!/usr/bin/env python3
"""
Script para añadir target="_blank" rel="noopener noreferrer"
a todas las referencias y enlaces a artículos en la página 11962.
"""

import sys
import json
import re
import urllib.request

PAGE_ID = 11962
PAGE_URL = "https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}"
BACKUP_FILE = "backup_page_11962_before_target_blank.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    # Lista de slugs/artículos objetivo a los que queremos asegurar target="_blank"
    target_articles = [
        "https://www.lastrasdecuellar.net/de-la-harina-a-las-fabricas-de-luz/",
        "https://www.lastrasdecuellar.net/bodon-de-la-ibienza/",
        "https://www.lastrasdecuellar.net/la-llegada-de-la-luz-a-lastras-de-cuellar/",
        "https://www.lastrasdecuellar.net/el-futuro-del-rio-cega-en-lastras-radiografia-del-proceso-de-extincion-del-salto-de-garrido-el-ladron/",
        "https://www.lastrasdecuellar.net/el-esgrafiado-la-piel-geometrica-de-lastras-de-cuellar/",
        "https://www.lastrasdecuellar.net/la-iglesia-de-lastras-de-cuellar/",
        "https://www.lastrasdecuellar.net/el-cura-chicote-y-la-construccion-del-crucero-de-la-iglesia-de-lastras/",
        "https://www.lastrasdecuellar.net/ayudanos-a-conservar-nuestra-torre/"
    ]

    replacements_count = 0
    for art_url in target_articles:
        # Buscar todas las etiquetas <a ... href="art_url" ...> que no tengan target="_blank"
        pattern = re.compile(rf'<a\s+([^>]*?)href=[\"\']{re.escape(art_url)}[\"\']([^>]*?)>')
        
        def replace_link(match):
            nonlocal replacements_count
            attr1 = match.group(1).strip()
            attr2 = match.group(2).strip()
            full_attrs = f"{attr1} {attr2}".strip()
            
            # Si ya tiene target="_blank", no duplicar
            if 'target="_blank"' in full_attrs:
                return match.group(0)
            
            replacements_count += 1
            # Reconstruir limpiamente
            extra = ' target="_blank" rel="noopener noreferrer"'
            if full_attrs:
                return f'<a href="{art_url}" {full_attrs}{extra}>'
            else:
                return f'<a href="{art_url}"{extra}>'

        html = pattern.sub(replace_link, html)

    print(f"[*] Total de enlaces actualizados a target='_blank': {replacements_count}")
    el_data[1]["elements"][0]["settings"]["html"] = html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando enlaces target='_blank' a WordPress: Página {PAGE_ID}...")
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
    print(f"[*] Verificando enlaces target='_blank' en vivo...")
    verify_req = urllib.request.Request(
        f"{PAGE_URL}?cache_bust=target_blank_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            count_blank = content.count('target="_blank"')
            print(f"[+] VERIFICADO: Encontradas {count_blank} instancias de target='_blank' en vivo!")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    updated_el_data = build_updated_data()
    print("[*] Árbol de elementos validado correctamente.")
    if "--deploy" in sys.argv:
        deploy(updated_el_data)
    else:
        print("[*] Modo de simulación completado. Ejecuta con '--deploy' para aplicar en vivo.")
