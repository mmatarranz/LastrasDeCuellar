#!/usr/bin/env python3
"""
Script para rediseñar la última sección de la página de Patrimonio (Página 11962):
"Ermitas, arquitectura devocional".

Incorpora las cuatro ermitas históricas de Lastras de Cuéllar:
1. Virgen de Salcedón (despoblado medieval, fuente y romería de Pentecostés)
2. San Diego o del bosque (La Serreta, cazadero ducal, fundación c. 1591 y romería de San Antón)
3. Humilladero (cementerio, sillería del s. XVI, cruz caminera y Santo Cristo)
4. La Magdalena (San Esteban, despoblado matriz del origen de Lastras y patrona mayor)
"""

import sys
import json
import re
import urllib.request
import urllib.parse
import os

PAGE_ID = 11962
PAGE_URL = "https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}?context=edit"
BACKUP_FILE = "backup_page_11962_before_ermitas_revamp.json"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

NEW_ERMITAS_CSS = """
/* ========================================================
   SECCIÓN 7: ERMITAS, ARQUITECTURA DEVOCIONAL
   ======================================================== */
.arq-ermitas-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
}

@media (max-width: 860px) {
  .arq-ermitas-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}

.arq-ermita-card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.arq-ermita-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: #cbd5e0;
}

.arq-ermita-card .arq-card-img-wrap {
  position: relative;
  width: 100%;
  height: 250px;
  background: #edf2f7;
  overflow: hidden;
}

.arq-ermita-card .arq-card-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.arq-ermita-card:hover .arq-card-img-wrap img {
  transform: scale(1.05);
}

.arq-ermita-floating-badge {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(17, 24, 21, 0.88);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #ffffff;
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 5px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.arq-ermita-facts {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 18px 0;
  padding: 14px 16px;
  background: #f8fafc;
  border-radius: 10px;
  border-left: 3px solid var(--color-terracotta);
}

.arq-ermita-fact-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
  font-size: 0.86rem;
  line-height: 1.45;
}

.arq-fact-label {
  font-weight: 700;
  color: var(--color-primary-dark);
  white-space: nowrap;
}

.arq-fact-value {
  color: #4a5568;
}

.arq-card-action {
  margin-top: auto;
  padding-top: 14px;
}
"""

