---
name: elementor-responsive-breakpoints
description: >-
  Directrices de diseño Mobile-First y control de breakpoints en Elementor: flex_direction_mobile column, paddings adaptativos, tipografía fluida y prevención de desbordamiento horizontal (horizontal overflow < 768px).
---

# Skill: Elementor Responsive & Breakpoints Matrix (Mobile-First Architecture)

## 1. Propósito y Activación
- **Propósito**: Garantizar que todas las interfaces, contenedores y widgets generados por agentes de Antigravity en Elementor se adapten de forma fluida y sin desbordamientos a todos los dispositivos, aplicando principios Mobile-First y controlando rigurosamente los breakpoints de pantalla (Mobile, Tablet, Desktop y Laptop/Widescreen).
- **Cuándo invocar esta skill**:
  - Al definir la dirección flexbox, espaciados (padding/margin), tamaños tipográficos y visibilidad de cualquier elemento.
  - Al diseñar layouts con más de una columna o tarjeta (grids, bento boxes, split headers).
  - Al auditar páginas existentes para eliminar el desbordamiento horizontal (*horizontal overflow*) en dispositivos móviles.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-get-page-structure`: Para inspeccionar las propiedades responsive preexistentes en los contenedores.
  - `elementor-get-widget-schemas`: Para validar qué controles soportan los modificadores `_mobile` y `_tablet`.
  - `elementor-create-preview-link`: Para generar la URL de previsualización que permita validar la responsividad en diferentes viewports.
- **Breakpoints Estándar de Elementor**:
  - **Mobile**: `< 768px` (referencia base de prueba: 360px - 414px).
  - **Tablet**: `768px - 1024px` (referencia base de prueba: 768px - 820px).
  - **Desktop**: `> 1024px` (referencia base: 1200px - 1440px).

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Regla de Conversión Flexbox para Móvil**:
   - Todo contenedor con `"flex_direction": "row"` en Desktop DEBE incluir explícitamente `"flex_direction_mobile": "column"`, salvo que se trate de una barra de botones compacta o tags horizontales con scroll permitido.
   - En layouts de 2 o más columnas, definir siempre `"flex_wrap": "wrap"` o `"flex_direction_mobile": "column"`.
2. **Escala de Espaciados Responsive (Paddings & Margins)**:
   - Los paddings laterales superiores a 32px en desktop deben reducirse obligatoriamente en móvil:
     * Desktop: `padding` lateral habitual de 32px a 80px.
     * Mobile (`padding_mobile`): estrictamente entre `12px` y `20px` (máximo `24px` en pantallas grandes).
   - Mantener `isLinked: false` cuando se requiera distinto espaciado vertical u horizontal.
3. **Tipografía Fluida y Adaptada a Viewport**:
   - En encabezados principales (`h1` y `h2`), definir siempre el tamaño adaptado para móvil mediante `font_size_mobile`:
     * H1: Desktop `38px - 56px` -> Mobile `26px - 34px`.
     * H2: Desktop `28px - 38px` -> Mobile `22px - 26px`.
     * Párrafos (`text-editor`): Desktop `16px - 18px` -> Mobile `15px - 16px` (nunca inferior a `14px` por accesibilidad).
4. **Visibilidad y Ocultación Condicional Limpia**:
   - Para ocultar elementos decorativos pesados o irrelevantes en móvil, usar los controles nativos de responsive:
     * `"hide_mobile": "hidden-mobile"`
     * `"hide_tablet": "hidden-tablet"`
     * `"hide_desktop": "hidden-desktop"`
5. **Gaps y Espaciados de Cuadrícula**:
   - Reducir `flex_gap_mobile` a la mitad o tercio del desktop (ej. Desktop `32px` -> Mobile `16px`).

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO anchos fijos en píxeles (`width: "600px"`, `min_width: "500px"`)**:
   - Los anchos rígidos en píxeles son la causa #1 de desbordamiento horizontal en smartphones. Usar porcentajes (`width: "100%"`), unidades relativas (`vw`, `rem`) o `content_width: "full"`.
2. **PROHIBIDO márgenes negativos agresivos sin contrapartida en móvil**:
   - Si se usa un margen negativo en desktop (ej. `-40px` para solapar un hero), DEBE restablecerse en móvil a `0px` (`margin_mobile: { "top": "0", ... }`) para no romper el flujo natural del scroll.
3. **PROHIBIDO elementos flotantes con scroll lateral involuntario**:
   - Si un contenedor interno utiliza un ancho mayor al 100% o scroll horizontal deliberado (ej. carrusel de tarjetas), el contenedor padre DEBE definir `"overflow": "hidden"` o clases específicas de carrusel swipe.

---

## 4. Matriz de Propiedades Clave Responsive en Elementor JSON

| Propiedad Base (Desktop) | Sufijo Móvil (`settings`) | Sufijo Tablet (`settings`) | Valores Recomendados Móvil |
| :--- | :--- | :--- | :--- |
| `flex_direction` | `flex_direction_mobile` | `flex_direction_tablet` | `"column"` |
| `flex_align_items` | `flex_align_items_mobile` | `flex_align_items_tablet` | `"stretch"` o `"center"` |
| `flex_justify_content` | `flex_justify_content_mobile` | `flex_justify_content_tablet` | `"center"` o `"flex-start"` |
| `flex_gap` | `flex_gap_mobile` | `flex_gap_tablet` | `{"unit": "px", "size": 16}` |
| `padding` | `padding_mobile` | `padding_tablet` | `top/bottom: 24-32px`, `left/right: 16px` |
| `margin` | `margin_mobile` | `margin_tablet` | Reset a `0` si había offset negativo |
| `font_size` (en tipografía) | `font_size_mobile` | `font_size_tablet` | Reducción de 25% a 40% respecto a desktop |
| `content_width` | `content_width_mobile` | `content_width_tablet` | `"full"` o `"boxed"` con 100% width |

---

## 5. Ejemplo de Payload JSON con Configuración Responsive Completa

Contenedor de 2 columnas (Texto a la izquierda, Tarjeta a la derecha) que conmuta fluidamente a columna única vertical en móviles:

```json
[
  {
    "id": "rspc001",
    "elType": "container",
    "isInner": false,
    "settings": {
      "content_width": "boxed",
      "flex_direction": "row",
      "flex_direction_tablet": "column",
      "flex_direction_mobile": "column",
      "flex_justify_content": "space-between",
      "flex_align_items": "center",
      "flex_gap": {
        "unit": "px",
        "size": 40,
        "sizes": {}
      },
      "flex_gap_mobile": {
        "unit": "px",
        "size": 20,
        "sizes": {}
      },
      "padding": {
        "unit": "px",
        "top": "64",
        "right": "32",
        "bottom": "64",
        "left": "32",
        "isLinked": false
      },
      "padding_mobile": {
        "unit": "px",
        "top": "32",
        "right": "16",
        "bottom": "32",
        "left": "16",
        "isLinked": false
      },
      "html_tag": "section"
    },
    "elements": [
      {
        "id": "rspcol1",
        "elType": "container",
        "isInner": true,
        "settings": {
          "content_width": "full",
          "width": {
            "unit": "%",
            "size": 55,
            "sizes": {}
          },
          "width_mobile": {
            "unit": "%",
            "size": 100,
            "sizes": {}
          },
          "flex_direction": "column"
        },
        "elements": [
          {
            "id": "rsptit1",
            "elType": "widget",
            "isInner": false,
            "widgetType": "heading",
            "settings": {
              "title": "Vive la Semana Cultural de Lastras",
              "header_size": "h2",
              "title_color": "",
              "__globals__": {
                "title_color": "globals/colors?id=primary"
              }
            },
            "elements": []
          },
          {
            "id": "rspdesc",
            "elType": "widget",
            "isInner": false,
            "widgetType": "text-editor",
            "settings": {
              "editor": "<p>Conciertos, exposiciones fotográficas y gastronomía tradicional durante siete días de celebración popular.</p>"
            },
            "elements": []
          }
        ]
      },
      {
        "id": "rspcol2",
        "elType": "container",
        "isInner": true,
        "settings": {
          "content_width": "full",
          "width": {
            "unit": "%",
            "size": 40,
            "sizes": {}
          },
          "width_mobile": {
            "unit": "%",
            "size": 100,
            "sizes": {}
          },
          "padding": {
            "unit": "px",
            "top": "24",
            "right": "24",
            "bottom": "24",
            "left": "24",
            "isLinked": true
          },
          "background_background": "classic",
          "border_radius": {
            "unit": "px",
            "top": "12",
            "right": "12",
            "bottom": "12",
            "left": "12",
            "isLinked": true
          }
        },
        "elements": [
          {
            "id": "rspbtn1",
            "elType": "widget",
            "isInner": false,
            "widgetType": "button",
            "settings": {
              "text": "Descargar Programa en PDF",
              "size": "md",
              "align": "center",
              "align_mobile": "justify",
              "link": {
                "url": "https://www.lastrasdecuellar.net/programa-cultural.pdf",
                "is_external": true,
                "nofollow": false
              }
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
1. **Auditoría de Ancho y Overflow**:
   - `0` instancias de `width` en píxeles (`unit: "px"`) en contenedores estructurales.
   - En una resolución de pantalla de 375px (iPhone standard), el ancho total renderizado del body no supera los 375px (`document.body.scrollWidth === window.innerWidth`).
2. **Conformidad de Contenedores Multicolumna**:
   - `100%` de los contenedores con `flex_direction: "row"` en desktop poseen su correspondiente definición `flex_direction_mobile: "column"` o `flex_wrap: "wrap"`.
3. **Legibilidad Tipográfica**:
   - En pantallas móviles, ningún párrafo posee `font_size` menor a 14px ni interlineado (`line-height`) inferior a 1.4em.
