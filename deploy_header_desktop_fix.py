import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth

with open('.agents/mcp_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
auth_header = cfg['mcpServers']['lastras-de-cuellar-segovia-elementor']['headers']['Authorization']
headers = {'Authorization': auth_header, 'Content-Type': 'application/json'}

def find_node(nodes, target_id):
    for n in nodes:
        if n.get('id') == target_id:
            return n
        if 'elements' in n:
            r = find_node(n['elements'], target_id)
            if r:
                return r
    return None

def update_nav_widget_html(html_str):
    # Fix the .elementor-element-23cca5d9 in @media (min-width: 1025px)
    # Ensure width: auto !important; max-width: none !important; min-width: fit-content !important;
    
    old_cta_pat = """.elementor-element-23cca5d9,
    [data-id="23cca5d9"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        flex: 0 0 auto !important;
        margin-left: 0.4rem !important;
    }"""
    
    new_cta_replacement = """.elementor-element-23cca5d9,
    [data-id="23cca5d9"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
        flex: 0 0 auto !important;
        width: auto !important;
        max-width: none !important;
        min-width: fit-content !important;
        margin: 0 0 0 0.4rem !important;
    }"""

    if old_cta_pat in html_str:
        html_str = html_str.replace(old_cta_pat, new_cta_replacement)
        print("Replaced old CTA pattern successfully.")
    else:
        # Fallback regex replace for .elementor-element-23cca5d9
        import re
        html_str = re.sub(
            r'(\.elementor-element-23cca5d9,\s*\[data-id="23cca5d9"\]\s*\{)([^}]+)(\})',
            r'\1\n        display: flex !important;\n        flex-direction: row !important;\n        align-items: center !important;\n        justify-content: center !important;\n        flex: 0 0 auto !important;\n        width: auto !important;\n        max-width: none !important;\n        min-width: fit-content !important;\n        margin: 0 0 0 0.4rem !important;\n    \3',
            html_str
        )
        print("Used regex replacement for CTA pattern.")

    # Also ensure .elementor-element-e39931c has min-width: 0 !important;
    old_nav_pat = """.elementor-element-e39931c,
    [data-id="e39931c"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 0.2rem !important;
        flex: 1 1 auto !important;
        margin: 0 0.5rem 0 auto !important;
        width: auto !important;
        flex-wrap: nowrap !important;
    }"""
    
    new_nav_replacement = """.elementor-element-e39931c,
    [data-id="e39931c"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 0.25rem !important;
        flex: 1 1 auto !important;
        width: auto !important;
        max-width: none !important;
        min-width: 0 !important;
        margin: 0 0.5rem 0 auto !important;
        flex-wrap: nowrap !important;
    }"""

    if old_nav_pat in html_str:
        html_str = html_str.replace(old_nav_pat, new_nav_replacement)
        print("Replaced old NAV pattern successfully.")

    return html_str

# 1. Update Template 13859
url_t = "https://www.lastrasdecuellar.net/wp-json/wp/v2/elementor_library/13859?context=edit"
res_t = requests.get(url_t, headers=headers).json()
with open("backup_template_13859_before_header_desktop_fix.json", "w", encoding="utf-8") as f:
    json.dump(res_t, f, ensure_ascii=False, indent=2)

el_t = json.loads(res_t["meta"]["_elementor_data"])
node_t = find_node(el_t, "lastras_mobile_nav_widget")
if node_t:
    node_t["settings"]["html"] = update_nav_widget_html(node_t["settings"]["html"])
    res_up_t = requests.post(url_t.replace("?context=edit", ""), headers=headers, json={
        "meta": {"_elementor_data": json.dumps(el_t, ensure_ascii=False)}
    })
    print(f"Updated Template 13859: HTTP {res_up_t.status_code}")

# 2. Update Page 26169 (Home)
url_p = "https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/26169?context=edit"
res_p = requests.get(url_p, headers=headers).json()
with open("backup_page_26169_inicio_before_header_desktop_fix.json", "w", encoding="utf-8") as f:
    json.dump(res_p, f, ensure_ascii=False, indent=2)

el_p = json.loads(res_p["meta"]["_elementor_data"])
node_p = find_node(el_p, "lastras_mobile_nav_widget")
if node_p:
    node_p["settings"]["html"] = update_nav_widget_html(node_p["settings"]["html"])

node_cam = find_node(el_p, "caminos_style_widget")
if node_cam:
    h = node_cam["settings"]["html"]
    # Ensure caminos_style_widget also has the width: auto !important on 23cca5d9
    old_cam_cta = """.elementor-element-23cca5d9 {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    flex: 0 0 auto !important;
    flex-shrink: 0 !important;
    margin-left: 0.5rem !important;
}"""
    new_cam_cta = """.elementor-element-23cca5d9 {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: center !important;
    flex: 0 0 auto !important;
    flex-shrink: 0 !important;
    width: auto !important;
    max-width: none !important;
    min-width: fit-content !important;
    margin-left: 0.5rem !important;
}"""
    if old_cam_cta in h:
        h = h.replace(old_cam_cta, new_cam_cta)
    node_cam["settings"]["html"] = h

res_up_p = requests.post(url_p.replace("?context=edit", ""), headers=headers, json={
    "meta": {"_elementor_data": json.dumps(el_p, ensure_ascii=False)}
})
print(f"Updated Page 26169: HTTP {res_up_p.status_code}")

