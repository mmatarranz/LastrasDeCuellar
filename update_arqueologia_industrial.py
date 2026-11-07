#!/usr/bin/env python3
"""
Script de actualización para el rediseño total de la sección
'Arqueología Industrial y Espacios Productivos' en la página de Patrimonio (ID 11962):
- Divide la sección en 4 filas únicas:
    1. Bodegas Subterráneas (enlace a /bodegas-de-lastras/)
    2. Fábricas de Miera y Cuchifre (enlace a /la-chimenea-de-cuchifre-y-las-fabricas-de-resina/)
    3. Los Alfares y Cacharreros Viejos (enlace a /los-alfares-lastras-cuellar/)
    4. Las Tejeras y Hornos de Tejas (con documentación de 1523, 1546 y Miñano, enlace a /los-barreros-y-la-extraccion-del-barro-arcilla/)
- Cada subsección cuenta con botón para más información en nueva ventana (target="_blank" rel="noopener noreferrer").
- Diseño alterno responsive, tipografía Playfair/Plus Jakarta Sans, y tokens del sistema de diseño.
- Purga LiteSpeed Cache y verificación en vivo.
"""

import sys
import json
import re
import urllib.request

PAGE_ID = 11962
PAGE_URL = "https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/"
REST_ENDPOINT = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}"
BACKUP_FILE = "backup_page_11962_before_arqueologia_industrial_revamp.json"

