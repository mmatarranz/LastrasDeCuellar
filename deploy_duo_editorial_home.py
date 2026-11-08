#!/usr/bin/env python3
"""
Despliegue del Dúo Editorial en la Portada (Página 26169) de Lastras de Cuéllar:
- Inserta el bloque Dúo Editorial (La Huella Resinera y La Arquitectura Popular)
  inmediatamente después de la sección de Últimas Noticias.
- Preserva todas las secciones existentes (Hero, Noticias, Bento, Tríptico, Colabora, Footer).
- Purga la caché de LiteSpeed.
- Verifica el despliegue en vivo.
"""

import sys
import json
import urllib.request

PAGE_ID = 26169
PAGE_URL = "https://www.lastrasdecuellar.net/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}"
BACKUP_FILE = "backup_page_26169_before_duo_editorial.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

DUO_HTML = """<!-- DÚO EDITORIAL: GRANDES MONOGRÁFICOS DE IDENTIDAD -->
<style>
/* ===================================================
   DÚO EDITORIAL: LA HUELLA RESINERA & ARQUITECTURA POPULAR
   =================================================== */
.duo-editorial-section {
  width: 100%;
  max-width: 1240px;
  margin: 1.5rem auto 4rem auto;
  padding: 0 1.25rem;
  box-sizing: border-box;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Cabecera Editorial */
.duo-editorial-header {
  margin-bottom: 2.25rem;
  text-align: left;
}

.duo-kicker-row {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(184, 74, 40, 0.08);
  border: 1px solid rgba(184, 74, 40, 0.22);
  padding: 6px 16px;
  border-radius: 9999px;
  margin-bottom: 0.85rem;
}

.duo-kicker-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #B84A28;
}

.duo-kicker {
  font-family: 'Cinzel', serif;
  font-size: 0.8rem;
  font-weight: 700;
  color: #B84A28;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.duo-editorial-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.45rem;
  line-height: 1.18;
  font-weight: 700;
  color: #111815;
  margin: 0 0 0.85rem 0;
  letter-spacing: -0.02em;
}

.duo-editorial-subtitle {
  font-size: 1.05rem;
  line-height: 1.62;
  color: #4A5568;
  max-width: 840px;
  margin: 0;
}

/* Grilla Dúo */
.duo-editorial-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  width: 100%;
  margin-top: 1.75rem;
}

/* Tarjeta Editorial */
.duo-card {
  position: relative;
  border-radius: 22px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 520px;
  padding: 2.5rem 2.2rem 2.2rem 2.2rem;
  box-sizing: border-box;
  text-decoration: none !important;
  box-shadow: 0 14px 35px -8px rgba(17, 24, 21, 0.16), 0 6px 12px -4px rgba(17, 24, 21, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.35s ease;
  isolation: isolate;
  background-color: #121A16;
}

.duo-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 45px -10px rgba(17, 24, 21, 0.32), 0 12px 18px -6px rgba(17, 24, 21, 0.18);
  border-color: rgba(214, 158, 46, 0.55);
}

/* Imagen de Fondo */
.duo-card-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
  transition: transform 0.65s cubic-bezier(0.16, 1, 0.3, 1), filter 0.65s ease;
  filter: brightness(0.9) contrast(1.05);
}

.duo-card:hover .duo-card-bg {
  transform: scale(1.06);
  filter: brightness(0.98) contrast(1.08);
}

/* Scrim / Degradado Oscuro Cinematográfico */
.duo-card-scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(14, 20, 17, 0.04) 0%,
    rgba(14, 20, 17, 0.32) 32%,
    rgba(14, 20, 17, 0.82) 66%,
    rgba(14, 20, 17, 0.98) 100%
  );
  z-index: 2;
  transition: background 0.35s ease;
}

.duo-card:hover .duo-card-scrim {
  background: linear-gradient(
    180deg,
    rgba(14, 20, 17, 0.02) 0%,
    rgba(14, 20, 17, 0.25) 28%,
    rgba(14, 20, 17, 0.86) 62%,
    rgba(14, 20, 17, 0.99) 100%
  );
}

/* Contenido de la Tarjeta */
.duo-card-body {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

/* Fila Superior de Metadatos */
.duo-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 0.25rem;
}

/* Badges de Categoría */
.duo-pill {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #FFFFFF;
  padding: 5px 13px;
  border-radius: 9999px;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.pill-resina {
  background-color: #176553;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.pill-patrimonio {
  background-color: #B84A28;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Badge de Lectura */
.duo-read-time {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 9999px;
  padding: 4px 11px;
  font-weight: 600;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

/* Título de la Tarjeta */
.duo-card-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.85rem;
  line-height: 1.22;
  font-weight: 700;
  color: #FFFFFF !important;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.55);
}

/* Descripción */
.duo-card-desc {
  font-size: 0.96rem;
  line-height: 1.58;
  color: rgba(255, 255, 255, 0.92);
  margin: 0;
  font-weight: 400;
}

/* Tags de Contenidos Clave */
.duo-tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 0.35rem 0 0.5rem 0;
  padding: 0;
  list-style: none;
}

.duo-tag-item {
  font-size: 0.76rem;
  font-weight: 600;
  color: #E2E8F0;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 6px;
  padding: 3px 9px;
  letter-spacing: 0.01em;
}

/* Botón de Acción */
.duo-card-btn {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  margin-top: 0.4rem;
  padding: 11px 20px;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: all 0.25s ease;
  width: fit-content;
}

.duo-card:hover .duo-card-btn {
  background: #FFFFFF;
  color: #111815;
  border-color: #FFFFFF;
  transform: translateX(3px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.duo-card-btn svg {
  transition: transform 0.25s ease;
}

.duo-card:hover .duo-card-btn svg {
  transform: translateX(4px);
}

/* RESPONSIVE DESIGN */
@media (max-width: 900px) {
  .duo-editorial-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .duo-card {
    min-height: 460px;
    padding: 2.2rem 1.6rem 1.8rem 1.6rem;
  }
}

@media (max-width: 767px) {
  .duo-editorial-section {
    margin: 1.75rem auto 3.25rem auto;
    padding: 0 1rem;
  }
  .duo-editorial-title {
    font-size: 1.95rem;
  }
  .duo-editorial-subtitle {
    font-size: 0.95rem;
  }
  .duo-card {
    min-height: 420px;
    padding: 1.8rem 1.3rem 1.6rem 1.3rem;
    border-radius: 18px;
  }
  .duo-card-title {
    font-size: 1.5rem;
  }
  .duo-card-desc {
    font-size: 0.9rem;
  }
  .duo-card-btn {
    width: 100%;
    justify-content: center;
    padding: 13px 18px;
    min-height: 48px;
    box-sizing: border-box;
  }
}
</style>

<section class="duo-editorial-section" aria-labelledby="duo-main-title">
  <!-- Cabecera de Sección -->
  <div class="duo-editorial-header">
    <div class="duo-kicker-row">
      <span class="duo-kicker-dot" aria-hidden="true"></span>
      <span class="duo-kicker">MONOGRÁFICOS DE IDENTIDAD &amp; MEMORIA VIVA</span>
    </div>
    <h2 id="duo-main-title" class="duo-editorial-title">Las Dos Grandes Huellas de Lastras de Cuéllar</h2>
    <p class="duo-editorial-subtitle">Adéntrate en los dos grandes pilares históricos y etnográficos de nuestro pueblo: el secular oficio resinero en el corazón del pinar y la riqueza monumental de nuestras ermitas, bodegas, molinos y esgrafiados.</p>
  </div>

  <!-- Grilla del Dúo Editorial -->
  <div class="duo-editorial-grid">
    <!-- Tarjeta 1: La Huella Resinera -->
    <a href="https://www.lastrasdecuellar.net/la-huella-resinera/" class="duo-card" title="Explorar el monográfico completo: La Huella Resinera de Lastras de Cuéllar">
      <img src="https://www.lastrasdecuellar.net/wp-content/uploads/pote-resina-scaled.jpg" alt="Pote tradicional de resina y corte en pino albar de Lastras de Cuéllar" class="duo-card-bg" loading="lazy" width="600" height="450">
      <div class="duo-card-scrim" aria-hidden="true"></div>
      <div class="duo-card-body">
        <div class="duo-meta-row">
          <span class="duo-pill pill-resina">OFICIOS TRADICIONALES • MEMORIA VIVA</span>
          <span class="duo-read-time">📖 Monográfico exhaustivo</span>
        </div>
        <h3 class="duo-card-title">El Alma del Pinar: La Huella Resinera</h3>
        <p class="duo-card-desc">Un homenaje riguroso y humano a las generaciones de resineros que forjaron la identidad lastreña: técnicas de corte, herramientas centenarias, la vida en el monte y la memoria oral de Tierra de Pinares.</p>
        <ul class="duo-tags-list" aria-label="Temas tratados en el reportaje">
          <li class="duo-tag-item">🌲 El Pote y la Media Luna</li>
          <li class="duo-tag-item">🗣️ Testimonios de Resineros</li>
          <li class="duo-tag-item">📜 Archivo de la Resina</li>
        </ul>
        <div class="duo-card-btn">
          <span>Explorar la Huella Resinera</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </div>
      </div>
    </a>

    <!-- Tarjeta 2: La Arquitectura Popular -->
    <a href="https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/" class="duo-card" title="Descubrir la investigación completa: La Arquitectura Popular de Lastras de Cuéllar">
      <img src="https://www.lastrasdecuellar.net/wp-content/uploads/esgrafiado-lastras-de-cuellar-scaled.jpg" alt="Esgrafiado geométrico tradicional segoviano en las fachadas de Lastras de Cuéllar" class="duo-card-bg" loading="lazy" width="600" height="450">
      <div class="duo-card-scrim" aria-hidden="true"></div>
      <div class="duo-card-body">
        <div class="duo-meta-row">
          <span class="duo-pill pill-patrimonio">ARQUITECTURA VERNÁCULA • HISTORIA</span>
          <span class="duo-read-time">🏛️ Investigación patrimonial</span>
        </div>
        <h3 class="duo-card-title">Ermitas, Bodegas y Esgrafiados: El Latido de la Piedra</h3>
        <p class="duo-card-desc">Una expedición exhaustiva por el patrimonio constructivo del municipio: las 170 bodegas del barrio norte, los molinos harineros del río Cega, las ermitas históricas y las singulares fachadas esgrafiadas segovianas.</p>
        <ul class="duo-tags-list" aria-label="Temas tratados en la investigación">
          <li class="duo-tag-item">🍷 170 Bodegas y Lagares</li>
          <li class="duo-tag-item">🌊 Molinos del Río Cega</li>
          <li class="duo-tag-item">🏛️ Ermitas y Esgrafiado</li>
        </ul>
        <div class="duo-card-btn">
          <span>Descubrir la Arquitectura</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </div>
      </div>
    </a>
  </div>
</section>
"""


