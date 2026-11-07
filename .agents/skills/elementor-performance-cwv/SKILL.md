---
name: elementor-performance-cwv
description: >-
  Optimización de Core Web Vitals (LCP, CLS, INP) en Elementor: control estricto de profundidad DOM (máximo 3 niveles de contenedores), carga prioritaria del Hero sin lazy-loading, aspect-ratio explícito e invalidación de caché LiteSpeed (UCSS).
---

# Skill: Elementor Performance & Core Web Vitals (CWV & DOM Optimization)

## 1. Propósito y Activación
- **Propósito**: Maximizar las métricas de rendimiento web (Core Web Vitals: LCP, CLS e INP), erradicar la sobrecarga del árbol DOM (*DOM Bloat*) provocada por anidamiento excesivo de contenedores en Elementor y coordinar la invalidación eficiente de caché con plugins de aceleración (LiteSpeed Cache / PageSpeed).
- **Cuándo invocar esta skill**:
  - Al estructurar árboles JSON de nuevas páginas o rediseñar secciones pesadas.
  - Al optimizar la sección Hero (cabecera visual) para acelerar el Largest Contentful Paint (LCP).
  - Al integrar vídeos incrustados, widgets de mapas o galerías de imágenes.
  - Al diagnosticar caídas en las puntuaciones de Google PageSpeed Insights o Google Lighthouse.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-get-page-structure`: Para calcular la profundidad máxima del árbol y contar el número total de nodos antes de aplicar cambios.
  - `elementor-clear-cache`: Para regenerar las hojas de estilo reducidas de Elementor.
  - REST API / Hooks de LiteSpeed Cache: Para purgar UCSS (Unique CSS) y Critical CSS tras mutaciones estructurales.
- **Límites de Rendimiento (Presupuesto Web)**:
  - **Profundidad de Contenedores**: Máximo 3 niveles (`Root Container` -> `Inner Container` -> `Widget`).
  - **Nodos DOM Totales**: Menos de 800 nodos por página (umbral crítico: 1.400 nodos según Google).
  - **LCP Target**: < 2.5 segundos.
  - **CLS Target**: < 0.1.

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Regla de Profundidad Máxima (Anti-DOM Bloat)**:
   - Los agentes NO deben anidar contenedores dentro de otros contenedores a más de 3 niveles de profundidad:
     * Nivel 1: Contenedor Raíz (`isInner: false`, ej. `<section>`).
     * Nivel 2: Contenedor Hijo de división o flex (`isInner: true`, ej. columnas o tarjetas).
     * Nivel 3: Contenedor Opcional exclusivo para grupos complejos de botones o tags.
     * Nivel 4+: ESTRICTAMENTE PROHIBIDO. Si se requiere alinear widgets, utilizar las propiedades de alineación nativas de Flexbox (`align-self`, `justify-content`) o clases utilitarias CSS en lugar de envolver cada widget en un nuevo contenedor.
2. **Optimización del Largest Contentful Paint (LCP)**:
   - La primera imagen visible del viewport (usualmente en la sección Hero) NUNCA debe cargarse con lazy loading diferido.
   - Si el Hero usa un widget de imagen o fondo:
     * Asignar prioridad alta (`fetchpriority="high"`).
     * Formato web moderno obligatorio: `.webp` o `.avif` comprimido (peso menor a 150 KB para desktop y 70 KB para móvil).
3. **Erradicación del Cumulative Layout Shift (CLS)**:
   - Todo widget de imagen, icono o elemento multimedia DEBE declarar dimensiones explícitas o relación de aspecto (`aspect_ratio`):
     ```json
     "aspect_ratio": "16:9" | "4:3" | "1:1"
     ```
   - Si se insertan iframes de YouTube o Vimeo, activar siempre la opción nativa de Elementor `"lazy_load": "yes"` e `"image_overlay": "yes"` para evitar que la carga síncrona del reproductor externo bloquee el hilo principal (Main Thread).
4. **Coordinación con LiteSpeed Cache**:
   - Tras mutar una página y llamar a `elementor-clear-cache`, si el entorno tiene activo LiteSpeed Cache, se debe purgar la caché de página (`Purge All - LSCache`) o invalidar el recurso UCSS específico de la página.

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO Contenedores Fantasma o Redundantes**:
   - No crear un contenedor cuyo único propósito sea envolver un único widget hijo sin aportar estilos de fondo, borde o padding imprescindibles.
2. **PROHIBIDO Fuentes Externas Múltiples**:
   - No añadir familias tipográficas de Google Fonts ad-hoc. Utilizar únicamente las familias declaradas en el Kit activo para evitar solicitudes DNS y peticiones de fuentes bloqueantes.
3. **PROHIBIDO Animaciones Pesadas en Pantallas Móviles**:
   - Evitar `entrance_animation` (FadeIn, SlideIn, Bounce) en cascada en todos los widgets. Las animaciones basadas en JavaScript recalculan continuamente el layout en móviles de gama media/baja disparando el INP (Interaction to Next Paint).
4. **PROHIBIDO Carga de Scripts en Widgets HTML**:
   - NUNCA inyectar scripts síncronos de terceros (`<script src="https://..."></script>`) dentro de widgets `html` sin el atributo `defer` o `async`.

---

## 4. Diagrama de Arquitectura de Contenedores Ligera

```
[MALA PRÁCTICA: DOM Bloat (6 niveles)]           [BUENA PRÁCTICA: DOM Optimizado (2 niveles)]
Root Container (Section)                         Root Container (Section)
 └── Sub Container (Wrapper)                      ├── Widget: Heading (align: center)
      └── Inner Container (Column)                └── Sub Container (Grid / Flex Row)
           └── Card Container                          ├── Card 1 (Article) -> Image + Title + Button
                └── Text Container                     └── Card 2 (Article) -> Image + Title + Button
                     └── Widget: Heading
