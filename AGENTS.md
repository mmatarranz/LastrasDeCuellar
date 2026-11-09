# 🤖 AGENTS.md — Protocolos de Operación y Reglas de Seguridad para Agentes de IA

> **Propósito**: Este documento establece las instrucciones operativas, directrices de ejecución y restricciones obligatorias para cualquier modelo o agente de IA que interactúe con este repositorio y el servidor MCP de WordPress/Elementor de **Lastras de Cuéllar**.

---

## ⚠️ Reglas Críticas Inviolables (Hard Constraints)

1. **BACKUP ANTES DE CUALQUIER MUTACIÓN**:
   - Está **estrictamente prohibido** actualizar o sobreescribir cualquier página, plantilla o kit global de Elementor sin haber guardado previamente una copia exacta del estado actual en formato JSON.
   - Formato obligatorio del archivo:
     `backup_page_{PAGE_ID}_{descripcion_de_accion}.json` o `backup_template_{ID}_....json` en la raíz o directorio correspondiente.

2. **PROTECCIÓN DE CREDENCIALES**:
   - Nunca expongas ni subas a repositorios públicos las credenciales de basic auth contenidas en `.agents/mcp_config.json`.
   - No hardcodees tokens o contraseñas en scripts nuevos; lee la configuración desde `.agents/mcp_config.json` o variables de entorno.

3. **PURGA DE CACHÉ LITESPEED OBLIGATORIA**:
   - El sitio opera con **LiteSpeed Cache**.
   - Cualquier cambio aplicado a una página o plantilla no se reflejará en vivo hasta que se limpie la caché correspondiente (`litespeed-purge` o invocando el endpoint de purga si está disponible).
   - Ten en cuenta que si capturas pantallas o inspeccionas el DOM con Playwright/curl sin purgar la caché o sin usar cabeceras `Cache-Control: no-cache` y cookies de sesión, verás contenido obsoleto.

4. **IDs DE ELEMENTOR ÚNICOS**:
   - Cada contenedor, sección, columna o widget en Elementor **debe tener un `id` único** de 7 u 8 caracteres hexadecimales/alfanuméricos (ej. `562371e6`, `7a1b4c9`).
   - Al duplicar estructuras o insertar componentes nuevos, genera siempre IDs nuevos para cada nodo. Duplicar IDs provoca fallos graves en el constructor visual de Elementor y en los estilos scoped.

---

## 🛠️ Protocolo Técnico para Modificar Elementor vía MCP / Scripts

### 1. Serialización de `_elementor_data`
En WordPress/Elementor, la estructura de la página se almacena en el meta campo `_elementor_data`.
- Es una cadena serializada JSON de un array de elementos raíz (típicamente contenedores flexbox `e-con`).
- **Verificación**: Antes de enviar el payload con `elementor-update-page-settings` o via REST API, valida que `json.loads()` y `json.dumps()` procesen la estructura sin errores de sintaxis o escapes corruptos.

### 2. Estructura Estándar de un Contenedor Flexbox (e-con)
```json
{
  "id": "abc1234",
  "elType": "container",
  "settings": {
    "content_width": "boxed",
    "flex_direction": "column",
    "background_background": "classic",
    "background_color": "#F9F7F2"
  },
  "elements": [ ...hijos... ],
  "isInner": false
}
```

### 3. Preservación de Widgets Dinámicos
- Si una página existente contiene widgets de consulta dinámica (ej. Posts de WordPress, filtros, galerías de vídeo, formularios), **no los reemplaces por HTML estático** a menos que el usuario lo solicite expresamente.
- Preserva sus configuraciones de query (`posts_per_page`, `categories`, `pagination`).

---

## 📱 Verificación y Auditoría Visual

Antes de dar por concluida una tarea de maquetación:

1. **Auditoría Desktop (1440px / 1200px)**:
   - Margen centralizado (boxed 1140px o 1200px según la sección).
   - Proporciones armoniosas del Bento Grid (2 o 3 columnas).