def build_updated_elements():
    with open(BACKUP_FILE, "r", encoding="utf-8") as bf:
        page_data = json.load(bf)

    el_raw = page_data.get("meta", {}).get("_elementor_data", "")
    elements = json.loads(el_raw) if isinstance(el_raw, str) else el_raw

    root = elements[0]
    orig_sections = root.get("elements", [])
    print(f"[*] Secciones actuales en el root: {len(orig_sections)}")

    # Comprobar si ya existe el dúo
    for s in orig_sections:
        if s.get("id") == "9f1d4a82":
            print("[!] La sección 9f1d4a82 ya existe. Se reemplazará con la versión más reciente.")
            orig_sections.remove(s)
            break

    # Localizar el índice de ultimas_noticias_sec
    noticias_idx = -1
    for i, s in enumerate(orig_sections):
        if s.get("id") == "ultimas_noticias_sec":
            noticias_idx = i
            break

    if noticias_idx == -1:
        raise ValueError("No se encontró 'ultimas_noticias_sec' en la estructura.")

    print(f"[+] 'ultimas_noticias_sec' encontrado en el índice: {noticias_idx}")

    # Construir el contenedor del Dúo Editorial
    duo_container = {
        "id": "9f1d4a82",
        "elType": "e-flexbox",
        "settings": {
            "content_width": "full",
            "flex_direction": "column"
        },
        "elements": [
            {
                "id": "3a7b8e19",
                "elType": "widget",
                "widgetType": "html",
                "settings": {
                    "_title": "Dúo Editorial - Huella Resinera y Arquitectura Popular",
                    "html": DUO_HTML
                },
                "elements": []
            }
        ],
        "isInner": False
    }

    # Insertar inmediatamente después de noticias (índice noticias_idx + 1)
    new_sections = (
        orig_sections[:noticias_idx + 1] +
        [duo_container] +
        orig_sections[noticias_idx + 1:]
    )

    root["elements"] = new_sections
    print(f"[+] Nueva cantidad de secciones en root: {len(new_sections)}")

    for i, s in enumerate(new_sections):
        title = s.get("settings", {}).get("_title", "")
        print(f"  {i}: {s.get('id')} ({s.get('elType')}) {title}")

    # Serializar y validar que no hay errores de parsing
    test_json = json.dumps([root], ensure_ascii=False)
    json.loads(test_json)
    print("[+] Serialización JSON de _elementor_data validada con éxito.")

    return json.dumps([root], ensure_ascii=False)


