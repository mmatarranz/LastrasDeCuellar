---
name: litespeed-cache-control
description: >-
  Gestión, inspección y purga de LiteSpeed Cache en WordPress: purga por URL o post ID, purga global (purge-all), validación de cabeceras HTTP de caché e invalidación coordinada de CSS crítico (UCSS).
---

# Skill: LiteSpeed Cache Control & Invalidation Protocol

## 1. Propósito y Activación
- **Propósito**: Garantizar que todas las modificaciones estructurales, cambios de diseño, publicaciones de nuevos contenidos o ajustes en kits globales de Elementor se reflejen de inmediato para los visitantes y las herramientas de auditoría visual, eliminando el servicio de HTML, CSS o assets obsoletos generados por LiteSpeed Cache y su motor de optimización (UCSS).
- **Cuándo invocar esta skill**:
  - Inmediatamente tras ejecutar cualquier mutación exitosa vía `elementor-update-page-settings`, scripts de Python o WP REST API.
  - Al detectar discrepancias visuales entre el preview interno de Elementor y el frontend público de la web.
  - Antes de realizar capturas de pantalla, auditorías móviles o comprobaciones de DOM con Playwright o headless Chrome.
  - Al actualizar plantillas globales del Theme Builder (`header`, `footer`, `single`, `archive`).

---

## 2. Requisitos Previos y Tools MCP
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-clear-cache`: Para invalidar y regenerar los archivos CSS compilados de Elementor (`/wp-content/uploads/elementor/css/`).
- **Herramientas locales**:
  - Script ejecutable: `scripts/purge_litespeed.py` para purgar URLs específicas o el sitio entero y verificar las cabeceras HTTP de caché en tiempo real.

---

## 3. Protocolo de Purga en 3 Pasos

Tras cualquier cambio en WordPress/Elementor, sigue este flujo riguroso:

```
[1. elementor-clear-cache] ──▶ [2. Purga LiteSpeed por URL / All] ──▶ [3. Verificación de Cabeceras HTTP]
```

### Paso 1: Regenerar CSS de Elementor
Ejecutar la herramienta MCP:
```json
{
  "ServerName": "lastras-de-cuellar-segovia-elementor",
  "ToolName": "elementor-clear-cache",
  "Arguments": {}
}
```

### Paso 2: Purgar LiteSpeed Cache
Ejecutar el script local con la URL específica de la página modificada o `--all`:
```bash
python3 .agents/skills/litespeed-cache-control/scripts/purge_litespeed.py --url https://www.lastrasdecuellar.net/
# O purga global del portal:
python3 .agents/skills/litespeed-cache-control/scripts/purge_litespeed.py --all
```

### Paso 3: Verificación de Cabeceras de Respuesta
Al realizar una petición `GET` a la página con cabeceras `Cache-Control: no-cache`:
- La cabecera `X-LiteSpeed-Cache` debe devolver `miss` en la primera petición (indicando que el servidor ha generado la página en vivo) y luego `hit` en las solicitudes posteriores.
- Comprobar que no se retorne ningún error 500, 502 o 504.

---

## 4. Detección y Resolución de Conflictos Comunes

1. **UCSS Obsoleto (Unique CSS)**:
   - LiteSpeed genera un archivo CSS minificado por página (`litespeed_ucss.css`). Si tras actualizar Elementor los nuevos contenedores aparecen sin estilos o sin flexbox, es porque el UCSS anterior aún no se ha purgado. Ejecutar la purga con `--all` y solicitar la regeneración.
2. **Caché del Navegador vs Caché de Servidor**:
   - Para inspecciones con Playwright o curl, enviar siempre las siguientes cabeceras HTTP para asegurar contenido fresco:
     ```http
     Cache-Control: no-cache, no-store, must-revalidate
     Pragma: no-cache
     ```
