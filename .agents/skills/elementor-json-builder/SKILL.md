---
name: elementor-json-builder
description: >-
  Construcción, formateo y validación estructural del árbol JSON _elementor_data en Elementor 3.x+ usando Contenedores Flexbox y Grid modernos, IDs alfanuméricos únicos de 7 caracteres y prohibición estricta de layouts obsoletos section/column.
---

# Skill: Elementor JSON Builder (Contenedores Flexbox/Grid Modernos)

## 1. Propósito y Activación
- **Propósito**: Guiar a los agentes de Antigravity en la construcción, formateo y validación estructural del árbol JSON `_elementor_data` utilizando la arquitectura estándar y moderna de Contenedores Flexbox y Grid de Elementor 3.x+. Garantiza que no se generen layouts obsoletos basados en `section`/`column`, previene la corrupción de estructuras anidadas y asegura identificadores deterministas y válidos.
- **Cuándo invocar esta skill**:
  - Al crear una nueva página, plantilla o sección desde cero vía MCP.
  - Al reconstruir, transformar o inyectar bloques y widgets en páginas existentes.
  - Antes de realizar cualquier mutación que involucre el metadato `_elementor_data` o llamadas a herramientas como `elementor-manage-elements` o actualización de posts vía REST API.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-get-widget-schemas`: Para validar los campos soportados por cada widget antes de componer su `settings`.
  - `elementor-get-page-structure`: Para inspeccionar la jerarquía existente antes de aplicar mutaciones parciales.
  - `elementor-build-composition` / `elementor-manage-elements`: Para validar o inyectar nodos estructurales.
- **Entorno WordPress**:
  - Elementor Core >= 3.16 (con experimento `container` activo).
  - Codificación UTF-8 sin escapar entidades incompatibles con MySQL JSON/serialized strings.

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Arquitectura de Contenedores Única**:
   - Todo nodo estructural primario o secundario DEBE tener `elType: "container"`.
   - `isInner`: `false` para contenedores raíz / padres de sección; `true` para contenedores anidados dentro de otro contenedor.
2. **Generación de ID de Nodo de 7 Caracteres**:
   - Cada nodo (`container` o `widget`) DEBE poseer un `id` alfanumérico único de exactamente 7 caracteres en minúsculas y números (ejemplo: `^[a-z0-9]{7}$`, generado mediante hash o sampling hexadecimal/base36: `Math.random().toString(36).substring(2, 9)` o `uuid4().hex[:7]`).
   - Ningún ID puede repetirse dentro de la misma página o documento.
3. **Estructura Canónica de Nodo**:
   Todo objeto en el array raíz o en la propiedad `elements` DEBE contener estrictamente estas 5 claves:
   ```json
   {
     "id": "abc1234",
     "elType": "container" | "widget",
     "isInner": false,
     "settings": {},
     "elements": []
   }
   ```
   Si `elType === "widget"`, DEBE incluir la propiedad `"widgetType"` (ej. `"widgetType": "heading"`), y `"elements"` debe ser siempre un array vacío `[]`.
4. **Mapeo de Widgets Esenciales**:
   - `heading`:
     * Claves mínimas en `settings`: `title` (string), `header_size` (`h1`..`h6`, `div`, `span`, `p`), `align` (`left`, `center`, `right`, `justify`).
   - `text-editor`:
     * Claves mínimas en `settings`: `editor` (HTML sanitizado).
   - `image`:
     * Claves mínimas en `settings`: `image` (`{"url": "...", "id": 123}`), `image_size` (`large`, `full`, etc.).
   - `button`:
     * Claves mínimas en `settings`: `text`, `link` (`{"url": "...", "is_external": "", "nofollow": ""}`), `size` (`sm`, `md`, `lg`).
   - `icon-box`:
     * Claves mínimas en `settings`: `title_text`, `description_text`, `selected_icon` (`{"value": "fas fa-star", "library": "fa-solid"}`), `position` (`top`, `left`, `right`).

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO usar `elType: "section"` o `elType: "column"`**: La arquitectura legado genera conflictos de renderizado con temas y kits basados en Flexbox Container.
2. **PROHIBIDO omitir la clave `elements`**: Aun si un nodo no tiene hijos, `elements: []` es un requisito estricto del deserializador PHP de Elementor. Omitir `elements` causa un TypeError fatal en el frontend renderer.
3. **PROHIBIDO IDs nulos, duplicados o con longitudes distintas a 7 caracteres**: IDs con guiones, espacios o 36 caracteres (UUID completos) rompen la generación de hojas de estilo en el cache CSS de Elementor (`post-{id}.css`).
4. **PROHIBIDO inyectar HTML sucio o sin cerrar** dentro de `settings.editor` o `settings.title`.

---

## 4. Protocolo de Prevalidación Sintáctica

Antes de invocar cualquier herramienta de mutación o escritura en base de datos, el agente DEBE ejecutar esta validación sintáctica:

```
[Árbol JSON Generado]
       │
       ▼