def deploy(new_el_raw):
    print(f"\n[*] Desplegando en WordPress REST API: {REST_ENDPOINT}...")
    payload = json.dumps({
        "meta": {
            "_elementor_data": new_el_raw
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        REST_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": AUTH_HEADER,
            "User-Agent": "LastrasDuoDeployAgent/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[+] Estado de la actualización en WP: {resp.status}")
            resp_body = resp.read().decode("utf-8")
            data = json.loads(resp_body)
            print(f"[+] Respuesta recibida. Título de página: {data.get('title', {}).get('rendered', '')}")
    except Exception as e:
        print(f"[-] ERROR al desplegar en WordPress: {e}", file=sys.stderr)
        sys.exit(1)

    # Purga de LiteSpeed Cache
    print("\n[*] Purgando LiteSpeed Cache...")
    purge_req = urllib.request.Request(
        PAGE_URL,
        headers={
            "User-Agent": "LastrasCacheAgent/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-LiteSpeed-Purge": "*",
            "Authorization": AUTH_HEADER
        }
    )
    try:
        with urllib.request.urlopen(purge_req) as p_resp:
            print(f"[+] Estado de purga LiteSpeed: {p_resp.status}")
            print(f"[+] Cabecera X-LiteSpeed-Cache: {p_resp.headers.get('X-LiteSpeed-Cache', 'None')}")
    except Exception as e:
        print(f"[!] Aviso durante la purga LiteSpeed: {e}")

    # Verificación en vivo
    print("\n[*] Verificando presencia del Dúo Editorial en vivo en la Home...")
    verify_req = urllib.request.Request(
        f"{PAGE_URL}?cache_bust=duo_editorial_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            found_huella = "la-huella-resinera" in content
            found_arq = "la-arquitectura-popular" in content
            found_title = "Las Dos Grandes Huellas de Lastras de Cuéllar" in content

            print(f"[+] ¿Detectado enlace a la-huella-resinera?: {found_huella}")
            print(f"[+] ¿Detectado enlace a la-arquitectura-popular?: {found_arq}")
            print(f"[+] ¿Detectado titular de sección?: {found_title}")

            if found_huella and found_arq and found_title:
                print("\n🎉 ÉXITO TOTAL: El Dúo Editorial está 100% activo y verificado en la portada en vivo!")
            else:
                print("\n[!] AVISO: Algunos elementos no se detectaron directamente en el HTML devuelto (revisar caché de red).")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    new_el_raw = build_updated_elements()
    if "--deploy" in sys.argv:
        deploy(new_el_raw)
    else:
        print("\n[*] Modo de simulación completado con éxito. Ejecuta con '--deploy' para aplicar en vivo.")