# Cargar credenciales desde .agents/mcp_config.json
with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
AUTH_HEADER = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def build_updated_data():
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        page_data = json.load(f)

    el_data = json.loads(page_data["meta"]["_elementor_data"])
    html = el_data[1]["elements"][0]["settings"]["html"]

    # --- 1. CSS PARA LAS 4 FILAS ÚNICAS ---
    css_new = """
/* --- ARQUEOLOGÍA INDUSTRIAL: 4 FILAS SHOWCASE --- */
.arq-industry-showcase {
  display: flex;
  flex-direction: column;
  gap: 48px;
  margin-top: 36px;
}

.arq-industry-row {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 44px;
  align-items: center;
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 40px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.arq-industry-row:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: #cbd5e0;
}

.arq-industry-row-reverse {
  grid-template-columns: 1.15fr 1fr;
}

.arq-industry-row-reverse .arq-industry-media {
  order: 2;
}

.arq-industry-row-reverse .arq-industry-content {
  order: 1;
}

.arq-industry-media {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.arq-industry-media .arq-media-frame {
  margin: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  background: var(--color-stone);
  aspect-ratio: 16 / 10;
}

.arq-industry-media .arq-media-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.arq-industry-row:hover .arq-industry-media .arq-media-frame img {
  transform: scale(1.03);
}

.arq-industry-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.arq-industry-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pill-wine {
  background: rgba(136, 19, 55, 0.1);
  color: #881337;
  border: 1px solid rgba(136, 19, 55, 0.2);
}

.pill-amber {
  background: rgba(180, 83, 9, 0.1);
  color: #b45309;
  border: 1px solid rgba(180, 83, 9, 0.2);
}

.arq-industry-title {
  font-family: var(--font-serif);
  font-size: clamp(1.45rem, 2.3vw, 1.85rem);
  font-weight: 700;
  color: var(--color-primary-dark);
  margin: 0;
  line-height: 1.3;
}

.arq-industry-text {
  font-size: 1.02rem;
  color: var(--color-text-main);
  line-height: 1.68;
  margin: 0;
}

/* Caja de documentación histórica para Tejeras */
.arq-history-box {
  background: #fdfaf6;
  border-left: 4px solid var(--color-terracotta);
  border-radius: var(--radius-sm);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  border-top: 1px solid #fae8d8;
  border-right: 1px solid #fae8d8;
  border-bottom: 1px solid #fae8d8;
}

.arq-history-item {
  font-size: 0.93rem;
  line-height: 1.6;
  color: var(--color-secondary-dark);
}

.arq-history-item p {
  margin: 4px 0 0 0;
}

.arq-history-badge {
  display: inline-block;
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-terracotta);
  background: rgba(192, 86, 33, 0.12);
  padding: 3px 9px;
  border-radius: 4px;
}

/* Botón de llamada a la acción para más información en nueva ventana */
.arq-industry-action {
  margin-top: 6px;
}

.arq-btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #ffffff;
  color: var(--color-terracotta);
  border: 2px solid var(--color-terracotta);
  padding: 12px 24px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.94rem;
  text-decoration: none;
  min-height: 46px;
  transition: all 0.22s ease;
  box-shadow: 0 2px 6px rgba(192, 86, 33, 0.08);
}

.arq-btn-outline:hover {
  background: var(--color-terracotta);
  color: #ffffff !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(192, 86, 33, 0.25);
}

.arq-btn-outline svg {
  transition: transform 0.22s ease;
  flex-shrink: 0;
}

.arq-btn-outline:hover svg {
  transform: translate(2px, -2px);
}

@media (max-width: 900px) {
  .arq-industry-row,
  .arq-industry-row-reverse {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 26px 20px;
  }
  .arq-industry-row-reverse .arq-industry-media,
  .arq-industry-row .arq-industry-media {
    order: 1 !important;
  }
  .arq-industry-row-reverse .arq-industry-content,
  .arq-industry-row .arq-industry-content {
    order: 2 !important;
  }
  .arq-industry-showcase {
    gap: 32px;
  }
  .arq-btn-outline {
    width: 100%;
    justify-content: center;
  }
}
"""

    # Añadir CSS justo antes de </style> si no existe
    if ".arq-industry-showcase" not in html:
        style_close = "</style>"
        idx_style = html.find(style_close)
        if idx_style == -1:
            raise ValueError("No se encontró </style> en el HTML")
        html = html[:idx_style] + css_new + "\n" + html[idx_style:]

    # --- 2. HTML DE LA SECCIÓN REDISEÑADA ---
    new_arqueologia_section = """<section id="arqueologia" class="arq-section" style="background-color: #fbf9f5;">
    <div class="arq-container">
      <div class="arq-section-header">
        <span class="arq-section-pill pill-pine">Patrimonio del Trabajo • Espacios Productivos</span>
        <h2 class="arq-section-title">Arqueología Industrial y Espacios Productivos</h2>
        <p class="arq-section-desc">
          Más allá de las viviendas y los templos, Lastras de Cuéllar atesora un impresionante conjunto de infraestructuras auxiliares y artesanales que explican su próspera economía histórica campesina, resinera, alfarera y vitivinícola.
        </p>
      </div>

      <!-- Contenedor Showcase: 4 filas únicas -->
      <div class="arq-industry-showcase">

        <!-- FILA 1: BODEGAS SUBTERRÁNEAS -->
        <article class="arq-industry-row arq-industry-row-normal">
          <div class="arq-industry-media">
            <div class="arq-media-frame">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/bodegas-de-lastras-1536x864-1.jpeg" alt="Bodegas subterráneas tradicionales de Lastras de Cuéllar" loading="lazy" width="768" height="480">
            </div>
            <div class="arq-media-caption">
              <strong>Arquitectura Hipogea:</strong> Zarceras de piedra caliza y respiraderos que emergen sobre los taludes de Lastras de Cuéllar.
            </div>
          </div>
          <div class="arq-industry-content">
            <div class="arq-industry-header">
              <span class="arq-section-pill pill-wine">Cultura del Vino • Patrimonio Subterráneo</span>
              <h3 class="arq-industry-title">1. Las Bodegas Subterráneas: Cinco Siglos de Tradición Vitivinícola</h3>
            </div>
            <p class="arq-industry-text">
              Si existe un elemento distintivo en la arquitectura vernácula de Lastras frente a su entorno comarcal, es su monumental conjunto de bodegas excavadas en los taludes arcillosos. Un patrimonio subterráneo único en la provincia de Segovia, equiparable a las célebres villas vinícolas de la Ribera del Duero como Moradillo de Roa o Vadocondes.
            </p>
            <div class="arq-feature-list">
              <div class="arq-feature-item">
                <strong>Galerías Abovedadas:</strong> Excavadas a golpe de pico a más de 8 metros de profundidad, conservan de forma natural una temperatura estable de 12–14°C y humedad óptima constante durante todo el año.
              </div>
              <div class="arq-feature-item">
                <strong>Zarceras de Piedra:</strong> Singulares chimeneas troncocónicas de mampostería caliza que sobresalen del terreno para ventilar el peligroso gas "tufo" desprendido durante la fermentación del mosto.
              </div>
              <div class="arq-feature-item">
                <strong>Lagares y Sociabilidad:</strong> Prensas con monumentales vigas de roble y husillos de enebro, junto a portones de cuarterones con gateras, conformando el corazón social de peñas y cuadrillas.
              </div>
            </div>
            <div class="arq-industry-action">
              <a href="https://www.lastrasdecuellar.net/bodegas-de-lastras/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Más información sobre las bodegas de Lastras de Cuéllar (se abre en nueva ventana)">
                <span>Más información sobre las Bodegas</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>

        <!-- FILA 2: FÁBRICAS DE MIERA Y LA CHIMENEA DE CUCHIFRE -->
        <article class="arq-industry-row arq-industry-row-reverse">
          <div class="arq-industry-media">
            <div class="arq-media-frame">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/chimenea-lastras-de-cuellar-768x432-1.webp" alt="Chimenea octogonal de la Fábrica de Cuchifre en Lastras de Cuéllar" loading="lazy" width="768" height="432">
            </div>
            <div class="arq-media-caption">
              <strong>Faro de los Pinares:</strong> Chimenea octogonal de ladrillo de la Fábrica de Cuchifre, con cerca de 30 metros de altura.
            </div>
          </div>
          <div class="arq-industry-content">
            <div class="arq-industry-header">
              <span class="arq-section-pill pill-pine">Patrimonio Resinero • Oro Líquido del Pinar</span>
              <h3 class="arq-industry-title">2. Las Fábricas de Miera, El Cuchifre y el Horno Peguero</h3>
            </div>
            <p class="arq-industry-text">
              El siglo XX consolidó a Lastras de Cuéllar como uno de los centros neurálgicos de la transformación resinera en Castilla. La extracción de la miera en los extensos pinares albares y negrales nutrió una floreciente industria química que destilaba la esencia de trementina (aguarrás) y la colofonia sólida.
            </p>
            <div class="arq-feature-list">
              <div class="arq-feature-item">
                <strong>Doble Complejo Industrial:</strong> Lastras contó simultáneamente con dos grandes plantas fabriles ("La Resinera Segoviana" y "La Fábrica de Cuchifre"), situando al municipio en la vanguardia provincial de producción.
              </div>
              <div class="arq-feature-item">
                <strong>La Chimenea de Cuchifre:</strong> Esbelta estructura de planta octogonal erigida a finales de los años 40 por los célebres constructores valencianos de la saga Martínez, hoy hito paisajístico visible a decenas de kilómetros.
              </div>
              <div class="arq-feature-item">
                <strong>El Histórico Horno Peguero:</strong> En la calle de la Fábrica se conserva este arcaico horno cupuliforme por aproximación de hiladas donde se calcinaba la «roña» para obtener la pez impermeabilizante para barcos, cubas y botas.
              </div>
            </div>
            <div class="arq-industry-action">
              <a href="https://www.lastrasdecuellar.net/la-chimenea-de-cuchifre-y-las-fabricas-de-resina/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Más información sobre la chimenea de Cuchifre y las fábricas de resina (se abre en nueva ventana)">
                <span>Más información sobre las Fábricas de Miera</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>

        <!-- FILA 3: LOS ALFARES Y CACHARREROS VIEJOS -->
        <article class="arq-industry-row arq-industry-row-normal">
          <div class="arq-industry-media">
            <div class="arq-media-frame">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/alfareros-lastras-de-cuellar-1024x717.jpg" alt="Alfareros históricos trabajando en Lastras de Cuéllar" loading="lazy" width="768" height="538">
            </div>
            <div class="arq-media-caption">
              <strong>Maestría del Torno:</strong> Generaciones de alfareros lastreños moldeando cántaros, cazuelas y loza popular castellana.
            </div>
          </div>
          <div class="arq-industry-content">
            <div class="arq-industry-header">
              <span class="arq-section-pill pill-terracotta">Artesanía del Barro • Alfarería Popular</span>
              <h3 class="arq-industry-title">3. Los Alfares y el Oficio Centenario de los Cacharreros</h3>
            </div>
            <p class="arq-industry-text">
              La alfarería concedió un sello de auténtica singularidad a Lastras de Cuéllar. Frente a pueblos circundantes consagrados en exclusiva al campo o al monte, en Lastras florecieron sagas familiares alfareras (como los "Churretas" o "Parrilleras") que dominaron el torneado a pie y la cocción en hornos árabes de leña de pino.
            </p>
            <div class="arq-feature-list">
              <div class="arq-feature-item">
                <strong>Ciclo Artesano del Barro:</strong> Arcilla pura extraída en Los Barreros, laboriosa soba manual y moldeado de cántaros, botijos, pucheros para el fuego y cazuelas vidriadas con sulfuro de plomo ("alcohol de hoja").
              </div>
              <div class="arq-feature-item">
                <strong>Rutas y Trueque Castellano:</strong> Los cacharreros cargaban carros y bestias protegidos con serones de paja de centeno para acudir a ferias de Segovia, Valladolid y Ávila, trocando loza por trigo, centeno o legumbres.
              </div>
              <div class="arq-feature-item">
                <strong>Identidad Colectiva:</strong> Un oficio esforzado y tenaz que forjó la memoria afectiva y el carácter emprendedor de toda la comunidad lastreña.
              </div>
            </div>
            <div class="arq-industry-action">
              <a href="https://www.lastrasdecuellar.net/los-alfares-lastras-cuellar/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Más información sobre los alfares y cacharreros de Lastras (se abre en nueva ventana)">
                <span>Más información sobre los Alfares</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>

        <!-- FILA 4: LAS TEJERAS Y HORNOS DE TEJA -->
        <article class="arq-industry-row arq-industry-row-reverse">
          <div class="arq-industry-media">
            <div class="arq-media-frame">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/Photo604255802249_inner_39-55-980-26-50-706-980-706-copia-scaled.jpeg" alt="Extracción tradicional del barro y tejeras en Los Barreros de Lastras de Cuéllar" loading="lazy" width="768" height="553">
            </div>
            <div class="arq-media-caption">
              <strong>Hornos y Barreros:</strong> Extracción artesanal de arcilla en Los Barreros y tejeras históricas de Lastras de Cuéllar.
            </div>
          </div>
          <div class="arq-industry-content">
            <div class="arq-industry-header">
              <span class="arq-section-pill pill-amber">Industria Cerámica • Raíz Fundacional</span>
              <h3 class="arq-industry-title">4. Las Tejeras: Origen Histórico, Ordenanzas y Raíz de un Pueblo</h3>
            </div>
            <p class="arq-industry-text">
              La manufactura de teja curva y ladrillo cocido en hornos de doble cámara ("hormigueros") es una de las actividades industriales más venerables y documentadas de Lastras de Cuéllar, sustentada en tres niveles históricos irrebatibles:
            </p>

            <!-- Bloque Documental Histórico de 3 Niveles -->
            <div class="arq-history-box">
              <div class="arq-history-item">
                <span class="arq-history-badge">1. Referencia Documental Directa (1523)</span>
                <p>
                  El testamento del regidor de Cuéllar <strong>Martín López de Córdoba Hinestrosa</strong> (14 de enero de 1523) declara: <em>«Más otro horno de teja que yo tengo en La Lastra, tenido en cien mil maravedíes»</em>. Una cifra exorbitante que atestigua que ya a inicios del siglo XVI era una potente infraestructura industrial en la que invertía la élite comarcal.
                </p>
              </div>
              <div class="arq-history-item">
                <span class="arq-history-badge">2. Primera Regulación Oficial e Institucional (1546)</span>
                <p>
                  Las <strong>Ordenanzas de la Villa y Tierra de Cuéllar de 1546 (Ley 139)</strong> fijan minuciosamente la <em>«forma en que debían fabricar y vender las tejas y los ladrillos»</em>, consagrando a Lastras como el gran centro productor y suministrador para toda la Comunidad de Villa y Tierra.
                </p>
              </div>
              <div class="arq-history-item">
                <span class="arq-history-badge">3. Historiografía y Leyenda de los Orígenes</span>
                <p>
                  Sebastián Miñano (1826) registra en su diccionario la memoria de alfarería y tejeras fundadas por pobladores navarros atraídos por los materiales. Asimismo, la tradición oral vincula el nacimiento del pueblo a los artesanos de aldeas medievales (San Esteban y El Escobar) que moldeaban el barro en <strong>Los Barreros</strong> antes de establecerse en la loma de La Lastra.
                </p>
              </div>
            </div>

            <div class="arq-industry-action">
              <a href="https://www.lastrasdecuellar.net/los-barreros-y-la-extraccion-del-barro-arcilla/" target="_blank" rel="noopener noreferrer" class="arq-btn-outline" aria-label="Más información sobre los barreros y tejeras de Lastras (se abre en nueva ventana)">
                <span>Más información sobre las Tejeras y Barreros</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
          </div>
        </article>

      </div>

      <!-- Testimonios Agropecuarios Complementarios -->
      <div class="arq-accordion" style="margin-top: 52px;">
        <details class="arq-accordion-item">
          <summary>🏭 La Cooperativa de Transformación de la Achicoria «Sagrado Corazón» (1962)</summary>
          <div class="arq-accordion-content">
            Inaugurada solemnemente en 1962 con la visita del gobernador civil, la cooperativa agrupó a más de un centenar de agricultores locales. En la dura posguerra española, el secado y tostado de la achicoria como sustituto popular del café supuso un balón de oxígeno económico para decenas de familias lastreñas antes de la llegada de los cafés solubles en la década de los setenta.
          </div>
        </details>
        <details class="arq-accordion-item">
          <summary>🐑 Las Tenadas Pastoriles en «Los Cabañones» y «La Navazuela»</summary>
          <div class="arq-accordion-content">
            Edificaciones de planta rectangular con gruesos muros de piedra caliza sin labrar y cubiertas a dos aguas con vigas de enebro y pino. Servían de albergue comunal para las cabañas de ganado ovino trashumante y churro, protegiéndolas de lobos y de los temporales invernales de la meseta.
          </div>
        </details>
      </div>
    </div>
  </section>"""

    # Reemplazo de la sección arqueologia antigua
    m = re.search(r"(<section[^>]*id=[\"']arqueologia[\"'].*?</section>)", html, re.DOTALL)
    if not m:
        raise ValueError("Sección arqueologia no encontrada para reemplazar")

    old_section = m.group(1)
    html = html.replace(old_section, new_arqueologia_section)

    el_data[1]["elements"][0]["settings"]["html"] = html
    return el_data


