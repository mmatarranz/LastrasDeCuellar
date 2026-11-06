# Lastras de Cuéllar - WordPress & Elementor Pro

Repositorio oficial y centro de desarrollo para el portal web **Lastras de Cuéllar** (`https://www.lastrasdecuellar.net`).

---

## 📌 Resumen del Proyecto

- **Sitio Web en Producción**: [https://www.lastrasdecuellar.net](https://www.lastrasdecuellar.net)
- **CMS**: WordPress
- **Constructor Visual**: Elementor Pro (Licencia Expert) con Atomic Editor activo
- **Servidor Web**: LiteSpeed Web Server (PHP 8.4.27, MySQL 8.4.11)
- **Tema Base**: Hello Elementor 3.5.1
- **Repositorio Remoto**: `git@github.com:mmatarranz/LastrasDeCuellar.git` (rama `main`)

---

## 📚 Documentación Técnica

La documentación detallada se organiza en el directorio [`docs/`](./docs/):

1. [**Arquitectura del Sistema (`docs/ARCHITECTURE.md`)**](./docs/ARCHITECTURE.md):
   - Especificaciones completas del servidor LiteSpeed, versión PHP, MySQL y límites de memoria.
   - Listado completo de plugins activos (LiteSpeed Cache, Rank Math SEO PRO, Wordfence, etc.).
   - Experimentos de Elementor activos (Contenedores, Marcado optimizado, SVG inline, etc.).

2. [**Inventario de Plantillas Elementor (`docs/ELEMENTOR_TEMPLATES.md`)**](./docs/ELEMENTOR_TEMPLATES.md):
   - Mapeo de IDs de cabecera (`13859`), pie de página (`26318`), popups (`21329`, `8903`), plantilla 404 (`15482`) y plantilla maestra de entradas (`22328`).
   - Condiciones de inclusión y exclusión aplicadas.

3. [**Rendimiento y Gestión de Caché (`docs/PERFORMANCE_AND_CACHING.md`)**](./docs/PERFORMANCE_AND_CACHING.md):
   - Configuración de LiteSpeed Cache y optimizaciones específicas para Elementor.
   - Protocolo de purga y regeneración de CSS (`elementor-clear-cache`).

4. [**Directrices de Desarrollo y Tema Hijo (`docs/DEVELOPMENT_GUIDELINES.md`)**](./docs/DEVELOPMENT_GUIDELINES.md):
   - Recomendación y arquitectura para la implementación de `hello-elementor-child`.
   - Seguridad (Wordfence, WPS Hide Login, nonces y validaciones).

---

## 🛠️ Habilidades del Agente (Skills en `.agents/skills/`)

Este repositorio cuenta con un set de habilidades modulares especializadas:

| Habilidad | Ubicación | Descripción |
| :--- | :--- | :--- |
| **`elementor-pro-builder`** | [`.agents/skills/elementor-pro-builder/`](./.agents/skills/elementor-pro-builder/SKILL.md) | Maquetación con contenedores Flexbox/Grid, Theme Builder, popups e integración MCP. |
| **`litespeed-cache-elementor`** | [`.agents/skills/litespeed-cache-elementor/`](./.agents/skills/litespeed-cache-elementor/SKILL.md) | Configuración de LSCache, Critical CSS y purga selectiva con Elementor. |
| **`rank-math-seo-pro`** | [`.agents/skills/rank-math-seo-pro/`](./.agents/skills/rank-math-seo-pro/SKILL.md) | Marcado Schema JSON-LD, migas de pan, redirecciones 301 y optimización on-page. |
| **`wordpress-custom-code`** | [`.agents/skills/wordpress-custom-code/`](./.agents/skills/wordpress-custom-code/SKILL.md) | Desarrollo en tema hijo, CPTs, taxonomías, integración ACF y seguridad. |
| **`elementor-performance-seo`** | [`.agents/skills/elementor-performance-seo/`](./.agents/skills/elementor-performance-seo/SKILL.md) | Optimización de Core Web Vitals (LCP, CLS, INP), fuentes y jerarquía semántica. |
| **`wordpress-git-workflow`** | [`.agents/skills/wordpress-git-workflow/`](./.agents/skills/wordpress-git-workflow/SKILL.md) | Procedimiento de commits semánticos, exclusiones de `.gitignore` y sincronización con GitHub. |

---

## 🚀 Guía Rápida de Sincronización Git

```bash
# Comprobar estado
git status

# Añadir archivos modificados
git add .

# Crear commit con formato semántico
git commit -m "docs(readme): update system specs and template index"

# Subir cambios al repositorio remoto
git push origin main
```
