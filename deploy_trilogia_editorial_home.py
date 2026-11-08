#!/usr/bin/env python3
"""
Despliegue de la Gran Trilogía de Nuestra Identidad en la Portada (Página 26169) de Lastras de Cuéllar:
- Actualiza la sección editorial a 3 tarjetas:
  1. La Huella Resinera
  2. La Arquitectura Popular
  3. Alfareros y Tejeros de Lastras de Cuéllar
- Grilla equilibrada de 3 columnas (repeat(3, 1fr)) en escritorio y colapso fluido en móvil.
- Purga de LiteSpeed Cache.
- Verificación exhaustiva en vivo.
"""

import sys
import json
import urllib.request

PAGE_ID = 26169
PAGE_URL = "https://www.lastrasdecuellar.net/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}"
BACKUP_FILE = f"backup_page_{PAGE_ID}_before_trilogia_home.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

TRILOGIA_HTML = """<!-- TRILOGÍA EDITORIAL: GRANDES MONOGRÁFICOS DE IDENTIDAD -->
<style>
/* ===================================================
   TRILOGÍA EDITORIAL: RESINA, ARQUITECTURA Y BARRO
   =================================================== */
.trilogia-editorial-section {
  width: 100%;
  max-width: 1260px;
  margin: 1.5rem auto 4.5rem auto;
  padding: 0 1.25rem;
  box-sizing: border-box;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Cabecera Editorial */
.trilogia-editorial-header {
  margin-bottom: 2.25rem;
  text-align: left;
}

.trilogia-kicker-row {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(184, 74, 40, 0.08);
  border: 1px solid rgba(184, 74, 40, 0.22);
  padding: 6px 16px;
  border-radius: 9999px;
  margin-bottom: 0.85rem;
}

.trilogia-kicker-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #B84A28;
}

.trilogia-kicker {
  font-family: 'Cinzel', serif;
  font-size: 0.8rem;
  font-weight: 700;
  color: #B84A28;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.trilogia-editorial-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.45rem;
  line-height: 1.18;
  font-weight: 700;
  color: #111815;
  margin: 0 0 0.85rem 0;
  letter-spacing: -0.02em;
}

.trilogia-editorial-subtitle {
  font-size: 1.05rem;
  line-height: 1.62;
  color: #4A5568;
  max-width: 860px;
  margin: 0;
}

/* Grilla de la Trilogía (3 Columnas) */
.trilogia-editorial-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.75rem;
  width: 100%;
  margin-top: 1.75rem;
}

/* Tarjeta Editorial */
.trilogia-card {
  position: relative;
  border-radius: 22px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 520px;
  padding: 2.2rem 1.6rem 2rem 1.6rem;
  box-sizing: border-box;
  text-decoration: none !important;
  box-shadow: 0 14px 35px -8px rgba(17, 24, 21, 0.16), 0 6px 12px -4px rgba(17, 24, 21, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.35s ease;
  isolation: isolate;
  background-color: #121A16;
}

.trilogia-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 45px -10px rgba(17, 24, 21, 0.32), 0 12px 18px -6px rgba(17, 24, 21, 0.18);
  border-color: rgba(214, 158, 46, 0.55);
}

/* Imagen de Fondo */
.trilogia-card-bg {
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

.trilogia-card:hover .trilogia-card-bg {
  transform: scale(1.06);
  filter: brightness(0.98) contrast(1.08);
}

/* Scrim / Degradado Cinematográfico */
.trilogia-card-scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(14, 20, 17, 0.04) 0%,
    rgba(14, 20, 17, 0.32) 30%,
    rgba(14, 20, 17, 0.84) 65%,
    rgba(14, 20, 17, 0.98) 100%
  );
  z-index: 2;
  transition: background 0.35s ease;
}

.trilogia-card:hover .trilogia-card-scrim {
  background: linear-gradient(
    180deg,
    rgba(14, 20, 17, 0.02) 0%,
    rgba(14, 20, 17, 0.24) 26%,
    rgba(14, 20, 17, 0.88) 60%,
    rgba(14, 20, 17, 0.99) 100%
  );
}

/* Contenido de la Tarjeta */
.trilogia-card-body {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Fila Superior de Metadatos */
.trilogia-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 0.2rem;
}

/* Badges de Categoría */
.trilogia-pill {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #FFFFFF;
  padding: 5px 12px;
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

.pill-barro {
  background-color: #C28B24;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Badge de Lectura */
.trilogia-read-time {
  font-size: 0.74rem;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 9999px;
  padding: 4px 10px;
  font-weight: 600;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

/* Título de la Tarjeta */
.trilogia-card-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.62rem;
  line-height: 1.24;
  font-weight: 700;
  color: #FFFFFF !important;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.55);
}

/* Descripción */
.trilogia-card-desc {
  font-size: 0.92rem;
  line-height: 1.55;
  color: rgba(255, 255, 255, 0.92);
  margin: 0;
  font-weight: 400;
}

/* Tags de Contenidos Clave */
.trilogia-tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin: 0.2rem 0 0.4rem 0;
  padding: 0;
  list-style: none;
}

.trilogia-tag-item {
  font-size: 0.74rem;
  font-weight: 600;
  color: #E2E8F0;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 6px;
  padding: 3px 8px;
  letter-spacing: 0.01em;
}

/* Botón de Acción */
.trilogia-card-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 0.35rem;
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: all 0.25s ease;
  width: fit-content;
}

.trilogia-card:hover .trilogia-card-btn {
  background: #FFFFFF;
  color: #111815;
  border-color: #FFFFFF;
  transform: translateX(3px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.trilogia-card-btn svg {
  transition: transform 0.25s ease;
}

.trilogia-card:hover .trilogia-card-btn svg {
  transform: translateX(4px);
}

/* RESPONSIVE DESIGN */
@media (max-width: 1024px) {
  .trilogia-editorial-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  .trilogia-card:last-child {
    grid-column: span 2;
  }
}

@media (max-width: 767px) {
  .trilogia-editorial-section {
    margin: 1.75rem auto 3.25rem auto;
    padding: 0 1rem;
  }
  .trilogia-editorial-grid {
    grid-template-columns: 1fr;
    gap: 1.4rem;
  }
  .trilogia-card:last-child {
    grid-column: span 1;
  }
  .trilogia-editorial-title {
    font-size: 1.95rem;
  }
  .trilogia-editorial-subtitle {
    font-size: 0.95rem;
  }
  .trilogia-card {
    min-height: 420px;
    padding: 1.8rem 1.3rem 1.6rem 1.3rem;
    border-radius: 18px;
  }
  .trilogia-card-title {
    font-size: 1.45rem;
  }
  .trilogia-card-desc {
    font-size: 0.88rem;
  }
  .trilogia-card-btn {
    width: 100%;
    justify-content: center;
    padding: 12px 18px;
    min-height: 48px;
    box-sizing: border-box;
  }
}
</style>

<section class="trilogia-editorial-section" aria-labelledby="trilogia-main-title">
  <!-- Cabecera de Sección -->
  <div class="trilogia-editorial-header">
    <div class="trilogia-kicker-row">
      <span class="trilogia-kicker-dot" aria-hidden="true"></span>
      <span class="trilogia-kicker">GRANDES MONOGRÁFICOS DE IDENTIDAD &amp; MEMORIA VIVA</span>
    </div>
    <h2 id="trilogia-main-title" class="trilogia-editorial-title">La Gran Trilogía de Lastras: Resina, Arquitectura y Barro</h2>
    <p class="trilogia-editorial-subtitle">Adéntrate en los tres pilares históricos, etnográficos y patrimoniales que forjaron la identidad única de nuestro pueblo: el secular oficio resinero en el mar de pinos, la monumentalidad de nuestra arquitectura popular y el milenario arte del barro y el fuego.</p>
  </div>

  <!-- Grilla de la Trilogía (3 Columnas) -->
  <div class="trilogia-editorial-grid">
    <!-- Tarjeta 1: La Huella Resinera -->
    <a href="https://www.lastrasdecuellar.net/la-huella-resinera/" class="trilogia-card" title="Explorar el monográfico: La Huella Resinera de Lastras de Cuéllar">
      <img src="https://www.lastrasdecuellar.net/wp-content/uploads/pote-resina-scaled.jpg" alt="Pote tradicional de resina y corte en pino albar de Lastras de Cuéllar" class="trilogia-card-bg" loading="lazy" width="600" height="450">
      <div class="trilogia-card-scrim" aria-hidden="true"></div>
      <div class="trilogia-card-body">
        <div class="trilogia-meta-row">
          <span class="trilogia-pill pill-resina">OFICIOS TRADICIONALES • MEMORIA VIVA</span>
          <span class="trilogia-read-time">📖 Monográfico</span>
        </div>
        <h3 class="trilogia-card-title">El Alma del Pinar: La Huella Resinera</h3>
        <p class="trilogia-card-desc">Un homenaje riguroso y humano a las generaciones de resineros que forjaron la identidad lastreña: técnicas de corte, herramientas centenarias y memoria viva de Tierra de Pinares.</p>
        <ul class="trilogia-tags-list" aria-label="Temas tratados en el reportaje">
          <li class="trilogia-tag-item">🌲 El Pote y la Media Luna</li>
          <li class="trilogia-tag-item">🗣️ Testimonios de Resineros</li>
          <li class="trilogia-tag-item">📜 Archivo de la Resina</li>
        </ul>
        <div class="trilogia-card-btn">
          <span>Explorar la Resina</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </div>
      </div>
    </a>

    <!-- Tarjeta 2: La Arquitectura Popular -->
    <a href="https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/" class="trilogia-card" title="Descubrir la investigación: La Arquitectura Popular de Lastras de Cuéllar">
      <img src="https://www.lastrasdecuellar.net/wp-content/uploads/esgrafiado-lastras-de-cuellar-scaled.jpg" alt="Esgrafiado geométrico tradicional segoviano en las fachadas de Lastras de Cuéllar" class="trilogia-card-bg" loading="lazy" width="600" height="450">
      <div class="trilogia-card-scrim" aria-hidden="true"></div>
      <div class="trilogia-card-body">
        <div class="trilogia-meta-row">
          <span class="trilogia-pill pill-patrimonio">ARQUITECTURA VERNÁCULA • HISTORIA</span>
          <span class="trilogia-read-time">🏛️ Patrimonio</span>
        </div>
        <h3 class="trilogia-card-title">Ermitas, Bodegas y Esgrafiados</h3>
        <p class="trilogia-card-desc">Una expedición exhaustiva por el patrimonio constructivo del municipio: las 170 bodegas del barrio norte, los molinos harineros del río Cega y las singulares fachadas esgrafiadas.</p>
        <ul class="trilogia-tags-list" aria-label="Temas tratados en la investigación">
          <li class="trilogia-tag-item">🍷 170 Bodegas y Lagares</li>
          <li class="trilogia-tag-item">🌊 Molinos del Río Cega</li>
          <li class="trilogia-tag-item">🏛️ Ermitas y Esgrafiado</li>
        </ul>
        <div class="trilogia-card-btn">
          <span>Descubrir la Arquitectura</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </div>
      </div>
    </a>

    <!-- Tarjeta 3: Alfareros y Tejeros -->
    <a href="https://www.lastrasdecuellar.net/alfareros-y-tejeros-lastras-de-cuellar/" class="trilogia-card" title="Conocer la crónica monográfica: Alfareros y Tejeros de Lastras de Cuéllar">
      <img src="https://www.lastrasdecuellar.net/wp-content/uploads/alfareros-lastras-de-cuellar.jpg" alt="Alfareros históricos moldeando el barro tradicional en Lastras de Cuéllar" class="trilogia-card-bg" loading="lazy" width="600" height="450">
      <div class="trilogia-card-scrim" aria-hidden="true"></div>
      <div class="trilogia-card-body">
        <div class="trilogia-meta-row">
          <span class="trilogia-pill pill-barro">ARTESANÍA DEL BARRO • OFICIOS PERDIDOS</span>
          <span class="trilogia-read-time">🏺 Crónica Etnográfica</span>
        </div>
        <h3 class="trilogia-card-title">Alfareros y Tejeros: Barro y Fuego</h3>
        <p class="trilogia-card-desc">La memoria de los alfares de Los Moscos y Carlos Avial, el torno tradicional, los hornos morunos de leña y las tejeras que vistieron de teja curva segoviana a toda la comarca.</p>
        <ul class="trilogia-tags-list" aria-label="Temas tratados en la investigación">
          <li class="trilogia-tag-item">🏺 Tornos y Alfares</li>
          <li class="trilogia-tag-item">🔥 Hornos Morunos</li>
          <li class="trilogia-tag-item">🧱 Tejeras Tradicionales</li>
        </ul>
        <div class="trilogia-card-btn">
          <span>Conocer a los Alfareros</span>
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
    sections = root.get("elements", [])

    target_sec = None
    for s in sections:
        if s.get("id") == "9f1d4a82":
            target_sec = s
            break

    if not target_sec:
        raise ValueError("No se encontró la sección 9f1d4a82 en la estructura.")

    target_widget = target_sec["elements"][0]
    target_widget["settings"]["_title"] = "Trilogía Editorial - Resina, Arquitectura y Alfarería"
    target_widget["settings"]["html"] = TRILOGIA_HTML

    print("[+] Sección 9f1d4a82 actualizada con la Trilogía de 3 tarjetas.")
    serialized = json.dumps([root], ensure_ascii=False)
    json.loads(serialized)
    print("[+] Serialización JSON validada correctamente.")
    return serialized


def deploy(new_el_raw):
    print(f"\n[*] Desplegando Trilogía Editorial a WordPress REST API: {REST_ENDPOINT}...")
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
            "User-Agent": "LastrasTrilogiaDeployAgent/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[+] Estado de actualización en WP: {resp.status}")
            resp_body = resp.read().decode("utf-8")
            data = json.loads(resp_body)
            print(f"[+] Página actualizada correctamente: '{data.get('title', {}).get('rendered', '')}'")
    except Exception as e:
        print(f"[-] ERROR al desplegar en WordPress: {e}", file=sys.stderr)
        sys.exit(1)

    # Purga de LiteSpeed Cache
    print("\n[*] Purgando LiteSpeed Cache para la Portada...")
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
    print("\n[*] Verificando presencia de la Trilogía Editorial en vivo en la Portada...")
    verify_req = urllib.request.Request(
        f"{PAGE_URL}?cache_bust=trilogia_editorial_{PAGE_ID}",
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
            found_alfar = "alfareros-y-tejeros-lastras-de-cuellar" in content
            found_title = "La Gran Trilogía de Lastras: Resina, Arquitectura y Barro" in content

            print(f"[+] ¿Detectado enlace a La Huella Resinera?: {found_huella}")
            print(f"[+] ¿Detectado enlace a La Arquitectura Popular?: {found_arq}")
            print(f"[+] ¿Detectado enlace a Alfareros y Tejeros?: {found_alfar}")
            print(f"[+] ¿Detectado titular de la Trilogía?: {found_title}")

            if found_huella and found_arq and found_alfar and found_title:
                print("\n🎉 ÉXITO TOTAL: La Gran Trilogía de Lastras (3 columnas) está 100% activa y verificada en vivo!")
            else:
                print("\n[!] AVISO: Algunos elementos no se detectaron en la respuesta (posible caché intermedia).")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    new_el_raw = build_updated_elements()
    if "--deploy" in sys.argv:
        deploy(new_el_raw)
    else:
        print("\n[*] Modo de simulación completado con éxito. Ejecuta con '--deploy' para aplicar en vivo.")