def deploy(el_data):
    print(f"[*] Desplegando rediseño de Arqueología Industrial a WordPress: Página {PAGE_ID}...")
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
        print(f"[+] Estado de respuesta HTTP: {resp.status}")
        resp_json = json.loads(resp.read().decode("utf-8"))
        print(f"[+] Página actualizada correctamente: '{resp_json.get('title', {}).get('rendered')}'")

    # Purga de LiteSpeed Cache
    print(f"[*] Purgando LiteSpeed Cache para: {PAGE_URL}...")
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
    print(f"[*] Verificando contenido en vivo...")
    verify_req = urllib.request.Request(
        f"{PAGE_URL}?cache_bust=arq_ind_{PAGE_ID}",
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache"
        }
    )
    try:
        with urllib.request.urlopen(verify_req) as v_resp:
            content = v_resp.read().decode("utf-8")
            checks = [
                ("arq-industry-showcase", "Contenedor de 4 filas showcase"),
                ("bodegas-de-lastras", "Enlace a Bodegas"),
                ("la-chimenea-de-cuchifre-y-las-fabricas-de-resina", "Enlace a Fábricas de Miera"),
                ("los-alfares-lastras-cuellar", "Enlace a Alfares"),
                ("los-barreros-y-la-extraccion-del-barro-arcilla", "Enlace a Tejeras y Barreros"),
                ("Martín López de Córdoba", "Cita histórica de 1523"),
                ("Ordenanzas de la Villa y Tierra de Cuéllar de 1546", "Regulación de 1546")
            ]
            all_passed = True
            for needle, label in checks:
                if needle in content:
                    print(f"[+] VERIFICADO: '{label}' presente en vivo.")
                else:
                    print(f"[!] AVISO: No se detectó '{label}' en vivo.")
                    all_passed = False

            if all_passed:
                print("\n[🎉 ÉXITO TOTAL] Todas las 4 subsecciones e hitos históricos verificados en vivo.")
            else:
                print("\n[!] Algunas comprobaciones están pendientes de propagación de caché.")
    except Exception as e:
        print(f"[!] Error al verificar en vivo: {e}")


if __name__ == "__main__":
    updated_el_data = build_updated_data()
    print("[*] Árbol de elementos construido y validado localmente con éxito.")
    if "--deploy" in sys.argv:
        deploy(updated_el_data)
    else:
        print("[*] Modo de simulación completado con éxito. Ejecuta con '--deploy' para aplicar en vivo.")