2. **Auditoría Mobile (375px - 390px - 414px)**:
   - Comprueba que no exista desbordamiento horizontal (`body { overflow-x: hidden; }` y anchos máximos al 100%).
   - Tamaños de fuente legibles en pantallas pequeñas (titulares reducidos adecuadamente a 24px-28px).
   - Botones y enlaces táctiles con un target mínimo de 44x44px.

---

## 🧩 Suite de Skills Nativas de Antigravity (`.agents/skills/`)

El agente cuenta con una suite de 11 habilidades operativas estructuradas según el estándar de Antigravity:
1. `elementor-json-builder`: Estructura JSON canónica de 5 campos, contenedores Flexbox/Grid e IDs alfanuméricos únicos de 7 caracteres.
2. `elementor-design-system`: Tokens del Kit activo (`__globals__` y `var(--e-global-*)`).
3. `elementor-seo-semantic`: Semántica HTML5 pura, exactamente un H1 por página y accesibilidad WCAG.
4. `wp-seo-structured-data`: Esquemas JSON-LD (AdministrativeArea, TouristAttraction, Article, BreadcrumbList) y script `validate_schema.py`.
5. `elementor-post-sync`: Persistencia atómica de metadatos de WordPress y rollback automático.
6. `litespeed-cache-control`: Invalidation y purga de LiteSpeed Cache con script `purge_litespeed.py`.
7. `elementor-responsive-breakpoints`: Principios Mobile-First y prevención de desbordamiento horizontal.
8. `elementor-performance-cwv`: Optimización de Core Web Vitals (LCP, CLS, INP) y límite de profundidad DOM <= 3.
9. `elementor-dynamic-tags`: Integración de bucles dinámicos y tags de CMS para Theme Builder.
10. `elementor-visual-qa-audit`: Enlaces de previsualización y comprobación de regresiones en 375px.
11. `google-analytics-audit`: Conexión segura con GA4 Data API, métricas de tráfico, páginas top, canales y dispositivos.

---

## 📂 Organización de Archivos de Trabajo y Backup Editorial Automatizado

- **Raíz (`/`)**: Scripts de producción globales, backups maestros (`backup_*.json`), script de respaldo editorial [`backup_content_markdown.py`](file:///Users/miguelangelmatarranzsanchez/Desktop/aplicaciones-web/LastrasDeCuellar/backup_content_markdown.py) y documentación oficial.
- **`backups/markdown/`**: Archivo vivo en formato Markdown (`.md`) con Frontmatter YAML de todas las entradas (`posts/`) y páginas (`pages/`), acompañado de los respaldos `_elementor_data` (`elementor_json/`), el manifiesto incremental (`sync_manifest.json`) y el índice maestro [`INDEX.md`](file:///Users/miguelangelmatarranzsanchez/Desktop/aplicaciones-web/LastrasDeCuellar/backups/markdown/INDEX.md).
  - Se sincroniza automáticamente cada noche mediante GitHub Actions ([`.github/workflows/backup-markdown.yml`](file:///Users/miguelangelmatarranzsanchez/Desktop/aplicaciones-web/LastrasDeCuellar/.github/workflows/backup-markdown.yml)) o ejecutando localmente `python3 backup_content_markdown.py`.
- **`scratch/`**: Scripts temporales, pruebas de maquetación, volcados de análisis y capturas de pantalla de depuración. No comprometer el flujo principal con pruebas intermedias.
- **`.agents/`**: Configuración técnica de los agentes y conectores MCP.

---

## 📋 Checklist Rápido para el Agente antes de Confirmar Éxito

- [ ] ¿Se generó el backup JSON del estado previo?
- [ ] ¿Los widgets nuevos tienen IDs únicos?
- [ ] ¿Se respetó el `DESIGN_SYSTEM.md` (colores, fuentes Playfair/Plus Jakarta Sans, estilo Bento)?
- [ ] ¿Se aplicó la actualización correctamente en WordPress?
- [ ] ¿Se purgó la caché de LiteSpeed?
- [ ] ¿Se verificó que no hay roturas en la versión móvil?
