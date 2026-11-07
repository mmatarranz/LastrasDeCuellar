---
name: elementor-design-system
description: >-
  Vincular estilos de color, tipografía y diseño a los tokens globales del Kit activo de Elementor (__globals__ y var(--e-global-*)), prohibiendo valores hexadecimales o familias tipográficas inline hardcodeadas.
---

# Skill: Elementor Design System (Global Tokens & Active Kit Sync)

## 1. Propósito y Activación
- **Propósito**: Garantizar la coherencia visual, mantenibilidad y adhesión estricta a la identidad de marca del sitio, vinculando todos los colores, tipografías y sombras a las variables globales del Kit activo de Elementor (`elementor_active_kit`).
- **Cuándo invocar esta skill**:
  - Antes de definir estilos de color, fuentes, márgenes, bordes o fondos en cualquier widget o contenedor.
  - Al generar nuevos componentes visuales, banners, botones, tarjetas (cards) o secciones editoriales.
  - Al refactorizar estilos heredados que contengan códigos hexadecimales arbitrarios o declaraciones inline dispersas.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-read-resource` / `elementor-list-resources`: Con URI `elementor://site-settings` o inspección de post de kit activo para leer los tokens globales registrados.
  - `elementor-manage-global-variable`: Para consultar o declarar tokens de color y tipografía globales si fuese necesario.
  - `elementor-get-default-styles`: Para conocer las asignaciones predeterminadas de contenedores y widgets.
- **Identificación de Kit**:
  - Obtener el ID del Kit activo leyendo la opción `elementor_active_kit` de WordPress (típicamente consultable en `wp_options` o a través de las tools de site-settings de Elementor).

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Inspección Previa del Kit**:
   - Todo agente DEBE consultar primero el mapa de colores y tipografías del kit activo antes de escribir un solo nodo de diseño.
   - Las 4 jerarquías tipográficas del sistema global son:
     * `Primary` (`--e-global-typography-primary` / `globals(typography?id=primary)`) -> Títulos principales (H1, H2 de impacto).
     * `Secondary` (`--e-global-typography-secondary` / `globals(typography?id=secondary)`) -> Subtítulos y cabeceras de soporte (H3, H4, leyendas).
     * `Text` (`--e-global-typography-text` / `globals(typography?id=text)`) -> Cuerpo de texto estándar, párrafos y listas.
     * `Accent` (`--e-global-typography-accent` / `globals(typography?id=accent)`) -> Botones, badges, metadatos, tags y llamadas a la acción.
2. **Vinculación Dual por Token Global**:
   Elementor almacena la vinculación global de dos formas complementarias en `settings`:
   - Clave interna de control dinámico: `__globals__`:
     ```json
     "__globals__": {
       "title_color": "globals/colors?id=primary",
       "typography_typography": "globals/typography?id=primary"
     }
     ```
   - En CSS embebido o clases personalizadas, utilizar siempre la propiedad nativa de Elementor:
     ```css
     color: var(--e-global-color-primary);
     font-family: var(--e-global-typography-text-font-family);
     ```
3. **Consistencia de Tokens de Color Globales**:
   Utilizar exclusivamente los tokens globales del sistema:
   - `primary`: Color primario corporativo / acento de marca.
   - `secondary`: Tonalidad de apoyo / contraste secundario.
   - `text`: Color base para lectura y tipografía general.
   - `accent`: Elementos interactivos, resaltados y estados hover.
   - Tokens custom del Kit registrados (ej. `globals/colors?id=6a89efb` correspondientes a paletas complementarias del proyecto).

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO valores Hexadecimales / RGB Hardcodeados**:
   - NUNCA escribir `"title_color": "#ff0000"` o `"background_color": "#ffffff"` directamente en `settings` salvo que el token global no exista Y haya sido expresamente autorizado por la arquitectura.
   - Si se requiere un color de fondo blanco/neutro, mapear contra el token global de fondo del kit (`globals/colors?id=background_light` o equivalente).
2. **PROHIBIDO declarar fuentes o `font_family` inline**:
   - NUNCA definir `"typography_font_family": "Roboto"` o `"Poppins"` en el widget. Si se altera la familia tipográfica manualmente a nivel widget, se rompe el responsive typography generator de Elementor.
3. **PROHIBIDO sobreescribir tamaños de fuente (`font_size`) de forma desalineada**:
   - No usar tamaños arbitrarios (ej. `27px`, `19.3px`). Respetar la escala modular del kit global o los tamaños de viewport (`clamp()`, `rem`).

---

## 4. Estructura de Mapeo de Tokens Elementor

Tabla de referencia para inyección en el diccionario `settings` y su sub-objeto `__globals__`:

| Elemento Visual | Propiedad en `settings` | Formato en `__globals__` | Variable CSS Resultante |
| :--- | :--- | :--- | :--- |
| Color de Título | `title_color: ""` | `"title_color": "globals/colors?id=primary"` | `var(--e-global-color-primary)` |
| Tipografía de Título | `typography_typography: "custom"` | `"typography_typography": "globals/typography?id=primary"` | `var(--e-global-typography-primary-...)` |
| Color de Párrafo | `text_color: ""` | `"text_color": "globals/colors?id=text"` | `var(--e-global-color-text)` |
| Tipografía de Párrafo | `typography_typography: "custom"` | `"typography_typography": "globals/typography?id=text"` | `var(--e-global-typography-text-...)` |
| Fondo de Botón | `button_background_color: ""` | `"button_background_color": "globals/colors?id=accent"` | `var(--e-global-color-accent)` |
| Tipografía de Botón | `typography_typography: "custom"` | `"typography_typography": "globals/typography?id=accent"` | `var(--e-global-typography-accent-...)` |

---

## 5. Ejemplo de Payload JSON con Sistema de Diseño Vinculado

Ejemplo de widget `heading` y widget `button` perfectamente conectados al sistema de diseño:

```json
[
  {
    "id": "k82d91a",
    "elType": "widget",
    "isInner": false,
    "widgetType": "heading",
    "settings": {
      "title": "Patrimonio Cultural y Natural",
      "header_size": "h2",
      "title_color": "",
      "typography_typography": "custom",
      "__globals__": {
        "title_color": "globals/colors?id=primary",
        "typography_typography": "globals/typography?id=primary"
      }
    },
    "elements": []
  },
  {
    "id": "m41f09c",
    "elType": "widget",
    "isInner": false,
    "widgetType": "button",
    "settings": {
      "text": "Conocer más",
      "size": "sm",
      "button_text_color": "#ffffff",
      "background_color": "",
      "typography_typography": "custom",
      "border_radius": {
        "unit": "px",
        "top": "6",
        "right": "6",
        "bottom": "6",
        "left": "6",
        "isLinked": true
      },
      "__globals__": {
        "background_color": "globals/colors?id=accent",
        "typography_typography": "globals/typography?id=accent"
      }
    },
    "elements": []
  }
]
```

---

## 6. Criterio de Validación de Éxito
1. **Auditoría de Settings**:
   - `0` instancias de regex `#(?:[0-9a-fA-F]{3}){1,2}\b` en propiedades de color principales dentro de `settings` (excluyendo colores absolutos requeridos para contraste como `#ffffff` sobre fondos oscuros).
   - `100%` de los widgets de texto/título con `__globals__` configurado apuntando a tokens válidos del kit activo.
2. **Inspección de Render**:
   - En el frontend compilado, las reglas CSS calculadas aplican las variables CSS del Kit (`var(--e-global-color-...)`) sin sobrescrituras no deseadas en `style=""`.