NEW_ERMITAS_SECTION_HTML = """  <!-- SECCIÓN 7: ERMITAS, ARQUITECTURA DEVOCIONAL -->
  <section id="ermitas" class="arq-section">
    <div class="arq-container">
      <div class="arq-section-header">
        <span class="arq-section-pill pill-terracotta">Espiritualidad, Memoria y Paisaje</span>
        <h2 class="arq-section-title">Ermitas, arquitectura devocional</h2>
        <p class="arq-section-desc">
          A lo largo de los siglos, el término de Lastras de Cuéllar albergó cuatro ermitas y templos históricos que vertebraban la devoción comunitaria, los despoblados medievales y los antiguos caminos: desde el retiro cinegético de La Serreta hasta el manantial sagrado de Salcedón.
        </p>
      </div>

      <div class="arq-ermitas-grid">
        <!-- TARJETA 1: VIRGEN DE SALCEDÓN -->
        <article class="arq-card arq-ermita-card">
          <div class="arq-card-img-wrap">
            <img src="https://www.lastrasdecuellar.net/wp-content/uploads/37281215285_b524d9a876_o.jpg" alt="Ermita de Nuestra Señora de Salcedón en Lastras de Cuéllar" loading="lazy" width="768" height="480">
            <span class="arq-ermita-floating-badge">Despoblado Medieval • Romería</span>
          </div>
          <div class="arq-card-body">
            <span class="arq-card-tag">Manantial Sagrado y Danza Ritual</span>
            <h3 class="arq-card-title">1. Ermita de la Virgen de Salcedón</h3>
            <p class="arq-card-text">
              Emplazada a unos cuatro kilómetros del pueblo en una pradera rodeada de densos pinares y junto a un legendario manantial de aguas puras, donde la tradición oral sitúa la aparición mariana. Sus raíces se hunden en el despoblado medieval de Salcedón, citado ya en el Fuero de Sepúlveda (1076, del latín <em>salictum</em>, sauceda). Con mandas de misas registradas desde inicios del siglo XVII, la ermita es el epicentro de la <strong>Romería de Pentecostés</strong>: jornada en la que el pueblo conduce en procesión a su patrona con danzas ininterrumpidas de paloteos y jotas al compás de la dulzaina castellana.
            </p>
            <div class="arq-ermita-facts">
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Ubicación:</span>
                <span class="arq-fact-value">Despoblado de Salcedón (a 4 km al SE)</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Hito Singular:</span>
                <span class="arq-fact-value">Fuente de Salcedón y Danza de Paloteos</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Celebración:</span>
                <span class="arq-fact-value">Lunes de Pentecostés (Romería Mayor)</span>
              </div>
            </div>
            <div class="arq-card-action">
              <a href="https://www.lastrasdecuellar.net/la-virgen-de-salcedon/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Leer la monografía histórica de la Virgen de Salcedón (se abre en nueva ventana)">
                <span>Leer monografía de Salcedón</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>

        <!-- TARJETA 2: SAN DIEGO O DEL BOSQUE (LA SERRETA) -->
        <article class="arq-card arq-ermita-card">
          <div class="arq-card-img-wrap">
            <img src="https://www.lastrasdecuellar.net/wp-content/uploads/ermita_de_san_anton_la_serreta.jpeg" alt="Ermita histórica de San Diego en el bosque de La Serreta" loading="lazy" width="768" height="480">
            <span class="arq-ermita-floating-badge">Cazadero Real • Casa de Alburquerque</span>
          </div>
          <div class="arq-card-body">
            <span class="arq-card-tag">Feudo Señorial en la Ribera del Cega</span>
            <h3 class="arq-card-title">2. San Diego o del Bosque (La Serreta)</h3>
            <p class="arq-card-text">
              Construida hacia <strong>1591</strong> en el corazón del Bosque de La Serreta, finca cinegética predilecta del rey Enrique IV y posterior feudo de don Beltrán de la Cueva, duque de Alburquerque, regulada por las célebres Ordenanzas de 1511. Erigida bajo la advocación franciscana de San Diego de Alcalá (canonizado en 1588), daba asistencia litúrgica a la comitiva ducal, guardas y monteros. Célebre por acoger también la romería tradicional de <strong>San Antón</strong>, albergó un valioso lienzo devocional asaltado en 1920 que la memoria legendaria de la comarca asociaba a la estela de Velázquez.
            </p>
            <div class="arq-ermita-facts">
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Ubicación:</span>
                <span class="arq-fact-value">Bosque y Palacio de La Serreta (río Cega)</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Fundación:</span>
                <span class="arq-fact-value">Hacia 1591 (Duques de Alburquerque)</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Devoción:</span>
                <span class="arq-fact-value">San Diego de Alcalá y Romería de San Antón</span>
              </div>
            </div>
            <div class="arq-card-action">
              <a href="https://www.lastrasdecuellar.net/palacio-bosque-la-serreta/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Descubrir el reportaje del Palacio y Bosque de La Serreta (se abre en nueva ventana)">
                <span>Descubrir el Bosque de La Serreta</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>

        <!-- TARJETA 3: HUMILLADERO (CEMENTERIO) -->
        <article class="arq-card arq-ermita-card">
          <div class="arq-card-img-wrap">
            <img src="https://www.lastrasdecuellar.net/wp-content/uploads/ermita-del-humilladero-lastras-de-cuellar-5-1024x768-1.webp" alt="Ermita del Humilladero o del Cementerio en Lastras de Cuéllar" loading="lazy" width="768" height="480">
            <span class="arq-ermita-floating-badge">Crucero Caminero • Siglo XVI</span>
          </div>
          <div class="arq-card-body">
            <span class="arq-card-tag">Plegaria de Arrieros y Memoria Vecinal</span>
            <h3 class="arq-card-title">3. Ermita del Humilladero (Cementerio)</h3>
            <p class="arq-card-text">
              Ubicada en la salida sur tradicional del caserío, se trata de una sobria obra del <strong>siglo XVI</strong> de planta cuadrangular, sillería de piedra caliza, alero labrado y cancela de forja para la devoción al aire libre. Nacida como «humilladero» caminero junto a una cruz de piedra, era el punto de parada obligada donde arrieros, labradores y pastores se arrodillaban («humillaban») al partir a los campos o regresar al anochecer orando ante el Santo Cristo. Tras la prohibición sanitaria decimonónica de realizar enterramientos en la iglesia, el cementerio municipal se ubicó contiguo a ella, consolidando su nombre popular de «la ermita del Cementerio».
            </p>
            <div class="arq-ermita-facts">
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Ubicación:</span>
                <span class="arq-fact-value">Salida sur del casco urbano (junto al cementerio)</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Arquitectura:</span>
                <span class="arq-fact-value">Sillería de piedra caliza y rejería de forja (s. XVI)</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Advocación:</span>
                <span class="arq-fact-value">Santo Cristo de los Caminantes y Difuntos</span>
              </div>
            </div>
            <div class="arq-card-action">
              <a href="https://www.lastrasdecuellar.net/la-ermita-del-cementerio/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Leer la investigación histórica de la Ermita del Humilladero (se abre en nueva ventana)">
                <span>Leer estudio del Humilladero</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>

        <!-- TARJETA 4: LA MAGDALENA (SAN ESTEBAN) -->
        <article class="arq-card arq-ermita-card">
          <div class="arq-card-img-wrap">
            <img src="https://www.lastrasdecuellar.net/wp-content/uploads/ruinas-san-esteban.png" alt="Ruinas y vega del despoblado medieval de San Esteban, solar de la primitiva ermita de La Magdalena" loading="lazy" width="768" height="480">
            <span class="arq-ermita-floating-badge">Origen Fundacional • Despoblado</span>
          </div>
          <div class="arq-card-body">
            <span class="arq-card-tag">La Aldea Primitiva y la Matrona de Lastras</span>
            <h3 class="arq-card-title">4. La Magdalena (San Esteban)</h3>
            <p class="arq-card-text">
              Testimonio directo del nacimiento comunal de Lastras de Cuéllar. La tradición documentada acredita que el pueblo actual nació de la unión de dos pequeñas aldeas medievales: <strong>San Esteban</strong> (en el prado de abajo) y <strong>El Escobar</strong> (en el prado de arriba). Sus pobladores —alfareros, tejeros y labradores asentados en una vega húmeda proclive a tercianas y fiebres palustres— decidieron refundar su vecindario en el altozano ventilado de La Lastra. Su templo y ermita primitiva bajo la advocación de <strong>Santa María Magdalena</strong> fue transferida como patrona titular a la gran iglesia parroquial de Lastras, perviviendo aún hoy en el paraje los cimientos de la aldea y la histórica Fuente de San Esteban.
            </p>
            <div class="arq-ermita-facts">
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Ubicación:</span>
                <span class="arq-fact-value">Prado de abajo y vega de San Esteban</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Origen Histórico:</span>
                <span class="arq-fact-value">Aldea matriz que dio nacimiento a Lastras</span>
              </div>
              <div class="arq-ermita-fact-item">
                <span class="arq-fact-label">Legado Vivo:</span>
                <span class="arq-fact-value">Advocación patronal de la Parroquia actual</span>
              </div>
            </div>
            <div class="arq-card-action">
              <a href="https://www.lastrasdecuellar.net/reportajes-especiales/historia-de-un-pueblo-y-sus-gentes/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Conocer la historia de los orígenes de Lastras y San Esteban (se abre en nueva ventana)">
                <span>Historia del poblado de San Esteban</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
"""


