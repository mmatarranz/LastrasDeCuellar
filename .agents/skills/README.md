# Directorio de Skills Nativas de Antigravity: WordPress & Elementor Suite

Este directorio contiene las especificaciones, contratos operativos y scripts ejecutables para que los agentes de Antigravity creen, muten y mantengan páginas, plantillas y datos estructurados de Elementor en el proyecto **Lastras de Cuéllar** con máxima seguridad en base de datos, adhesión semántica, optimización SEO y fidelidad de diseño responsive.

---

## Matriz de Habilidades y Ciclo de Vida Operativo

```
[FASE 1: DISEÑO Y PREPARACIÓN]
 ├── elementor-design-system/SKILL.md          (Tokens globales del Kit activo, prohibición inline)
 └── elementor-dynamic-tags/SKILL.md           (Mapeo de tags dinámicos, bucles y CPTs)

[FASE 2: CONSTRUCCIÓN ESTRUCTURAL Y SEMÁNTICA]
 ├── elementor-json-builder/SKILL.md           (Árbol JSON Flexbox/Grid, IDs alfanuméricos de 7 chars)
 ├── elementor-responsive-breakpoints/SKILL.md (Mobile-First, flex_direction_mobile, prevención anti-overflow)
 ├── elementor-seo-semantic/SKILL.md           (Semántica HTML5 pura, exactamente un H1, alt text, a11y)
 └── wp-seo-structured-data/SKILL.md           (Schema.org / JSON-LD: AdministrativeArea, TouristAttraction, Article)

[FASE 3: OPTIMIZACIÓN Y PERFORMANCE]
 └── elementor-performance-cwv/SKILL.md        (Límite de profundidad DOM <= 3, LCP prioritario, aspect-ratio CLS)

[FASE 4: PERSISTENCIA Y RECONCILIACIÓN]
 ├── elementor-post-sync/SKILL.md              (Metadatos _elementor_edit_mode, regeneración CSS, rollback atómico)
 └── litespeed-cache-control/SKILL.md          (Purga selectiva o global de LiteSpeed Cache y validación de cabeceras)

[FASE 5: ASEGURAMIENTO DE CALIDAD]
 └── elementor-visual-qa-audit/SKILL.md        (Preview link con nonce, test anti-overflow en 375px, WCAG contrast)

[FASE 6: MEDICIÓN Y ANALÍTICA WEB]
 └── google-analytics-audit/SKILL.md           (Auditoría GA4 Data API, páginas populares, canales y dispositivos)
```

---

## Índice Detallado de Skills

1. [**`elementor-json-builder`**](./elementor-json-builder/SKILL.md)
   * Arquitectura moderna de **Contenedores Flexbox/Grid** (`elType: "container"`). Prohibición de `section`/`column`.
   * Formato canónico de 5 campos por nodo (`id`, `elType`, `isInner`, `settings`, `elements`).
   * IDs alfanuméricos de 7 caracteres únicos (`^[a-z0-9]{7}$`).

2. [**`elementor-design-system`**](./elementor-design-system/SKILL.md)
   * Inspección obligatoria previa de `elementor_active_kit`.
   * Prohibición de valores hexadecimales hardcodeados y fuentes inline.
   * Vinculación vía tokens `__globals__` y variables CSS nativas (`var(--e-global-color-...)`).

3. [**`elementor-seo-semantic`**](./elementor-seo-semantic/SKILL.md)
   * Etiquetas semánticas obligatorias en contenedores: `<header>`, `<section>`, `<article>`, `<main>`, `<aside>`.
   * Regla de **exactamente un solo H1 por página** con progresión descendente estricta.
   * Atributos `alt` obligatorios y tamaños nativos de WordPress (`medium_large`, `large`, etc.).

4. [**`wp-seo-structured-data`**](./wp-seo-structured-data/SKILL.md)
   * Inyección de esquemas JSON-LD para **Lastras de Cuéllar**: `AdministrativeArea`, `Place`, `TouristAttraction`, `Event`, `NewsArticle` y `BreadcrumbList`.
   * Script validador ejecutable en [`.agents/skills/wp-seo-structured-data/scripts/validate_schema.py`](./wp-seo-structured-data/scripts/validate_schema.py).

5. [**`elementor-post-sync`**](./elementor-post-sync/SKILL.md)
   * Sincronización obligatoria de metadatos: `_elementor_edit_mode = "builder"` y `_elementor_template_type`.
   * Regeneración forzada de CSS con `elementor-clear-cache`.
   * Snapshot de seguridad previo y rutina de **Rollback automático** ante errores HTTP 401, 403 o 500.

6. [**`litespeed-cache-control`**](./litespeed-cache-control/SKILL.md)
   * Gestión e invalidación de caché LiteSpeed (HTML y UCSS) tras cada despliegue de Elementor.
   * Script de purga automatizada en [`.agents/skills/litespeed-cache-control/scripts/purge_litespeed.py`](./litespeed-cache-control/scripts/purge_litespeed.py).

7. [**`elementor-responsive-breakpoints`**](./elementor-responsive-breakpoints/SKILL.md)
   * Principio Mobile-First en Flexbox (`flex_direction_mobile: "column"`).
   * Reducción adaptativa de paddings y tipografía fluida en móviles (< 768px).
   * Prohibición de anchos fijos en píxeles causantes de desbordamiento horizontal (*horizontal overflow*).

8. [**`elementor-performance-cwv`**](./elementor-performance-cwv/SKILL.md)
   * Prevención de *DOM Bloat*: profundidad máxima estricta de 3 niveles de contenedores.
   * Optimización del LCP (evitar lazy-loading en la imagen crítica del Hero, formatos `.webp`/`.avif`).
   * Eliminación del CLS con `aspect_ratio` explícito e invalidación coordinada de LiteSpeed Cache (UCSS).

9. [**`elementor-dynamic-tags`**](./elementor-dynamic-tags/SKILL.md)
   * Mapeo de datos dinámicos mediante el objeto `__dynamic__` para Theme Builder (`single`, `archive`, `search`).
   * Widgets dedicados de tema (`theme-post-title`, `theme-post-content`, `theme-post-featured-image`).
   * Paginación obligatoria en queries y exclusión de post actual en widgets de artículos relacionados.

10. [**`elementor-visual-qa-audit`**](./elementor-visual-qa-audit/SKILL.md)
    * Validación post-inyección mediante `elementor-create-preview-link`.
    * Verificación de cero desbordamiento en viewport de 375px (`scrollWidth === innerWidth`).
    * Auditoría de ratios de contraste tipográfico WCAG 2.1 AA (mínimo 4.5:1).

11. [**`google-analytics-audit`**](./google-analytics-audit/SKILL.md)
    * Conexión segura con Google Analytics 4 (GA4 Data API v1beta) mediante Service Account.
    * Auditoría de tráfico web, páginas y artículos más populares, tasa de rebote e interacción.
    * Análisis de adquisición de tráfico (búsqueda orgánica, redes, directo) y dispositivos (móvil vs desktop).
    * Scripts ejecutables en `scripts/` (`run_report.py`, `ga4_client.py`, `test_connection.py`).

