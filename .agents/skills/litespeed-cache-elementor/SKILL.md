---
name: litespeed-cache-elementor
description: >-
  Use this skill when configuring, troubleshooting, or optimizing caching with LiteSpeed Cache
  on this WordPress & Elementor Pro site, specifically for CSS/JS tuning, cache purges, and server-side rules.
---

# LiteSpeed Cache & Elementor Pro Optimization

This skill provides operational procedures for managing and troubleshooting **LiteSpeed Cache (LSCache)** on a LiteSpeed web server hosting **Elementor Pro** (`https://www.lastrasdecuellar.net`).

---

## 1. LiteSpeed Cache + Elementor Architecture

Because the server runs LiteSpeed Web Server, LSCache handles server-level page caching via rewrite rules and response headers (`X-LiteSpeed-Cache: hit/miss`).

### Critical Settings for Elementor
- **Do NOT combine CSS blindly**: Elementor loads CSS per widget/page. Combining all CSS files (`CSS Combine`) can cause layout breaks or render-blocking issues.
- **Generate Critical CSS (CCSS)**: Enable CCSS per page type (Home, Single, Archive) to eliminate render-blocking CSS.
- **Unique CSS (UCSS)**: If enabled, ensure inline CSS generation doesn't conflict with Elementor's internal CSS files.
- **Exclude from Optimization**:
  - Elementor Editor URLs: Always exclude `elementor-preview=*` and `action=elementor` from caching and minification.
  - Exclude Elementor dynamic JS: `frontend.min.js`, `webpack.runtime.min.js`.

---

## 2. Purge & Invalidation Runbook

When edits are made in Elementor or code is updated:

1. **Selective Purge vs. Full Purge**:
   - **Post/Page Edit**: LiteSpeed automatically purges the specific URL and related archives/home.
   - **Theme Builder / Global Styles / Header / Footer**: A global site part edit requires a **Purge All - LSCache** because the header/footer affects every cached page.
   - **Stale Front-end Appearance**:
     1. In Elementor MCP / Tools: Run `elementor-clear-cache` (deletes generated Elementor CSS).
     2. In LiteSpeed: Purge LSCache completely (`litespeed_purge_all()`).
     3. Clear browser cache or test in private window.

---

## 3. Image & Media Optimization via LiteSpeed / QUIC.cloud

- **WebP Replacement**: Configure LSCache Image Optimization to serve `.webp` alternatives with rewrite rules.
- **Lazy Loading**: Use LiteSpeed Responsive Placeholder and exclude the first 1-2 viewport images (hero images) from lazy loading to safeguard LCP.
