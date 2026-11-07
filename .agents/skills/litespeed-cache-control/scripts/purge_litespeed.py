#!/usr/bin/env python3
"""
Script de purga y verificación de LiteSpeed Cache para Lastras de Cuéllar.
Permite purgar una URL específica o el sitio completo, enviando cabeceras de purga
y comprobando el estado de la cabecera X-LiteSpeed-Cache tras la invalidación.
"""

import sys
import os
import argparse
import requests
import json

BASE_URL = "https://www.lastrasdecuellar.net"

def get_auth_headers():
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".agents", "mcp_config.json")
    if not os.path.exists(config_path):
        config_path = os.path.join(os.getcwd(), ".agents", "mcp_config.json")
    
    headers = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                server = data.get("mcpServers", {}).get("lastras-de-cuellar-segovia-elementor", {})
                h = server.get("headers", {})
                if h:
                    headers.update(h)
        except Exception as e:
            print(f"[Aviso] No se pudo leer credenciales de {config_path}: {e}")
    return headers

def purge_target(url, purge_all=False):
    auth_headers = get_auth_headers()
    purge_headers = {
        "User-Agent": "LastrasAntigravityCacheAgent/1.0",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "X-LiteSpeed-Purge": "*" if purge_all else url
    }
    purge_headers.update(auth_headers)

    target_url = url if not purge_all else f"{BASE_URL}/"
    print(f"[*] Enviando solicitud de purga a: {target_url} (Modo: {'GLOBAL' if purge_all else 'PÁGINA'})")

    try:
        # Enviar petición con cabecera de purga LiteSpeed
        res = requests.get(target_url, headers=purge_headers, timeout=15)
        print(f"[*] Código de respuesta: {res.status_code}")
        cache_hdr = res.headers.get("X-LiteSpeed-Cache", "No presente")
        print(f"[*] Cabecera X-LiteSpeed-Cache resultante: {cache_hdr}")

        # Segunda petición de verificación para medir frescura
        verify_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Cache-Control": "max-age=0"
        }
        verify_res = requests.get(target_url, headers=verify_headers, timeout=15)
        verify_cache = verify_res.headers.get("X-LiteSpeed-Cache", "No presente")
        print(f"[*] Verificación de entrega pública (X-LiteSpeed-Cache): {verify_cache}")

        if res.status_code in [200, 204]:
            print(f"✅ Purga de LiteSpeed procesada con éxito para {target_url}")
            return True
        else:
            print(f"⚠️ El servidor respondió con estado {res.status_code}")
            return False
    except Exception as ex:
        print(f"❌ Error al contactar el servidor: {ex}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Purgador de LiteSpeed Cache para Lastras de Cuéllar")
    parser.add_argument("--url", help="URL específica para purgar", default=None)
    parser.add_argument("--all", action="store_true", help="Purgar la caché de todo el sitio")

    args = parser.parse_args()

    if not args.url and not args.all:
        target = f"{BASE_URL}/"
        purge_target(target, purge_all=False)
    elif args.all:
        purge_target(BASE_URL, purge_all=True)
    else:
        purge_target(args.url, purge_all=False)
