# 🎨 DESIGN_SYSTEM.md — Sistema de Diseño UI / UX

> **Identidad de Marca**: Lastras de Cuéllar (Segovia) — Editorial, Naturaleza, Historia y Modernidad  
> **Concepto Estético**: *Bento Grid Editorial* con toques de diseño editorial clásico (Serif noble) combinado con una interfaz contemporánea, limpia y táctil.

---

## 🏛️ 1. Tipografía (Typography Stack)

El portal combina tres tipografías Google Fonts con roles específicos:

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Cinzel:wght@600;700&display=swap');
```

| Fuente | Familia / Categoría | Rol de Aplicación | Estilos habituales |
|---|---|---|---|
| **`Playfair Display`** | Serif Editorial | Titulares principales (`h1`, `h2`), frases célebres y cabeceras de reportajes monográficos | 600, 700, cursiva para acentos |
| **`Cinzel`** | Serif Epigráfica / Clásica | Títulos de gran solemnidad (Historia, Patrimonio, Arqueología), letras capitulares o subtítulos con `letter-spacing: 0.1em` | 600, 700 uppercase |
| **`Plus Jakarta Sans`** | Sans-serif Geométrica Moderna | Cuerpo de texto (`p`), interfaz de usuario, botones, menús, etiquetas, metadatos y navegación | 400 (regular), 500 (medium), 600 (semibold) |

### Jerarquía Tipográfica
- **`h1` (Hero / Gran Titular)**: `36px` - `48px` (Desktop) / `28px` - `32px` (Mobile) · `line-height: 1.15` · `font-weight: 700`
- **`h2` (Títulos de Bloques y Secciones)**: `26px` - `34px` · `line-height: 1.2` · `font-weight: 600`
- **`h3` (Títulos de Tarjetas / Bento Cards)**: `18px` - `22px` · `line-height: 1.3`
- **Cuerpo (`body`, `p`)**: `15px` - `16px` · `line-height: 1.65` · `color: #2D3748` o `#4A5568`
- **Pills / Badges / Metadatos**: `11px` - `13px` · `text-transform: uppercase` · `letter-spacing: 0.05em` · `font-weight: 600`

---

## 🎨 2. Paleta Cromática (Color Palette)

### Fondos y Superficies
- **Fondo Base Global (Parchment/Sand)**: `#F9F7F2` (Aporta calidez, textura acogedora y aleja el diseño del blanco clínico frío).
- **Fondo Secundario / Tarjetas Claras**: `#FFFFFF` con borde sutil `rgba(0, 0, 0, 0.06)` y sombra `box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04)`.
- **Fondo Oscuro / Hero / Footers**: `#111815` o `#151C22` (Pizarra profunda, tinta segoviana).

### Colores de Identidad y Categorías
- **🌲 Pino Silvestre (Naturaleza)**: `#176553`  
  *Uso*: Naturaleza, pinares, entorno de lagunas, badges ecológicos.
- **🧱 Resina / Tierra Arcillosa (Historia & Patrimonio)**: `#B84A28`  
  *Uso*: Historia, arquitectura popular, patrimonio monumental, botones primarios de acción.
- **✨ Ámbar / Oro Castellano (Destacados)**: `#D69E2E` / `#F6BE28`  
  *Uso*: Reportajes exclusivos, estrellas, detalles de luz, acentos cálidos.
- **🌊 Azul Tradición (Cultura)**: `#1E3A8A`  
  *Uso*: Fiestas, tradiciones, gastronomía, eventos y folclore.

---

## 🍱 3. Componentes UI Estándar

### 1. Bento Card (Tarjeta Modular)
- **Border Radius**: `16px` (móvil) a `24px` (desktop).
- **Borde**: `1px solid rgba(0, 0, 0, 0.06)` sobre fondo claro; `1px solid rgba(255, 255, 255, 0.1)` sobre fondo oscuro.
- **Glassmorphism (Overlay)**:
  ```css
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  ```
- **Transición Hover**:
  ```css
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease;
  /* Hover state */
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
  ```

### 2. Badges y Pills Temáticos
Pequeñas píldoras flotantes para categorizar artículos:
```html
<span class="badge-pill badge-naturaleza">Naturaleza</span>
<span class="badge-pill badge-historia">Historia</span>
<span class="badge-pill badge-cultura">Cultura</span>
```
```css
.badge-pill {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 9999px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #FFFFFF;
}
.badge-naturaleza { background-color: #176553; }
.badge-historia { background-color: #B84A28; }
.badge-cultura { background-color: #1E3A8A; }
.badge-destacado { background-color: #D69E2E; color: #111815; }
```

### 3. Botones y Llamadas a la Acción (CTA)
- **Botón Primario (Terracota)**:
  - Fondo: `#B84A28` · Color: `#FFFFFF` · Radio: `9999px` (Pill completa) o `12px`.
  - Padding: `12px 28px` · Tipografía: `Plus Jakarta Sans`, 600 weight.
- **Botón Secundario / Outline**:
  - Fondo: `transparent` · Borde: `1.5px solid #111815` · Color: `#111815`.

---

## 📐 4. Grillas y Responsividad (Grid & Breakpoints)

- **Desktop (≥ 1024px)**:
  - Ancho de contenedor máximo (*boxed*): `1200px` (o `1140px`).
  - Disposición Bento: Grilla de 3 o 4 columnas con tarjeta principal destacada (doble span `col-span-2`).
- **Tablet (768px – 1023px)**:
  - Grilla de 2 columnas balanceadas.
- **Mobile (< 768px)**:
  - 1 sola columna (`flex-direction: column !important; width: 100% !important;`).
  - Gaps reducidos de `24px` a `14px` - `16px`.
  - Margen lateral seguro: `16px` a cada lado (`padding: 0 16px;`).
  - Sin elementos con anchos fijos en píxeles que superen `100vw`.
