#!/usr/bin/env python3
"""
Script de actualización para la página 'La Huella Resinera' (ID 26397):
1. Elimina la tarjeta 'Los Alfares de Lastras de Cuéllar' de la sección de archivo.
2. Reorganiza las 3 tarjetas restantes en una sola línea (grid 3 columnas: repeat(3, 1fr)).
3. Elimina todas las referencias a alfares/alfareros para centrar el contenido exclusivamente en los resineros y el pote tradicional.
4. Despliega en WordPress REST API y purga LiteSpeed Cache.
5. Verifica el resultado en vivo.
"""

import sys
import json
import re
import urllib.request

PAGE_ID = 26397
PAGE_URL = "https://www.lastrasdecuellar.net/la-huella-resinera/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}?context=edit"
BACKUP_FILE = f"backup_page_{PAGE_ID}_before_remove_alfares_3_cols.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as bf:
        page_data = json.load(bf)

    raw = page_data["meta"]["_elementor_data"]
    el_data = json.loads(raw) if isinstance(raw, str) else raw
    html = el_data[1]["elements"][0]["settings"]["html"]

    # 1. Actualizar CSS de .archive-grid a 3 columnas
    old_css = """.archive-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
  margin-top: 36px;
}

@media (max-width: 860px) {
  .archive-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}"""

    new_css = """.archive-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 36px;
}

@media (max-width: 960px) {
  .archive-grid {
    grid-template-columns: 1fr;
    gap: 22px;
  }
}"""

    if old_css not in html:
        raise ValueError("No se encontró el bloque CSS original de .archive-grid")
    html = html.replace(old_css, new_css)

    # Ajustar altura del thumbnail para 3 columnas (185px)
    old_thumb = """.archive-card-thumb {
  height: 200px;"""
    new_thumb = """.archive-card-thumb {
  height: 185px;"""
    if old_thumb in html:
        html = html.replace(old_thumb, new_thumb)

    # 2. Eliminar la tarjeta de Los Alfares del archivo
    alfar_card_regex = r'<a\s+href="https://www\.lastrasdecuellar\.net/los-alfares-lastras-cuellar/"\s+class="archive-card"[^>]*>.*?</a>'
    match = re.search(alfar_card_regex, html, re.DOTALL)
    if not match:
        raise ValueError("No se encontró la tarjeta de 'Los Alfares de Lastras de Cuéllar'")
    html = html[:match.start()] + html[match.end():]

    # Limpiar posibles saltos vacíos
    html = re.sub(r'\n\s*\n\s*</div>\s*</div>\s*<!-- LLAMAMIENTO', '\n    </div>\n  </div>\n\n  <!-- LLAMAMIENTO', html)

    # 3. Eliminar referencias a alfares/alfareros para centrar en el oficio resinero
    # Hero text
    old_hero_text = "el barro cocido de sus alfares y la silueta eterna de sus chimeneas industriales."
    new_hero_text = "la nobleza de sus tradicionales potes de barro y la silueta eterna de sus chimeneas industriales."
    if old_hero_text in html:
        html = html.replace(old_hero_text, new_hero_text)

    # Hero stat
    old_stat = """        <div class="resin-stat-box">
          <span class="resin-stat-num">Alfares Propios</span>
          <span class="resin-stat-lbl">Potes de barro modelados</span>
        </div>"""
    new_stat = """        <div class="resin-stat-box">
          <span class="resin-stat-num">El Pote de Barro</span>
          <span class="resin-stat-lbl">Tiesto cónico tradicional</span>
        </div>"""
    if old_stat in html:
        html = html.replace(old_stat, new_stat)

    # Sección 3: Enfocada puramente en el Pote Resinero
    old_sec3 = """    <!-- SECCIÓN 3: LOS ALFARES Y EL POTE DE BARRO -->
    <div class="story-split" style="margin-top: 70px;">
      <div class="story-content">
        <span class="sec-tag">Artesanía de Barro</span>
        <h3>Los Alfares de Lastras: El nido de barro para el oro líquido</h3>
        <p>
          Mientras en la mayoría de pueblos de la comarca los resineros dependían de piezas traídas de fuera, 
          <strong>Lastras de Cuéllar contó con una floreciente tradición de alfares y tejeras</strong> 
          (talleres históricos como los de <em>Los Moscos</em> o <em>Carlos Avial</em>).
        </p>
        <p>
          En sus tornos de alfarero moldearon con arcilla autóctona decenas de miles de <strong>potes resineros</strong>: 
          tiestos cónicos sin orificio de desagüe, con borde reforzado para encajar con firmeza entre las dos puntas de hierro clavadas en la corteza del pino. 
        </p>
        <p>
          El pote de barro cocido era perfecto: su peso evitaba que el viento lo volteara, mantenía fresca la resina bajo el sol canicular 
          y no reaccionaba químicamente con la miera pura.
        </p>
        <ul class="resin-list">
          <li><strong>Tierra y agua:</strong> Arcillas modeladas y cocidas en hornos morunos de leña de pino.</li>
          <li><strong>Abastecimiento comarcal:</strong> Surtían de potes a los montes comunales de Lastras, Cuéllar, Hontalbilla y Cantalejo.</li>
        </ul>
      </div>

      <div class="story-media">
        <img src="https://www.lastrasdecuellar.net/wp-content/uploads/pote-de-barro-resinero-tradicional.jpg" alt="Pote tradicional de resina de barro cocido y cerámica" />
        <div class="story-badge-float">
          <strong>El Pote de Barro:</strong> Pieza identitaria elaborada en los alfares locales de Lastras que acompañó a generaciones enteras de resineros.
        </div>
      </div>
    </div>"""

    new_sec3 = """    <!-- SECCIÓN 3: EL POTE RESINERO TRADICIONAL -->
    <div class="story-split" style="margin-top: 70px;">
      <div class="story-content">
        <span class="sec-tag">Herramienta y Tradición</span>
        <h3>El Pote Resinero: El nido de barro para el oro líquido</h3>
        <p>
          Mientras en otros puntos de la península se ensayaron recipientes metálicos o de zinc, 
          <strong>en Lastras de Cuéllar el pote de barro cocido fue siempre la pieza reina insustituible</strong> 
          del oficio tradicional en el pinar.
        </p>
        <p>
          Eran <strong>tiestos cónicos de arcilla autóctona</strong> cocida al fuego, sin orificio de desagüe y provistos de un reborde reforzado diseñado específicamente para encajar con firmeza milimétrica entre las dos puntas de hierro clavadas en la corteza del pino bajo la chapa de zinc.
        </p>
        <p>
          El pote de barro cocido resultaba perfecto para el resinero: su propio peso evitaba que los vendavales lo voltearan del tronco, mantenía fresca y protegida la resina bajo el sol canicular de Castilla y no reaccionaba químicamente con la miera pura ni alteraba su calidad cristalina.
        </p>
        <ul class="resin-list">
          <li><strong>Tierra y fuego:</strong> Arcilla porosa cocida para resistir tanto las heladas invernales como los rigores del verano.</li>
          <li><strong>Capacidad exacta:</strong> Diseñado a la medida para acopiar la miera que brotaba tras cada pica antes de la recogida con la paletilla.</li>
        </ul>
      </div>

      <div class="story-media">
        <img src="https://www.lastrasdecuellar.net/wp-content/uploads/pote-de-barro-resinero-tradicional.jpg" alt="Pote tradicional de resina de barro cocido y cerámica" />
        <div class="story-badge-float">
          <strong>El Pote de Barro:</strong> Pieza identitaria e insustituible que acompañó a generaciones enteras de resineros en Lastras de Cuéllar.
        </div>
      </div>
    </div>"""

    if old_sec3 in html:
        html = html.replace(old_sec3, new_sec3)

    # Validaciones finales
    cards_count = html.count('class="archive-card"')
    if cards_count != 3:
        raise ValueError(f"Se esperaban exactamente 3 tarjetas en el archivo, se encontraron {cards_count}")

    alfar_matches = len(re.findall(r'alfar', html, re.IGNORECASE))
    print(f"[+] Referencias a 'alfar' restantes en el HTML: {alfar_matches}")
    print(f"[+] Tarjetas restantes en el archivo: {cards_count}")

    el_data[1]["elements"][0]["settings"]["html"] = html
    return el_data


