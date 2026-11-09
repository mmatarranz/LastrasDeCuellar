#!/usr/bin/env python3
"""
Convierte el bloque de identidad del Header (Escudo + 'Lastras de Cuéllar' + 'TIERRA DE PINARES • SEGOVIA',
contenedor 1a85c756) en un enlace interactivo completo hacia la página de inicio (https://www.lastrasdecuellar.net/)
tanto en la Plantilla Global del Header (13859) como en todas las páginas que incrustan el Header maestro.
"""

import json
import os
import urllib.request
import sys

BASE_URL = "https://www.lastrasdecuellar.net"
HOME_URL = "https://www.lastrasdecuellar.net/"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
AUTH_HEADER = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def api_request(url, method="GET", payload=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "LastrasHeaderBrandLink/1.0"
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))


BRAND_LINK_JS = """
  function initHeaderBrandHomeLink() {
    var brands = document.querySelectorAll('[data-id="1a85c756"], .elementor-element-1a85c756');
    brands.forEach(function(brand) {
      brand.style.cursor = 'pointer';
      if (!brand.querySelector('.lastras-brand-home-overlay')) {
        if (window.getComputedStyle(brand).position === 'static') {
          brand.style.position = 'relative';
        }
        var a = document.createElement('a');
        a.href = 'https://www.lastrasdecuellar.net/';
        a.className = 'lastras-brand-home-overlay';
        a.setAttribute('aria-label', 'Ir a la página de inicio de Lastras de Cuéllar');
        a.title = 'Ir al Inicio — Lastras de Cuéllar';
        a.style.cssText = 'position:absolute;inset:0;z-index:25;display:block;text-decoration:none;background:transparent;';
        brand.appendChild(a);
      }
    });
  }
"""

BRAND_LINK_CSS = """
[data-id="1a85c756"], .elementor-element-1a85c756 {
    position: relative !important;
    cursor: pointer !important;
    text-decoration: none !important;
    transition: opacity 0.2s ease !important;
}
[data-id="1a85c756"]:hover, .elementor-element-1a85c756:hover {
    opacity: 0.88 !important;
}
"""


def inject_brand_link_in_tree(nodes):
    modified = False
    for node in nodes:
        nid = node.get("id")
        if nid == "1a85c756":
            settings = node.setdefault("settings", {})
            settings[" tag"] = {"$$type": "string", "value": "a"}
            settings["link"] = {
                "$$type": "link",
                "value": {
                    "destination": {"$$type": "url", "value": HOME_URL},
                    "isTargetBlank": {"$$type": "boolean", "value": False},
                    "tag": {"$$type": "string", "value": "a"}
                }
            }
            modified = True
        elif nid == "7b2e4b47":
            settings = node.setdefault("settings", {})
            if "image" in settings and isinstance(settings["image"].get("value"), dict):
                settings["image"]["value"]["link"] = {
                    "$$type": "link",
                    "value": {
                        "destination": {"$$type": "url", "value": HOME_URL},
                        "isTargetBlank": {"$$type": "boolean", "value": False},
                        "tag": {"$$type": "string", "value": "a"}
                    }
                }
                modified = True
        elif nid == "6d470876":
            settings = node.setdefault("settings", {})
            settings["link"] = {
                "$$type": "link",
                "value": {
                    "destination": {"$$type": "url", "value": HOME_URL},
                    "isTargetBlank": {"$$type": "boolean", "value": False},
                    "tag": {"$$type": "string", "value": "a"}
                }
            }
            modified = True
        elif nid == "lastras_mobile_nav_widget":
            html = node.get("settings", {}).get("html", "")
            if "initHeaderBrandHomeLink" not in html:
                html = html.replace("</style>", BRAND_LINK_CSS + "\n</style>", 1)
                html = html.replace(
                    "function highlightCurrentTab() {",
                    BRAND_LINK_JS + "\n  function highlightCurrentTab() {"
                )
                html = html.replace(
                    "initMobileMenu();\n      highlightCurrentTab();",
                    "initMobileMenu();\n      initHeaderBrandHomeLink();\n      highlightCurrentTab();"
                )
                html = html.replace(
                    "initMobileMenu();\n    highlightCurrentTab();",
                    "initMobileMenu();\n    initHeaderBrandHomeLink();\n    highlightCurrentTab();"
                )
                node["settings"]["html"] = html
                modified = True

        if "elements" in node and isinstance(node["elements"], list):
            if inject_brand_link_in_tree(node["elements"]):
                modified = True

    return modified


# 1. Actualizar Plantilla 13859 (Header Global)
print("=== 1. ACTUALIZANDO PLANTILLA HEADER GLOBAL (13859) ===")
code, tpl13859 = api_request(f"{BASE_URL}/wp-json/wp/v2/elementor_library/13859?context=edit")
if code == 200:
    bkp_tpl = "backup_template_13859_before_brand_home_link.json"
    if not os.path.exists(bkp_tpl):
        with open(bkp_tpl, "w", encoding="utf-8") as f:
            json.dump(tpl13859, f, ensure_ascii=False, indent=2)
    el_tpl = json.loads(tpl13859["meta"]["_elementor_data"])
    if inject_brand_link_in_tree(el_tpl):
        c_up, _ = api_request(
            f"{BASE_URL}/wp-json/wp/v2/elementor_library/13859",
            method="POST",
            payload={"meta": {"_elementor_data": json.dumps(el_tpl, ensure_ascii=False)}}
        )
        print(f"Plantilla 13859 actualizada: HTTP {c_up}")

# 2. Actualizar todas las páginas con el Header incrustado
TARGET_PAGES = [26169, 26499, 26397, 26389, 15218, 11962, 5459, 392, 402]
print("=== 2. ACTUALIZANDO PÁGINAS CON HEADER INCRUSTADO ===")
for pid in TARGET_PAGES:
    code, pdata = api_request(f"{BASE_URL}/wp-json/wp/v2/pages/{pid}?context=edit")
    if code != 200:
        continue
    bkp_p = f"backup_page_{pid}_before_brand_home_link.json"
    if not os.path.exists(bkp_p):
        with open(bkp_p, "w", encoding="utf-8") as f:
            json.dump(pdata, f, ensure_ascii=False, indent=2)
    el_p = json.loads(pdata["meta"]["_elementor_data"])
    if inject_brand_link_in_tree(el_p):
        c_up, _ = api_request(
            f"{BASE_URL}/wp-json/wp/v2/pages/{pid}",
            method="POST",
            payload={"meta": {"_elementor_data": json.dumps(el_p, ensure_ascii=False)}}
        )
        print(f"Página {pid} ({pdata.get('slug')}) actualizada: HTTP {c_up}")
