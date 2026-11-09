import json
import time
import requests

with open('.agents/mcp_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
auth_header = cfg['mcpServers']['lastras-de-cuellar-segovia-elementor']['headers']['Authorization']
headers = {'Authorization': auth_header, 'Content-Type': 'application/json'}

url_p = "https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/26169?context=edit"
res_p = requests.get(url_p, headers=headers).json()

# 1. Save backup of current state
backup_filename = f"backup_page_26169_before_caminos_restore_{int(time.time())}.json"
with open(backup_filename, "w", encoding="utf-8") as f:
    json.dump(res_p, f, ensure_ascii=False, indent=2)
print(f"Saved pre-mutation backup to: {backup_filename}")

# 2. Load the full uncorrupted HTML from backup_page_26169_before_header_fix_1794259526.json
with open('backup_page_26169_before_header_fix_1794259526.json') as f:
    d_uncorrupted = json.load(f)

el_uncorrupted = json.loads(d_uncorrupted['meta']['_elementor_data']) if isinstance(d_uncorrupted, dict) else d_uncorrupted

def find_node(nodes, target_id):
    for n in nodes:
        if n.get('id') == target_id: return n
        if 'elements' in n:
            r = find_node(n['elements'], target_id)
            if r: return r
    return None

w_orig = find_node(el_uncorrupted, 'caminos_style_widget')
full_html = w_orig['settings']['html']

# Section 1 boundary: 1607 to 6817
preamble = full_html[:1607]
rest_of_styles = full_html[6817:]

perfect_header_css = """/* ---------------------------------------------------
   1. MASTER HEADER (79a3f82) - FLAWLESS INLINE FIT
   --------------------------------------------------- */
.elementor-element-79a3f82 {
    width: 100% !important;
    background-color: rgba(249, 247, 242, 0.98) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border-bottom: 1px solid rgba(22, 28, 34, 0.08) !important;
    box-shadow: 0 4px 20px rgba(30, 37, 43, 0.05) !important;
    padding: 0.5rem 1.5rem !important;
    position: sticky !important;
    top: 0 !important;
    inset-block-start: 0px !important;
    z-index: 1000 !important;
    box-sizing: border-box !important;
}
.elementor-element-5e544b69 {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
    width: 100% !important;
    height: auto !important;
    min-height: 54px !important;
    flex-wrap: nowrap !important;
    gap: 0.5rem !important;
    box-sizing: border-box !important;
}
.elementor-element-1a85c756,
[data-id="1a85c756"],
a.elementor-element-1a85c756 {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 0.65rem !important;
    flex: 0 0 auto !important;
    width: auto !important;
    max-width: none !important;
    min-width: fit-content !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
    cursor: pointer !important;
    text-decoration: none !important;
    transition: opacity 0.2s ease !important;
}
.elementor-element-1a85c756:hover {
    opacity: 0.88 !important;
}
.elementor-element-7b2e4b47,
.elementor-element-1a85c756 img,
[data-id="7b2e4b47"] img,
[data-id="7b2e4b47"] {
    width: auto !important;
    height: 48px !important;
    max-width: 40px !important;
    max-height: 48px !important;
    object-fit: contain !important;
    display: block !important;
    flex-shrink: 0 !important;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12)) !important;
    margin: 0 !important;
    padding: 0 !important;
}
.elementor-element-46c38472,
[data-id="46c38472"] {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: flex-start !important;
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: fit-content !important;
    line-height: 1.15 !important;
    box-sizing: border-box !important;
    text-align: left !important;
    margin: 0 !important;
    padding: 0 !important;
}
.elementor-element-6d470876,
[data-id="6d470876"],
.elementor-element-1a85c756 span,
.elementor-element-1a85c756 a,
.elementor-element-6d470876 a {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 1.28rem !important;
    font-weight: 700 !important;
    color: #151C22 !important;
    letter-spacing: -0.01em !important;
    white-space: nowrap !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.15 !important;
    width: auto !important;
    text-decoration: none !important;
}
.elementor-element-23395620,
[data-id="23395620"],
.elementor-element-1a85c756 p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    color: #7B5800 !important;
    text-transform: uppercase !important;
    white-space: nowrap !important;
    margin: 2px 0 0 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}
.elementor-element-e39931c,
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
}
.elementor-element-e39931c .e-button-base,
.elementor-element-e39931c a {
    background: transparent !important;
    background-color: transparent !important;
    color: #1A242D !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    border: none !important;
    padding: 0.4rem 0.55rem !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    text-decoration: none !important;
}
.elementor-element-e39931c .e-button-base:hover,
.elementor-element-e39931c a:hover {
    color: #7B5800 !important;
    background: rgba(123, 88, 0, 0.08) !important;
    background-color: rgba(123, 88, 0, 0.08) !important;
}
.elementor-element-23cca5d9,
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
}
.elementor-element-23cca5d9 a,
.elementor-element-2ce90fc2 {
    background: #7B5800 !important;
    background-color: #7B5800 !important;
    color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 0.95rem !important;
    border-radius: 6px !important;
    box-shadow: 0 4px 12px rgba(123, 88, 0, 0.25) !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
    display: inline-flex !important;
    align-items: center !important;
}
.elementor-element-23cca5d9 a:hover,
.elementor-element-2ce90fc2:hover {
    background: #5D4300 !important;
    background-color: #5D4300 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(123, 88, 0, 0.35) !important;
}
@media (max-width: 1024px) {
    .elementor-element-e39931c,
    [data-id="e39931c"],
    .elementor-element-23cca5d9,
    [data-id="23cca5d9"] {
        display: none !important;
    }
}
"""

restored_html = preamble + perfect_header_css.strip() + '\n\n' + rest_of_styles

# 3. Update the live element tree of 26169
live_el = json.loads(res_p['meta']['_elementor_data'])
w_live = find_node(live_el, 'caminos_style_widget')
if w_live:
    w_live['settings']['html'] = restored_html
    print("Updated caminos_style_widget with full 122KB CSS!")

# Also ensure ultimas_noticias_sec and noticias_inner_con have explicit column settings
c_sec = find_node(live_el, 'ultimas_noticias_sec')
if c_sec and not c_sec.get('settings'):
    c_sec['settings'] = {'content_width': 'full'}

c_inner = find_node(live_el, 'noticias_inner_con')
if c_inner:
    if not c_inner.get('settings'):
        c_inner['settings'] = {}
    c_inner['settings']['flex_direction'] = 'column'
    c_inner['settings']['content_width'] = 'boxed'
    print("Configured noticias_inner_con with flex_direction: column in Elementor settings!")

# Send update to WordPress
payload = {
    'meta': {
        '_elementor_data': json.dumps(live_el, ensure_ascii=False)
    }
}
res_up = requests.post(url_p.replace("?context=edit", ""), headers=headers, json=payload)
print(f"POST to Page 26169: HTTP {res_up.status_code}")

