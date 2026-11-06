# Project Guidelines: Lastras de Cuéllar (WordPress & Elementor Pro)

## Project Stack & Standards
- **CMS**: WordPress
- **Page Builder**: Elementor & Elementor Pro
- **Architecture**: Flexbox / CSS Grid Containers (avoid legacy sections/columns)
- **Theme**: Hello Elementor (with Child Theme for custom modifications)
- **Remote Repository**: `git@github.com:mmatarranz/LastrasDeCuellar.git` (branch `main`)

## Core Directives
1. **Never edit parent theme or core files**: All PHP functions, filters, and custom CSS must go inside the child theme or dedicated custom plugins.
2. **Elementor MCP Integration**: When using `elementor-lastras-de-cuellar-segovia`, adhere to atomic operations, verify element IDs, and never trigger `elementor-clear-cache` automatically on routine edits.
3. **Responsive & Mobile-First**: In Elementor styles, use `@media (--mobile)` and `@media (--tablet)` rather than hardcoded pixel media queries.
4. **Git Discipline**: Keep sensitive credentials (`wp-config.php`, `.env`, database dumps) and heavy user uploads (`wp-content/uploads/`) strictly out of git. Commit changes with semantic messages and sync to GitHub.
