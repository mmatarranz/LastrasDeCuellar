#!/usr/bin/env python3
"""
Actualiza y publica la entrada conmemorativa del XX Aniversario y Nuevo Diseño Editorial 2026
de lastrasdecuellar.net (Post ID 26394, Media ID 26509), leyendo la autenticación desde
.agents/mcp_config.json sin exponer credenciales en el código fuente.
"""

import json
import urllib.request

BASE_URL = "https://www.lastrasdecuellar.net/wp-json/wp/v2"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
AUTH_HEADER = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def api_request(url, method="GET", payload=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "Lastras20AniversarioRedesign/1.0"
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


if __name__ == "__main__":
    post = api_request(f"{BASE_URL}/posts/26394?context=edit")
    print("Estado actual del Post 26394:", post.get("status"))
    print("Título:", post.get("title", {}).get("raw"))
    print("Enlace:", post.get("link"))
    print("Imagen destacada (Media ID):", post.get("featured_media"))
