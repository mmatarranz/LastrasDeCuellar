---
name: elementor-seo-semantic
description: >-
  Garantizar que todas las páginas y plantillas de Elementor cumplan con jerarquía semántica HTML5 pura (header, section, article, main, aside), exactamente un solo H1 por página, atributos alt obligatorios y accesibilidad WCAG 2.1 AA.
---

# Skill: Elementor SEO & Semántica HTML Estricta

## 1. Propósito y Activación
- **Propósito**: Garantizar que todas las estructuras y elementos generados o modificados en Elementor cumplan con las directrices más exigentes de SEO técnico On-Page, accesibilidad web (WCAG 2.1 AA) y jerarquía semántica HTML5 pura.
- **Cuándo invocar esta skill**:
  - Al diseñar nuevas páginas de aterrizaje, entradas de blog, hubs de contenido o plantillas temáticas.
  - Al insertar o editar contenedores estructurales (`container`) y widgets de contenido (`heading`, `image`, `text-editor`).
  - Durante auditorías automatizadas previas a la publicación definitiva de un documento en WordPress.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-get-page-structure`: Para escanear el árbol completo y comprobar cuántos H1 existen actualmente en la página.
  - `elementor-list-assets` / `elementor-upload-media`: Para verificar los metadatos de imágenes subidas a la biblioteca de medios (`alt_text`, `title`, dimensiones).
  - `elementor-manage-elements`: Para inyectar la configuración semántica de contenedores y widgets.

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Etiquetado Semántico Explícito en Contenedores (`html_tag`)**:
   - Todo contenedor de nivel superior (raíz) DEBE definir obligatoriamente la propiedad `settings.html_tag` acorde a su función:
     * `header`: Para cabeceras de página, héroes principales o banners superiores del sitio.
     * `section`: Para secciones temáticas discretas del contenido (noticias, historia, galería, servicios).
     * `article`: Para tarjetas de noticias independientes, entradas de blog, testimonios o posts en grids.
     * `main`: Exclusivo para el contenedor envolvente de contenido principal cuando no lo gestione el tema padre.
     * `footer`: Para pies de página o bloques de cierre de documento.
     * `nav`: Para barras o listas de enlaces de navegación interna.
     * `aside`: Para barras laterales o bloques complementarios con enlaces relacionados.
   - En contenedores puramente decorativos o de ajuste interno de flexbox, utilizar `div`.
2. **Jerarquía Rigurosa de Encabezados (H1 - H6)**:
   - **Regla Estricta del H1 Único**: Debe haber **exactamente un único H1** por página. Si la plantilla de tema ya inyecta el `h1` mediante el título del post/página, los widgets de Elementor deben comenzar en `h2`.
   - **Orden Descendente Secuencial**: No se permite saltar niveles de jerarquía (ej. de `h2` pasar a `h4` sin un `h3` intermedio).
   - **Tarjetas y Bento Grids**: Los títulos dentro de tarjetas repetidas o módulos de grid deben tiparse como `h3` o `h4`, nunca `h2` si están subordinados a un título de sección `h2`.
   - En el widget `heading`, la etiqueta se establece mediante `"header_size": "h1" | "h2" | "h3" | "h4" | "h5" | "h6"`.
3. **Optimización Semántica y Rendimiento en Widgets de Imagen (`image`)**:
   - **Atributo `alt` no vacío**: El campo `alt` DEBE ser descriptivo, libre de keyword stuffing y en el idioma del sitio (español). Si la imagen es puramente decorativa, debe marcarse expresamente con intención decorativa o quedar documentado.
   - **Tamaños Nativos de WordPress**:
     * PROHIBIDO dejar el tamaño en blanco o forzar redimensiones arbitrarias en CSS.
     * Seleccionar siempre un tamaño registrado:
       - `"image_size": "full"` -> Solo para héroes panorámicos de alta fidelidad o fondos nítidos.
       - `"image_size": "large"` -> Para imágenes de cabecera de artículos y banners medianos (1024px max).
       - `"image_size": "medium_large"` -> Para tarjetas de noticias, bento grids y columnas dobles (768px max).
       - `"image_size": "thumbnail"` -> Para avatares, iconos o miniaturas compactas (150x150).

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO múltiples etiquetas `h1`**: Detectar dos o más widgets con `header_size: "h1"` es motivo de detención inmediata del despliegue.
2. **PROHIBIDO dejar `html_tag: "div"` en todos los contenedores raíz**: El "div-soup" penaliza el ranking de accesibilidad (Lighthouse Accessibility) y comprensión por rastreadores web.
3. **PROHIBIDO usar `heading` simplemente para estilizar visualmente texto pequeño**: Si un texto requiere tamaño destacado pero no es un encabezado jerárquico, se debe usar `header_size: "p"` o `"span"` con clases de utilidad tipográfica, manteniendo intacto el outline del documento.
4. **PROHIBIDO imágenes con URL directa externa sin ID de medio (`image.id`)**: Las imágenes huérfanas sin ID de medio en WordPress impiden la generación de atributos nativos `srcset` y `sizes`, destruyendo las métricas Core Web Vitals (LCP).

---

## 4. Matriz de Decisión Semántica

```
¿Qué función cumple este nodo contenedor?
├── ¿Es el Hero / Cabecera principal del documento? ──► html_tag: "header"
├── ¿Es un bloque temático de la página? (ej. Actualidad) ──► html_tag: "section"
│   └── ¿Dentro hay tarjetas de post individuales? ──► html_tag: "article"
│       └── ¿El título de la tarjeta? ──► widget: heading (header_size: "h3")
├── ¿Es una barra lateral de widgets o accesos? ──► html_tag: "aside"
└── ¿Es solo un wrapper para centrar o alinear botones? ──► html_tag: "div"
```

---

## 5. Ejemplo de Payload JSON Semántico y Accesible

Estructura de una sección de noticias con contenedor raíz `<section>`, encabezado `H2`, y tarjeta interna `<article>` con imagen optimizada y título `H3`:

```json
[
  {
    "id": "s81be01",
    "elType": "container",
    "isInner": false,
    "settings": {
      "html_tag": "section",
      "content_width": "boxed",
      "flex_direction": "column"
    },
    "elements": [
      {
        "id": "h2sec01",
        "elType": "widget",
        "isInner": false,
        "widgetType": "heading",
        "settings": {
          "title": "Últimas Noticias de la Villa",
          "header_size": "h2"
        },
        "elements": []
      },
      {
        "id": "art0001",
        "elType": "container",
        "isInner": true,
        "settings": {
          "html_tag": "article",
          "flex_direction": "column",
          "content_width": "full"
        },
        "elements": [
          {
            "id": "img0001",
            "elType": "widget",
            "isInner": false,
            "widgetType": "image",
            "settings": {
              "image": {
                "url": "https://www.lastrasdecuellar.net/wp-content/uploads/2026/11/fiestas-lastras.webp",
                "id": 26840,
                "alt": "Plaza Mayor de Lastras de Cuéllar durante la celebración de las fiestas tradicionales"
              },
              "image_size": "medium_large",
              "caption_source": "none"
            },
            "elements": []
          },
          {
            "id": "h3crd01",
            "elType": "widget",
            "isInner": false,
            "widgetType": "heading",
            "settings": {
              "title": "Celebración de la festividad de San Isidro Labrador",
              "header_size": "h3"
            },
            "elements": []
          },
          {
            "id": "txt0001",
            "elType": "widget",
            "isInner": false,
            "widgetType": "text-editor",
            "settings": {
              "editor": "<p>Los vecinos y visitantes se reunieron en la pradera para la tradicional procesión y posterior comida campestre.</p>"
            },
            "elements": []
          }
        ]
      }
    ]
  }
]
```

---

## 6. Criterio de Validación de Éxito
1. **Conteo Estricto de Encabezados**:
   - `conteo(header_size == "h1") <= 1` en todo el documento JSON.
   - Progresión matemática válida en niveles H (no hay saltos de `h2` a `h4`).
2. **Conformidad de Contenedores**:
   - Todo contenedor de nivel 0 (`isInner: false`) tiene `html_tag in ["header", "section", "article", "main", "footer", "aside"]`.
3. **Auditoría de Imágenes**:
   - Cada nodo `widgetType: "image"` tiene `settings.image.alt` con longitud mínima > 10 caracteres y `settings.image_size` con valor normalizado de WP (`thumbnail`, `medium`, `medium_large`, `large`, `full`).