```

---

## 5. Ejemplo de Payload JSON Altamente Optimizado para CWV

Sección Hero con LCP optimizado, aspect ratio explícito, sin contenedores fantasma y con imagen de fondo liviana:

```json
[
  {
    "id": "cwvhero",
    "elType": "container",
    "isInner": false,
    "settings": {
      "html_tag": "header",
      "content_width": "boxed",
      "flex_direction": "column",
      "flex_justify_content": "center",
      "flex_align_items": "center",
      "padding": {
        "unit": "px",
        "top": "80",
        "right": "24",
        "bottom": "80",
        "left": "24",
        "isLinked": false
      },
      "padding_mobile": {
        "unit": "px",
        "top": "40",
        "right": "16",
        "bottom": "40",
        "left": "16",
        "isLinked": false
      }
    },
    "elements": [
      {
        "id": "cwvtopt",
        "elType": "widget",
        "isInner": false,
        "widgetType": "heading",
        "settings": {
          "title": "Portal Oficial de Lastras de Cuéllar",
          "header_size": "h1",
          "align": "center",
          "title_color": "",
          "__globals__": {
            "title_color": "globals/colors?id=primary",
            "typography_typography": "globals/typography?id=primary"
          }
        },
        "elements": []
      },
      {
        "id": "cwvsubt",
        "elType": "widget",
        "isInner": false,
        "widgetType": "text-editor",
        "settings": {
          "editor": "<p>Información municipal, historia viva, turismo sostenible y servicios públicos en el corazón de Segovia.</p>",
          "align": "center"
        },
        "elements": []
      },
      {
        "id": "cwvmedia",
        "elType": "widget",
        "isInner": false,
        "widgetType": "image",
        "settings": {
          "image": {
            "url": "https://www.lastrasdecuellar.net/wp-content/uploads/2026/11/panoramica-lastras-hero.webp",
            "id": 26855,
            "alt": "Vista panorámica de Lastras de Cuéllar rodeada de pinares"
          },
          "image_size": "large",
          "aspect_ratio": "16:9",
          "align": "center"
        },
        "elements": []
      }
    ]
  }
]
```

---

## 6. Criterio de Validación de Éxito
1. **Auditoría de Profundidad de Árbol**:
   - `profundidad_maxima(json_tree) <= 3`. Ninguna rama supera 3 contenedores anidados.
2. **Verificación de Ratio de Contenedores/Widgets**:
   - El ratio `total_widgets / total_containers >= 1.2` (no hay más contenedores que contenido real).
3. **Cumplimiento de Buenas Prácticas Multimedia**:
   - `0` widgets de tipo `video` sin `image_overlay` habilitado.
   - `100%` de las imágenes del Hero con tamaño nativo `.webp`/`.avif` con peso optimizado.
