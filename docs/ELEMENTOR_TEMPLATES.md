# Inventario de Plantillas Elementor Pro (Theme Builder)

Este documento registra los componentes del Theme Builder y plantillas globales de **Lastras de Cuéllar** extraídas mediante la integración MCP con Elementor Pro.

---

## 1. Plantillas Globales Activas

### 1.1. Header Global
- **ID del Post**: `13859`
- **Tipo**: `header`
- **Título**: `Header`
- **Estado**: Publicado (`publish`), Activo (`is_active: true`)
- **Condiciones de visualización**:
  - `include/general` (Aplica a todo el sitio web por defecto).
  - Excepciones aplicadas (`exclude`):
    - Portada principal: `exclude/singular/front_page`
    - Páginas específicas excluidas: `26169`, `26397`, `26389`, `5459`, `392`, `402`, `15218`.

### 1.2. Footer Global
- **ID del Post**: `26318`
- **Tipo**: `footer`
- **Título**: `Footer Global`
- **Estado**: Publicado (`publish`), Activo (`is_active: true`)
- **Condiciones de visualización**:
  - `include/general` (Aplica a todo el sitio web).
  - Excepciones aplicadas (`exclude`):
    - Portada principal: `exclude/singular/front_page`
    - Páginas específicas: `26169`, `26397`, `26389`, `5459`, `392`, `402`, `15218`.

### 1.3. Popups y Menús Desplegables
- **Menú Emergente Principal**:
  - **ID**: `21329`
  - **Tipo**: `popup`
  - **Título**: `menu`
  - **Estado**: Publicado, Activo (`include/general`)
- **Menú Móvil**:
  - **ID**: `8903`
  - **Tipo**: `popup`
  - **Título**: `menu movil`
  - **Estado**: Publicado, Activo (`include/general`)

---

## 2. Plantillas de Contenido Singular y Archivos

### 2.1. Plantilla Maestra de Entradas (Single Post)
- **ID**: `22328`
- **Tipo**: `single`
- **Título**: `Plantilla Maestra de Entradas | Stitch 2026`
- **Estado**: Publicado (`publish`)
- **Condición**: `include/singular/post`
- **Nota**: Revisar si debe activarse como plantilla predeterminada para todas las noticias y entradas del blog.
- **Otras plantillas de entradas en borrador**:
  - ID `9771`: `entradas` (draft)
  - ID `5755`: `entradas` (draft)

### 2.2. Página de Error 404
- **ID**: `15482`
- **Tipo**: `error-404`
- **Título**: `404`
- **Estado**: Publicado (`publish`)
- **Condición**: `include/singular/not_found404`

### 2.3. Archivos y Resultados de Búsqueda
- **Archivo de Etiquetas**:
  - **ID**: `8454`
  - **Tipo**: `archive`
  - **Título**: `archivo etiquetas`
  - **Condición**: `include/archive/post_tag`
- **Buscador**:
  - **ID**: `8446`
  - **Tipo**: `archive`
  - **Título**: `buscador`
  - **Condición**: `include/archive/search`

---

## 3. Protocolo de Modificación de Plantillas

1. **Lectura previa**:
   - Ejecutar `elementor-get-page-structure` con el ID de la plantilla antes de aplicar cambios estructurales.
2. **Edición atómica**:
   - Utilizar `elementor-manage-elements` para cambios quirúrgicos o `elementor-build-composition` para sustituciones completas de layout.
3. **Puntos de ruptura**:
   - Ajustar diseño responsive mediante `@media (--mobile)` y `@media (--tablet)`.
4. **Purga de caché**:
   - Tras modificar cabecera o pie global, purgar la caché de LiteSpeed para que se refleje inmediatamente en las páginas cacheadas.
