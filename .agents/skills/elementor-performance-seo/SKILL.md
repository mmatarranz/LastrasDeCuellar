---
name: elementor-performance-seo
description: >-
  Use this skill to optimize Core Web Vitals (LCP, CLS, INP), reduce DOM depth,
  improve page load speeds, configure caching, manage typography/fonts, and implement
  technical SEO and accessibility best practices for Elementor Pro and WordPress sites.
---

# Elementor Pro Performance, CWV & SEO Optimization

This skill provides guidelines to ensure that WordPress sites built with Elementor Pro achieve high performance scores (90+ Google PageSpeed / Lighthouse), optimal Core Web Vitals, and solid technical SEO.

---

## 1. Core Web Vitals Optimization

### Largest Contentful Paint (LCP)
- **Hero Image Preloading**: If the hero image is the LCP element, ensure `fetchpriority="high"` and avoid lazy loading for the first viewport image.
- **Font Rendering**: Set `font-display: swap` for all fonts to prevent FOIT (Flash of Invisible Text). Host fonts locally or disable unused Google font weights.
- **Server Response**: Recommend page caching (e.g. WP Rocket, LiteSpeed, or server-level FastCGI/Redis cache).

### Cumulative Layout Shift (CLS)
- **Image & Video Dimensions**: Always specify explicit `width` and `height` attributes on images, logos, and video containers.
- **Elementor Popups & Sticky Headers**: Ensure sticky headers have a dedicated placeholder or fixed min-height to prevent sudden content jumps during scroll.
- **Web Fonts**: Use fallback fonts with matched metrics (`size-adjust`, `ascent-override`) to avoid layout jumps when custom fonts load.

### Interaction to Next Paint (INP)
- **Debounce/Throttle Event Listeners**: Ensure custom scripts attached to scroll, resize, or input events are throttled.
- **Minimize Third-Party Scripts**: Defer tracking pixels (Google Analytics, Tag Manager, Meta Pixel) until user interaction when possible.

---

## 2. Elementor DOM & Feature Tuning

1. **Enable Performance Features (WP Admin → Elementor → Settings → Features)**:
   - **Optimized DOM Output**: Removes wrapper divs.
   - **Improved Asset Loading**: Loads only the CSS/JS required for widgets present on the page.
   - **Improved CSS Loading**: Renders CSS inline or conditionally.
   - **Font Awesome Inline Rendering**: Inlines SVG icons instead of loading full font libraries (`font-awesome.min.css`).

2. **Container Hygiene**:
   - Limit nesting depth to 2–3 levels.
   - Use Flexbox `gap` instead of multiple nested containers or margin hacking.
   - Avoid empty spacer widgets; use container padding/margin or flex gap.

3. **Cache Invalidation Runbook**:
   - When front-end styles look outdated or broken after updates, use `elementor-clear-cache`.
   - Never call `elementor-clear-cache` automatically after every small edit; only when resolving stale rendered assets.

---

## 3. Technical SEO & Semantic HTML

1. **Heading Hierarchy**:
   - Exactly **one** `<h1>` per page (typically the page title or hero heading).
   - Follow logical sequential order: `<h1>` → `<h2>` → `<h3>`. Never skip levels for visual sizing (use Elementor Typography styling to resize an `<h2>` if needed, rather than misusing an `<h4>`).

2. **Semantic HTML Tags in Elementor**:
   - In container and widget settings, configure the HTML Tag:
     - Header container: `<header>`
     - Main content container: `<main>`
     - Footer container: `<footer>`
     - Navigation: `<nav>`
     - Articles / blog cards: `<article>`
     - Sidebar / complementary: `<aside>`

3. **Images & Accessibility**:
   - Meaningful `alt` text for informative images; empty `alt=""` for purely decorative elements.
   - Ensure color contrast ratio meets WCAG AA (at least 4.5:1 for normal text, 3:1 for large text).
   - Ensure all interactive elements (buttons, links) have accessible names and visible focus states.
