# Guía de Rendimiento y Caché (LiteSpeed + Elementor)

Esta guía define las estrategias para mantener un rendimiento óptimo (90+ en PageSpeed / Lighthouse), minimizar el bloqueo de renderizado y evitar problemas de estilos rotos.

---

## 1. Configuración de LiteSpeed Cache (LSCache)

El servidor funciona bajo **LiteSpeed Web Server**, lo que permite una integración de caché nativa en memoria extremadamente rápida.

### 1.1. Ajustes de Caché
- **Caché Pública**: Activada para páginas y recursos estáticos.
- **Caché Privada**: Activada para usuarios identificados (WordPress Admin).
- **TTL Estándar**:
  - Front-page y artículos: 604800 segundos (7 días).
  - Páginas estáticas: 604800 segundos.
  - Feeds: 0 o 3600 segundos.

### 1.2. Optimización CSS y JS para Elementor
- **Combinar CSS**: **Desactivado** o con exclusiones estrictas. Elementor 4.4 genera CSS modular y atómico; combinar todos los archivos genera bundles pesados que bloquean el First Contentful Paint.
- **Critical CSS (CCSS)**: Activado. Genera el CSS crítico del primer pantallazo de forma asíncrona mediante los servidores de QUIC.cloud.
- **Minificación CSS/JS**: Activada.
- **Carga de JS diferida (Defer/Async)**: Activada, excluyendo librerías interactivas críticas para evitar retrasos en el Interaction to Next Paint (INP).

### 1.3. Optimización de Imágenes
- **Conversión a WebP**: Activada en LSCache. Las imágenes JPG/PNG se sirven como `.webp` en navegadores compatibles sin modificar la URL original gracias a reglas de reescritura de LiteSpeed.
- **Lazy Loading**: Activado para imágenes fuera del primer scroll. **Importante**: Desactivar lazy-load en la imagen destacada/hero superior para proteger el LCP (Largest Contentful Paint).

---

## 2. Invalidadación y Purga de Caché

### Matriz de Decisión de Purga

| Escenario | Acción de Caché | Herramienta |
| :--- | :--- | :--- |
| Edición de un artículo o página normal | Purga automática de esa URL | Automática (LiteSpeed) |
| Edición del Header (`ID 13859`) o Footer (`ID 26318`) | Purga completa de LiteSpeed | LiteSpeed Cache → Purgar todo |
| Cambio de colores o tipografías globales de Elementor | Purgar CSS Elementor + Purgar LiteSpeed | `elementor-clear-cache` + LiteSpeed |
| Estilos desactualizados en frontend tras actualizar plugins | Purgar CSS Elementor + Purgar LiteSpeed | `elementor-clear-cache` + LiteSpeed |
| Rutinas habituales de edición de texto | No requiere vaciado forzado | Guardar / Publicar |