1. ¿Es un Array JSON válido de objetos raíz? (No un objeto envuelto)
       │── NO ──► RECHAZAR: Fallo de estructura raíz
       ▼ SÍ
2. Validación Recursiva de Cada Nodo:
   - ¿Tiene `id` de 7 caracteres regex `^[a-z0-9]{7}$`?
   - ¿IDs únicos en todo el conjunto indexado?
   - ¿`elType` es exclusivamente "container" o "widget"?
   - Si `elType == "container"`: ¿`elements` es array? ¿No tiene `widgetType`?
   - Si `elType == "widget"`: ¿Tiene `widgetType` reconocido? ¿`elements.length === 0`?
       │── NO ──► RECHAZAR: Nodo corrupto
       ▼ SÍ
3. Validación de Settings por Widget:
   - ¿Tipos de datos correctos en settings de cada widgetType?
       │── NO ──► RECHAZAR: Settings inválidas
       ▼ SÍ
[APROBADO PARA INYECCIÓN VÍA MCP]
```

---

## 5. Ejemplo de Payload JSON Canónico

Estructura de un contenedor raíz Flexbox vertical con dos contenedores anidados (Layout Split con Texto y Botón):

```json
[
  {
    "id": "c1a9f02",
    "elType": "container",
    "isInner": false,
    "settings": {
      "content_width": "boxed",
      "flex_direction": "column",
      "flex_gap": {
        "unit": "px",
        "size": 32,
        "sizes": {}
      },
      "padding": {
        "unit": "px",
        "top": "48",
        "right": "24",
        "bottom": "48",
        "left": "24",
        "isLinked": false
      },
      "html_tag": "section"
    },
    "elements": [
      {
        "id": "e4b81c3",
        "elType": "widget",
        "isInner": false,
        "widgetType": "heading",
        "settings": {
          "title": "Innovación y Tradición en Lastras de Cuéllar",
          "header_size": "h2",
          "align": "center"
        },
        "elements": []
      },
      {
        "id": "d72ef41",
        "elType": "container",
        "isInner": true,
        "settings": {
          "content_width": "full",
          "flex_direction": "row",
          "flex_justify_content": "space-between",
          "flex_align_items": "center"
        },
        "elements": [
          {
            "id": "a93bc21",
            "elType": "widget",
            "isInner": false,
            "widgetType": "text-editor",
            "settings": {
              "editor": "<p>Descubre los eventos culturales y la actualidad de nuestra comarca con cobertura en directo.</p>"
            },
            "elements": []
          },
          {
            "id": "f81aa05",
            "elType": "widget",
            "isInner": false,
            "widgetType": "button",
            "settings": {
              "text": "Ver Programación",
              "link": {
                "url": "https://www.lastrasdecuellar.net/actualidad/",
                "is_external": false,
                "nofollow": false
              },
              "size": "md"
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
1. **Comprobación Estructural**: `json.loads(payload)` valida sin excepciones sintácticas.
2. **Inspección de Esquema**:
   - `0` nodos con `elType: "section"` o `"column"`.
   - `100%` de nodos con `id` coincidente con `^[a-z0-9]{7}$`.
   - `len(set(all_ids)) == len(all_ids)` (cero duplicados).
3. **Respuesta MCP Positiva**: La llamada a `elementor-manage-elements` o actualización de post devuelve estado HTTP `200` y confirmación de parseo de elementos por el core de Elementor.
