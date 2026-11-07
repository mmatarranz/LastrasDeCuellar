---
name: elementor-visual-qa-audit
description: >-
  Pipeline automatizado de control de calidad visual y auditoría de regresiones con Playwright/headless browser tras mutaciones en Elementor: links de previsualización con nonce, test anti-overflow en 375px y verificación de contraste WCAG.
---

# Skill: Elementor Visual QA & Automated Regression Audit

## 1. Propósito y Activación
- **Propósito**: Establecer un pipeline automatizado de aseguramiento de calidad (QA) y detección de regresiones visuales tras cualquier mutación realizada por agentes de Antigravity en Elementor. Garantiza que no se publiquen layouts rotos, elementos superpuestos, textos invisibles por bajo contraste o errores de JavaScript en consola.
- **Cuándo invocar esta skill**:
  - Inmediatamente después de completar la inyección de datos y la regeneración de caché (`elementor-post-sync`).
  - Antes de marcar como completada cualquier tarea de rediseño, actualización de cabeceras, footers o páginas clave.
  - Tras cambios en tokens globales del Kit activo para asegurar que no se rompieron componentes existentes.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-create-preview-link`: Para obtener el enlace seguro de previsualización con nonce activo antes de hacer público el contenido.
  - `elementor-get-page-structure`: Para cotejar que todos los nodos enviados existen efectivamente en el post procesado.
  - `elementor-manage-revisions`: Para revertir a la revisión anterior si el QA detecta fallos visuales críticos.
- **Entorno de Pruebas**:
  - Motor de ejecución headless (Node.js/Puppeteer o Python/Playwright/Requests) para inspección de DOM renderizado.

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Verificación de Tres Viewports Estándar**:
   - Toda auditoría automatizada o visual DEBE comprobar el renderizado en al menos 3 anchos de pantalla:
     * **Mobile**: 375 x 812 px (iPhone estándar).
     * **Tablet**: 768 x 1024 px (iPad vertical).
     * **Desktop**: 1440 x 900 px (MacBook/Portátil).
2. **Inspección de Desbordamiento Horizontal (Zero Overflow Rule)**:
   - En el viewport Mobile (375px), ejecutar la comprobación DOM:
     ```javascript
     const hasOverflow = document.documentElement.scrollWidth > window.innerWidth;
     ```
   - Si `hasOverflow === true`, el despliegue se considera **FALLIDO** y debe identificarse el nodo causante mediante el cálculo de `element.getBoundingClientRect().right > window.innerWidth`.
3. **Auditoría de Contraste Accesible (WCAG 2.1 AA)**:
   - El contraste de color entre el texto y su fondo inmediato DEBE cumplir:
     * Texto normal (< 18pt o < 14pt negrita): Ratio mínimo **4.5:1**.
     * Texto grande (>= 18pt o >= 14pt negrita): Ratio mínimo **3.0:1**.
   - Prohibido texto blanco sobre fondos claros o texto gris suave (#888) sobre fondo blanco.
4. **Inspección de Recursos Rotos (404 / Console Errors)**:
   - Escanear la respuesta de la página en busca de:
     * Peticiones HTTP 404 en imágenes, fuentes o hojas de estilo (`post-{id}.css`).
     * Errores fatales de JavaScript en la consola (`Uncaught TypeError: elementorFrontend is not defined`, etc.).

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO Dar por "Terminada" una tarea sin prueba en preview**:
   - Nunca responder al usuario que una página está lista basándose únicamente en que la API devolvió HTTP 200, sin haber verificado que el frontend renderiza el árbol de Elementor correctamente.
2. **PROHIBIDO Ignorar FOUC (Flash of Unstyled Content)**:
   - Si los estilos de Elementor se cargan con retraso extremo debido a que el archivo CSS no fue compilado a tiempo, no ignorar la advertencia: se debe re-ejecutar `elementor-clear-cache`.
3. **PROHIBIDO Publicar con Elementos Superpuestos Invisibles**:
   - En contenedores con márgenes negativos o posicionamiento absoluto, verificar que no bloqueen los clics de botones o enlaces subyacentes (`pointer-events`).

---

## 4. Pipeline de Auditoría Automatizada (Checklist de Aprobación)

```
[Inyección Finalizada en Post-Sync]
                │
                ▼
  [1. Obtener Enlace Preview] ──► elementor-create-preview-link(post_id)
                │
                ▼
  [2. Render Headless / Fetch]
  ├── A. Código HTTP de Página es 200 (Sin 500, sin PHP warnings)
  ├── B. Cero errores 404 en hojas de estilo post-{id}.css
  ├── C. Zero Overflow en Mobile (scrollWidth === 375px)
  ├── D. Ratio de contraste WCAG >= 4.5:1 en textos principales
  └── E. Cero shortcodes crudos o texto JSON visible en el HTML
                │
         ¿Pasa todos los checks?
         ├── SÍ ──► [APROBAR Y PUBLICAR]
         └── NO ──► [ACTIVAR ROLLBACK Y NOTIFICAR ALERTA TÉCNICA]
```

---

## 5. Script Automatizado de Verificación y Auditoría (Python / Node)

Script de ejemplo utilizado por los agentes para auditar la página tras una sincronización:

```python
import json
import re
import requests

def audit_elementor_frontend(preview_url, post_id):
    """
    Ejecuta un barrido de QA sobre la URL de previsualización o página pública.
    """
    print(f"[QA AUDIT] Iniciando inspección sobre: {preview_url}")
    
    response = requests.get(preview_url, timeout=15)
    
    # Check 1: Estado HTTP
    if response.status_code != 200:
        return False, f"Fallo HTTP {response.status_code} al cargar preview."
    
    html = response.text
    
    # Check 2: Detección de JSON o Shortcodes crudos no parseados
    corrupt_patterns = [
        r'\[elementor-tag\s+',
        r'\{\\\"id\\\":\\\"[a-z0-9]{7}\\\"',
        r'_elementor_data'
    ]
    for pattern in corrupt_patterns:
        if re.search(pattern, html):
            return False, f"Error Crítico: Se detectaron residuos crudos de Elementor en el HTML ({pattern})."
    
    # Check 3: Confirmación de carga del CSS compilado de Elementor
    css_pattern = rf'/uploads/elementor/css/post-{post_id}\.css'
    if not re.search(css_pattern, html) and f'elementor-post-{post_id}' not in html:
        return False, f"Aviso: La hoja de estilos post-{post_id}.css no está vinculada en el documento."
    
    # Check 4: Verificación de Contenedor Principal
    if 'elementor-element' not in html:
        return False, "La página no contiene clases nativas de Elementor (renderizador inactivo)."
        
    print("[QA AUDIT OK] Estructura básica, CSS compilado y sintaxis verificadas con éxito.")
    return True, "Auditoría superada exitosamente."
```

---

## 6. Criterio de Validación de Éxito
1. **Resolución Exitosa del Pipeline**:
   - La función de auditoría devuelve `True` sin alertas críticas de sintaxis o render.
2. **Ausencia Total de Residuos Crudos**:
   - Búsqueda de regex `\[elementor-tag` o `\"widgetType\"` en el HTML público arroja `0` resultados.
3. **Validación de Experiencia de Usuario**:
   - Enlace `preview_url` listo para el usuario final sin desbordamiento horizontal y con jerarquía tipográfica legible.
