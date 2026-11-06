# Arquitectura del Sistema - Lastras de Cuéllar

Documento técnico que detalla la infraestructura, entorno del servidor, configuración de WordPress y plugins instalados en producción.

---

## 1. Entorno del Servidor

- **Dominio Principal**: `https://www.lastrasdecuellar.net`
- **Servidor Web**: LiteSpeed Web Server
- **Sistema Operativo**: Linux
- **Versión PHP**: `8.4.27`
- **Límites PHP**:
  - `memory_limit`: `1024M` (WordPress limit: `512M` / `1024M`)
  - `max_input_vars`: `10000`
  - `post_max_size`: `120M`
  - `upload_max_filesize`: `100M`
- **Base de Datos**: MySQL Community Server - GPL `v8.4.11`
- **Extensiones Clave**: GD instalada, ZIP instalada, permisos de escritura correctos.
- **Conexión a Elementor Library**: Conectada y operativa.

---

## 2. Entorno WordPress

- **Versión WordPress**: `7.1.4` (o versión local / de desarrollo reportada)
- **Idioma**: `es_ES`
- **Zona Horaria**: `Europe/Madrid`
- **Estructura de Permalinks**: `/%postname%/`
- **Modo Debug**: Inactivo (producción)
- **Tema Activo**: `Hello Elementor` (v3.5.1)
  - *Recomendación técnica detectada*: Implementar tema hijo (`Hello Elementor Child`) para preservar modificaciones de código PHP y CSS en futuras actualizaciones.

---

## 3. Elementor & Elementor Pro

- **Versión Elementor Core**: `4.4.0-beta2`
- **Versión Elementor Pro**: `4.4.0-beta2`
- **Licencia**: Nivel **Expert** (Activa)
- **Editor Atómico**: Activo (`atomic_editor: true`)
- **Experimentos y Características Activas**:
  - `container`: Contenedores Flexbox y Grid activos.
  - `e_font_icon_svg`: Fuentes de iconos integradas como SVG inline (ahorra carga de fuentes CSS pesadas).
  - `additional_custom_breakpoints`: Puntos de ruptura personalizados activos.
  - `e_optimized_markup`: Marcado HTML optimizado del DOM activo.
  - `theme_builder_v2`: Nuevo maquetador de temas activo por defecto.
  - `hello-theme-header-footer`: Soporte de cabecera y pie integrado activo.
  - `markdown_rendering`: Generación de markdown para agentes IA activa.
  - `mega-menu`: Soporte de mega menús anidados activo.

---

## 4. Plugins Activos en Producción

| Plugin | Versión | Autor | Propósito |
| :--- | :--- | :--- | :--- |
| **Elementor** | 4.4.0-beta2 | Elementor.com | Maquetador visual base |
| **Elementor Pro** | 4.4.0-beta2 | Elementor.com | Funcionalidades Pro (Theme Builder, Popups, Form, Loop) |
| **LiteSpeed Cache** | 7.9.3 | LiteSpeed Technologies | Aceleración de caché a nivel de servidor LiteSpeed |
| **Rank Math SEO** | 1.0.281 | Rank Math SEO | Suite de SEO base |
| **Rank Math SEO PRO** | 3.0.99 | Rank Math SEO | Schema avanzado, redirecciones, monitor 404 |
| **Wordfence Security** | 9.0.2 | Wordfence | Firewall de aplicaciones web (WAF) y seguridad |
| **Site Kit by Google** | 1.191.0 | Google | Search Console, Analytics y métricas |
| **WP Mail SMTP** | 4.10.3 | WP Mail SMTP | Entrega fiable de correos transaccionales |
| **WPS Hide Login** | 1.9.19 | WPServeur | Ocultamiento de la ruta estándar `wp-login.php` |
| **Custom Login Page Customizer** | 2.5.4 | Hardeep Asrani | Personalización estética de la pantalla de acceso |
| **Asesor de Cookies RGPD** | 1.0.48 | Carlos Doral Pérez | Cumplimiento normativo RGPD / ePrivacy |
| **Antispam Bee** | 2.11.13 | pluginkollektiv | Protección antispam sin cookies externas |
| **Auto Image Attributes From Filename** | 4.9.1 | Arun Basil Lal | Generación automática de etiquetas `alt`, títulos y descripciones en medios |
| **PDF Embedder** | 5.0.2 | PDF Embedder | Visualización incrustada de bandos, actas y documentos PDF |
| **Post Type Switcher** | 4.1.1 | Triple J Software | Cambio rápido entre tipos de contenido (entradas, páginas, CPTs) |
| **Reading Time WP** | 2.0.18 | Jason Yingling | Estimación del tiempo de lectura en artículos |
| **HTTP Headers** | 1.19.6 | Dimitar Ivanov | Cabeceras de seguridad HTTP (HSTS, CSP, X-Frame) |
| **Easy MCP AI** | 2.3.2 | EasyMCPAI | Conector MCP para agentes de inteligencia artificial |
| **AI / AI Provider for Anthropic** | 1.5.0 / 1.0.5 | WP Contributors / Anthropic | Integración de servicios generativos de IA en WordPress |
| **WP Dashboard Notes** | 1.0.13 | Jeroen Sormani | Notas internas en el panel de control de administración |