def deploy(el_data):
    print(f"\n[*] Desplegando cambios a WordPress: Página {PAGE_ID} ({PAGE_URL})...")
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

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[+] Estado de respuesta HTTP WP: {resp.status}")
            resp_json = json.loads(resp.read().decode("utf-8"))
            print(f"[+] Página actualizada correctamente: '{resp_json.get('title', {}).get('rendered')}'")
    except Exception as e:
        print(f"[-] ERROR al desplegar en WordPress: {e}", file=sys.stderr)
        sys.exit(1)

    # Purga de LiteSpeed Cache
    print(f"\n[*] Purgando LiteSpeed Cache para: {PAGE_URL}...")
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
    print(f"\n[*] Verificando contenido en vivo con cache-busting...")
    verify_req = urllib.request.Request(
        f"{PAGE_URL}?cache_bust=archive_3_cols_no_alfares_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            has_grid_3 = "grid-template-columns: repeat(3, 1fr);" in content
            has_alfar_card = "los-alfares-lastras-cuellar" in content
            cards_count = content.count('class="archive-card" target="_blank"')

            print(f"[+] Verificación CSS 3 columnas: {'SÍ' if has_grid_3 else 'NO'}")
            print(f"[+] ¿Tarjeta de alfares eliminada?: {'SÍ' if not has_alfar_card else 'NO'}")
            print(f"[+] Tarjetas con target='_blank' en vivo: {cards_count} (esperadas: 3)")

            if has_grid_3 and not has_alfar_card and cards_count == 3:
                print("\n🎉 ÉXITO TOTAL: 3 tarjetas en una sola línea y referencias a alfares eliminadas con éxito en vivo!")
            else:
                print("\n[!] AVISO: Comprobar caché de LiteSpeed.")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    el_data = build_updated_data()
    print("[*] Árbol de elementos validado correctamente.")
    if "--deploy" in sys.argv:
        deploy(el_data)
    else:
        print("[*] Modo de simulación completado. Ejecuta con '--deploy' para aplicar en vivo.")
