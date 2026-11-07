---
name: elementor-dynamic-tags
description: >-
  Mapeo e integración de tags dinámicos (__dynamic__) y Theme Builder de Elementor con posts, páginas, taxonomías y campos de WordPress para plantillas single, archive, search y bucles dinámicos (loop grids).
---

# Skill: Elementor Dynamic Tags & Loop Architecture (CPT & CMS Integration)

## 1. Propósito y Activación
- **Propósito**: Estandarizar la vinculación de plantillas y widgets de Elementor con la base de datos de contenidos vivos de WordPress (entradas, páginas, Custom Post Types, campos personalizados ACF/Pods y taxonomías), evitando textos o imágenes estáticas hardcodeadas en plantillas reutilizables del Theme Builder.
- **Cuándo invocar esta skill**:
  - Al diseñar o modificar plantillas de Theme Builder: `single` (entradas individuales), `archive` (listados de categorías/etiquetas) o `search` (resultados de búsqueda).
  - Al implementar cuadrículas dinámicas de contenido mediante widgets `posts`, `loop-grid` o `portfolio`.
  - Al requerir datos contextuales como autor, fecha de publicación, número de comentarios o campos meta de WordPress.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-list-posts`: Para listar posts de muestra y verificar que las taxonomías o post types existen.
  - `elementor-get-widget-schemas`: Para validar los esquemas de widgets dinámicos (`theme-post-title`, `theme-post-content`, `theme-post-featured-image`, `posts`, `loop-grid`).
  - `elementor-manage-site-parts`: Para asociar plantillas a las condiciones de visualización adecuadas (`include/archive`, `include/singular`).

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Uso del Objeto `__dynamic__` para Enlaces y Valores Nativos**:
   - Todo campo textual o enlace que deba extraerse del post actual DEBE declararse en el sub-objeto `__dynamic__` dentro de `settings`:
     * Título dinámico:
       ```json
       "__dynamic__": {
         "title": "[elementor-tag id=\"...\" name=\"post-title\"]"
       }
       ```
     * Enlace a la entrada:
       ```json
       "__dynamic__": {
         "link": "[elementor-tag id=\"...\" name=\"post-url\"]"
       }
       ```
     * Imagen destacada:
       ```json
       "__dynamic__": {
         "image": "[elementor-tag id=\"...\" name=\"post-featured-image\"]"
       }
       ```
2. **Definición de Valores de Respaldo (*Fallbacks*)**:
   - Todo tag dinámico que dependa de campos que puedan estar vacíos (ej. `post-excerpt` o campos personalizados de metadatos) DEBE incluir un valor de respaldo (`fallback`) en sus parámetros o en `settings` para evitar renders rotos o bloques en blanco.
3. **Configuración Eficiente de Widgets de Consulta (`posts` / `loop-grid`)**:
   - **Paginación obligatoria**: Todo widget de listado con más de 6 elementos debe tener activada la paginación (`pagination_type: "numbers"` o `"load_more_on_click"`) para evitar consultas MySQL pesadas de 100+ posts en el frontend.
   - **Exclusión de Post Actual**: En widgets de "Artículos relacionados" dentro de una plantilla `single`, DEBE incluirse `"query_exclude": "current_post"`.
   - **Filtro por Post Type explícito**: Definir explícitamente `"query_post_type": "post"` (o el CPT correspondiente), nunca dejarlo indeterminado.

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO Contenido Estático en Plantillas Theme Builder**:
   - NUNCA escribir un título estático (ej. `"Noticia de Ejemplo"`) en el widget `heading` de una plantilla `single-post`. Si se edita la plantilla, todos los artículos mostrarían el mismo título. Usar siempre el widget dedicado `theme-post-title` o un `heading` con tag dinámico.
2. **PROHIBIDO IDs de Elementor Tags Inválidos**:
   - No inventar cadenas al azar dentro de `[elementor-tag ...]` sin el hash o ID generado por la API de Elementor. Cuando no se use la macro de shortcode, preferir los widgets nativos de tema de Elementor Pro (`widgetType: "theme-post-title"`, `"theme-post-featured-image"`, `"theme-post-content"`).
3. **PROHIBIDO Consultas Sin Límite (`posts_per_page: -1`)**:
   - Consultas con valor `-1` o superiores a 20 entradas en páginas principales causan saturación de memoria PHP y bloqueos de CPU en WordPress.

---

## 4. Mapeo de Widgets de Tema vs Widgets Estándar Dinámicos

| Elemento Dinámico | Opción A: Widget Nativo de Tema (Recomendado) | Opción B: Widget Estándar + `__dynamic__` |
| :--- | :--- | :--- |
| **Título del Post** | `widgetType: "theme-post-title"` | `widgetType: "heading"` + tag `post-title` |
| **Imagen Destacada** | `widgetType: "theme-post-featured-image"` | `widgetType: "image"` + tag `post-featured-image` |
| **Cuerpo de la Noticia**| `widgetType: "theme-post-content"` | N/A (Solo widget de tema) |
| **Metadatos (Fecha/Autor)**| `widgetType: "post-info"` | `widgetType: "text-editor"` + tag `post-date` |
| **Extracto / Resumen**| `widgetType: "theme-post-excerpt"` | `widgetType: "text-editor"` + tag `post-terms` |

---

## 5. Ejemplo de Payload JSON para Plantilla Single Post Reutilizable

Estructura canónica de cabecera de entrada con título dinámico, información de publicación e imagen destacada:

```json
[
  {
    "id": "dynsng1",
    "elType": "container",
    "isInner": false,
    "settings": {
      "html_tag": "header",
      "content_width": "boxed",
      "flex_direction": "column",
      "flex_gap": {
        "unit": "px",
        "size": 24,
        "sizes": {}
      },
      "padding": {
        "unit": "px",
        "top": "48",
        "right": "24",
        "bottom": "32",
        "left": "24",
        "isLinked": false
      }
    },
    "elements": [
      {
        "id": "dyntit1",
        "elType": "widget",
        "isInner": false,
        "widgetType": "theme-post-title",
        "settings": {
          "header_size": "h1",
          "title_color": "",
          "__globals__": {
            "title_color": "globals/colors?id=primary",
            "typography_typography": "globals/typography?id=primary"
          }
        },
        "elements": []
      },
      {
        "id": "dyninf1",
        "elType": "widget",
        "isInner": false,
        "widgetType": "post-info",
        "settings": {
          "layout": "inline",
          "show_meta": ["author", "date", "comments"],
          "icon_align": "left"
        },
        "elements": []
      },
      {
        "id": "dynimg1",
        "elType": "widget",
        "isInner": false,
        "widgetType": "theme-post-featured-image",
        "settings": {
          "image_size": "large",
          "aspect_ratio": "16:9",
          "border_radius": {
            "unit": "px",
            "top": "12",
            "right": "12",
            "bottom": "12",
            "left": "12",
            "isLinked": true
          }
        },
        "elements": []
      }
    ]
  }
]
```

---

## 6. Criterio de Validación de Éxito
1. **Auditoría de Plantillas Theme Builder**:
   - Si `_elementor_template_type` es `"single"` o `"single-post"`, el árbol JSON DEBE contener widgets nativos (`theme-post-title`, `theme-post-content`) o etiquetas dinámicas verificables en `__dynamic__`.
2. **Validación de Consultas (`query`)**:
   - `0` widgets de tipo `posts` con `posts_per_page` igual a `-1` o ausente.
   - Presencia confirmada de `query_exclude: "current_post"` en widgets de recomendación interna.
3. **Renderizado de Contenido Real**:
   - Al consultar la URL renderizada en el frontend de un post real, el título de la página coincide con `post.post_title` de la base de datos de WordPress y no con valores estáticos de prueba.
