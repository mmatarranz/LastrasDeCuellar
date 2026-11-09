import json
import time
import requests

with open('.agents/mcp_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
auth_header = cfg['mcpServers']['lastras-de-cuellar-segovia-elementor']['headers']['Authorization']
headers = {'Authorization': auth_header, 'Content-Type': 'application/json'}

url_p = "https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/26169?context=edit"
res_p = requests.get(url_p, headers=headers).json()

# 1. Backup before mutation
backup_file = f"backup_page_26169_before_bulletproof_thumb_fix_{int(time.time())}.json"
with open(backup_file, "w", encoding="utf-8") as f:
    json.dump(res_p, f, ensure_ascii=False, indent=2)
print("Backup saved to:", backup_file)

def find_node(nodes, target_id):
    for n in nodes:
        if n.get('id') == target_id: return n
        if 'elements' in n:
            r = find_node(n['elements'], target_id)
            if r: return r
    return None

live_el = json.loads(res_p['meta']['_elementor_data'])
w = find_node(live_el, 'caminos_style_widget')
html = w['settings']['html']

old_grid_block_start = "/* Grilla de 4 Tarjetas Dinámicas de Noticias */"
old_grid_block_end = "/* CTA Inferior de Noticias */"

idx1 = html.find(old_grid_block_start)
idx2 = html.find(old_grid_block_end, idx1)

if idx1 == -1 or idx2 == -1:
    print("ERROR: Markers not found!")
    exit(1)

bulletproof_grid_css = """/* Grilla de 4 Tarjetas Dinámicas de Noticias */
.elementor-element-noticias_posts_grid {
    width: 100% !important;
}
.elementor-element-noticias_posts_grid .elementor-posts-container {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 1.5rem !important;
    width: 100% !important;
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
.elementor-element-noticias_posts_grid .elementor-posts-container .elementor-post:nth-child(n+5) {
    display: none !important;
}
.elementor-element-noticias_posts_grid .elementor-post {
    background: #FFFFFF !important;
    border-radius: 18px !important;
    border: 1px solid rgba(22, 28, 34, 0.08) !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(30, 37, 43, 0.04) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.35s ease !important;
}
.elementor-element-noticias_posts_grid .elementor-post:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 16px 36px rgba(30, 37, 43, 0.1) !important;
    border-color: rgba(184, 74, 40, 0.35) !important;
}
.elementor-element-noticias_posts_grid .elementor-post__thumbnail__link,
.elementor-element-noticias_posts_grid .elementor-post__thumbnail {
    display: block !important;
    width: 100% !important;
    height: 195px !important;
    min-height: 195px !important;
    max-height: 195px !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    position: relative !important;
    background-color: #EAE6DF !important;
    border-radius: 17px 17px 0 0 !important;
}
.elementor-element-noticias_posts_grid .elementor-post__thumbnail img,
.elementor-element-ultimas_noticias_sec .elementor-post__thumbnail img {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100% !important;
    height: 100% !important;
    min-width: 100% !important;
    min-height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;
    object-fit: cover !important;
    object-position: center !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    transform: none !important;
    transition: filter 0.3s ease !important;
}
.elementor-element-noticias_posts_grid .elementor-post:hover .elementor-post__thumbnail img,
.elementor-element-ultimas_noticias_sec .elementor-post:hover .elementor-post__thumbnail img {
    filter: brightness(1.05) !important;
    transform: none !important;
}
.elementor-element-noticias_posts_grid .elementor-post__text {
    padding: 1.35rem 1.3rem 1.4rem 1.3rem !important;
    display: flex !important;
    flex-direction: column !important;
    flex-grow: 1 !important;
}
.elementor-element-noticias_posts_grid .elementor-post__meta-data {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    color: #A43C1B !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 0.55rem !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
}
.elementor-element-noticias_posts_grid .elementor-post__title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.15rem !important;
    line-height: 1.35 !important;
    font-weight: 700 !important;
    margin: 0 0 0.65rem 0 !important;
}
.elementor-element-noticias_posts_grid .elementor-post__title a {
    color: #151C22 !important;
    text-decoration: none !important;
    transition: color 0.2s ease !important;
}
.elementor-element-noticias_posts_grid .elementor-post:hover .elementor-post__title a {
    color: #A43C1B !important;
}
.elementor-element-noticias_posts_grid .elementor-post__excerpt {
    margin-bottom: 1.2rem !important;
}
.elementor-element-noticias_posts_grid .elementor-post__excerpt p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    line-height: 1.5 !important;
    color: #555555 !important;
    margin: 0 !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 3 !important;
    -webkit-box-orient: vertical !important;
    overflow: hidden !important;
}
.elementor-element-noticias_posts_grid .elementor-post__read-more {
    margin-top: auto !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: #A43C1B !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    text-decoration: none !important;
    transition: gap 0.25s ease, color 0.2s ease !important;
}
.elementor-element-noticias_posts_grid .elementor-post:hover .elementor-post__read-more {
    gap: 10px !important;
    color: #7B2E15 !important;
}
@media (max-width: 767px) {
    .elementor-element-noticias_posts_grid .elementor-post__thumbnail__link,
    .elementor-element-noticias_posts_grid .elementor-post__thumbnail {
        height: 120px !important;
        min-height: 120px !important;
        max-height: 120px !important;
    }
    .elementor-element-noticias_posts_grid .elementor-post__thumbnail img,
    .elementor-element-ultimas_noticias_sec .elementor-post__thumbnail img {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        min-width: 100% !important;
        min-height: 120px !important;
        max-height: 120px !important;
        object-fit: cover !important;
        transform: none !important;
    }
}
"""

new_html = html[:idx1] + bulletproof_grid_css + "\n\n" + html[idx2:]
w['settings']['html'] = new_html

payload = {
    'meta': {
        '_elementor_data': json.dumps(live_el, ensure_ascii=False)
    }
}

res_up = requests.post(url_p.replace("?context=edit", ""), headers=headers, json=payload)
print(f"POST to Page 26169: HTTP {res_up.status_code}")
