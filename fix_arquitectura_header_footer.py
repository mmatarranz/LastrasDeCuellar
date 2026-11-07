#!/usr/bin/env python3
"""
Script para sincronizar y corregir el Header y Footer de la página de
Arquitectura Popular y Patrimonio (ID 11962).

1. Integra el Header maestro (79a3f82) de la plantilla 13859 con todos sus estilos
   responsivos, navegación unificada, botón de vídeos y drawer móvil.
2. Preserva intacto el contenedor de contenido de Arquitectura Popular (arq_content_container).
3. Integra el Footer maestro (45db84e0) de la plantilla 26318 y su widget de estilos
   globales (luxury_footer_styles) para restaurar el diseño oscuro de alta gama.
4. Purga la caché de LiteSpeed para reflejar los cambios inmediatamente.
"""

import json
import urllib.request
import base64
import sys

PAGE_ID = 11962
URL_PAGE = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}?context=edit"
URL_HEADER = "https://www.lastrasdecuellar.net/wp-json/wp/v2/elementor_library/13859?context=edit"
URL_FOOTER = "https://www.lastrasdecuellar.net/wp-json/wp/v2/elementor_library/26318?context=edit"

# 1. Leer credenciales
with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
auth_header = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

def fetch_json(url):
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def post_json(url, payload):
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))

print("1. Obteniendo datos actuales de la página 11962 y plantillas...")
page_data = fetch_json(URL_PAGE)
t_head = fetch_json(URL_HEADER)
t_foot = fetch_json(URL_FOOTER)

# Extraer nodos maestros
raw_head = t_head.get("meta", {}).get("_elementor_data", "[]")
el_head = json.loads(raw_head) if isinstance(raw_head, str) else raw_head
master_header = el_head[0]

raw_foot = t_foot.get("meta", {}).get("_elementor_data", "[]")
el_foot = json.loads(raw_foot) if isinstance(raw_foot, str) else raw_foot
master_footer_container = el_foot[0]
master_footer_styles = el_foot[1]

# Extraer contenido actual de la página 11962
raw_page = page_data.get("meta", {}).get("_elementor_data", "[]")
el_page = json.loads(raw_page) if isinstance(raw_page, str) else raw_page

content_container = None
for el in el_page:
    if el.get("id") == "arq_content_container":
        content_container = el
        break

if not content_container:
    # Si no se encuentra por ID, tomar el segundo elemento
    if len(el_page) >= 2:
        content_container = el_page[1]
    else:
        print("ERROR: No se encontró el contenedor de contenido en la página 11962!")
        sys.exit(1)

print(f"Contenedor de contenido localizado: {content_container.get('id')}")

# Construir nuevo árbol de elementos
new_elements = [
    master_header,
    content_container,
    master_footer_container,
    master_footer_styles
]

print(f"2. Estructura construida con {len(new_elements)} nodos raíz.")

payload = {
    "meta": {
        "_elementor_data": json.dumps(new_elements, ensure_ascii=False),
        "_elementor_edit_mode": "builder"
    }
}

print("3. Enviando actualización a WordPress...")
code, resp = post_json(URL_PAGE, payload)
print(f"Resultado de la actualización: HTTP {code}")

if code in [200, 201]:
    print("¡Página 11962 actualizada con éxito!")
else:
    print("Error al actualizar:", resp)
    sys.exit(1)

# 4. Purgar caché de LiteSpeed
print("4. Purgando caché de LiteSpeed...")
purge_headers = {
    "Authorization": auth_header,
    "User-Agent": "LastrasAntigravityCacheAgent/1.0",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "X-LiteSpeed-Purge": "*"
}
try:
    purge_req = urllib.request.Request("https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/", headers=purge_headers)
    with urllib.request.urlopen(purge_req) as purge_resp:
        print(f"Purga LiteSpeed URL: HTTP {purge_resp.getcode()}")
        print("X-LiteSpeed-Cache:", dict(purge_resp.getheaders()).get("x-litespeed-cache"))
except Exception as e:
    print("Aviso en purga:", e)

try:
    purge_all_req = urllib.request.Request("https://www.lastrasdecuellar.net/", headers=purge_headers)
    with urllib.request.urlopen(purge_all_req) as purge_all_resp:
        print(f"Purga LiteSpeed Global: HTTP {purge_all_resp.getcode()}")
except Exception as e:
    print("Aviso en purga global:", e)

print("¡Proceso completado exitosamente!")