def build_updated_elementor_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    # 1. Inyectar nuevo CSS antes de </style>
    if "/* SECCIÓN 7: ERMITAS" not in html:
        style_end_pos = html.find("</style>")
        if style_end_pos == -1:
            raise ValueError("No se encontró </style> en el widget HTML")
        html = html[:style_end_pos] + NEW_ERMITAS_CSS + "\n" + html[style_end_pos:]

    # 2. Actualizar QuickNav button
    html = html.replace(
        '<a href="#ermitas" class="arq-quicknav-btn">🕊️ Ermitas y Paisaje</a>',
        '<a href="#ermitas" class="arq-quicknav-btn">🕊️ Ermitas, arquitectura devocional</a>'
    )

    # 3. Reemplazar la Sección 7 completa
    pattern = r"(<!-- SECCIÓN 7:.*?)(?=  <!-- LLAMADA A LA ACCIÓN)"
    new_html, num_subs = re.subn(pattern, NEW_ERMITAS_SECTION_HTML + "\n", html, flags=re.DOTALL)
    if num_subs != 1:
        raise ValueError(f"Se esperaba 1 sustitución de la sección 7, pero se realizaron {num_subs}")

    el_data[1]["elements"][0]["settings"]["html"] = new_html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando rediseño de Ermitas a WordPress (Página {PAGE_ID})...")
    headers = {
        "Authorization": AUTH_HEADER,
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "meta": {
            "_elementor_data": json.dumps(el_data, ensure_ascii=False)
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(REST_ENDPOINT, data=data_bytes, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        print(f"[+] Estado HTTP: {resp.status}")
        resp_json = json.loads(resp.read().decode("utf-8"))
        print(f"[+] Página actualizada con éxito: {resp_json.get('title', {}).get('rendered')}")


def purge_litespeed():
    print("[*] Purgando caché de LiteSpeed...")
    purge_script = os.path.join(os.path.dirname(__file__), ".agents", "skills", "litespeed-cache-control", "scripts", "purge_litespeed.py")
    if os.path.exists(purge_script):
        cmd = f"python3 '{purge_script}' --url '{PAGE_URL}'"
        res = os.system(cmd)
        print(f"[+] Resultado de purga por script: {res}")
    else:
        # Fallback de purga directa
        req = urllib.request.Request(PAGE_URL, headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-LiteSpeed-Purge": PAGE_URL,
            "Authorization": AUTH_HEADER
        })
        try:
            with urllib.request.urlopen(req) as resp:
                print(f"[+] Purga directa HTTP status: {resp.status}")
        except Exception as e:
            print(f"[!] Error purga directa: {e}")


def verify_deployment():
    print("[*] Verificando contenido en vivo...")
    req = urllib.request.Request(PAGE_URL, headers={
        "User-Agent": "Mozilla/5.0",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    })
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        checks = [
            "Ermitas, arquitectura devocional",
            "Ermita de la Virgen de Salcedón",
            "San Diego o del Bosque (La Serreta)",
            "Ermita del Humilladero (Cementerio)",
            "La Magdalena (San Esteban)"
        ]
        all_ok = True
        for c in checks:
            present = c in content
            print(f"  - Verificación '{c}': {'OK' if present else 'NO ENCONTRADO'}")
            if not present:
                all_ok = False
        return all_ok


if __name__ == "__main__":
    updated_data = build_updated_elementor_data()
    deploy(updated_data)
    purge_litespeed()
    verified = verify_deployment()
    if verified:
        print("[🎉] ¡Rediseño de la sección Ermitas completado y verificado con éxito!")
    else:
        print("[⚠️] Atención: Algún contenido puede requerir unos segundos adicionales para invalidar UCSS.")
