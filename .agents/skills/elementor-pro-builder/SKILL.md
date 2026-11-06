---
name: elementor-pro-builder
description: >-
  Use this skill whenever creating, modifying, inspecting, or managing WordPress pages,
  Theme Builder templates (Header, Footer, Single, Archive, Loop Item, Popup), global styles,
  or containers in Elementor Pro, particularly when using the Elementor MCP tools.
---

# Elementor Pro Site Builder & MCP Workflows

This skill guides the design, construction, and modification of layouts and templates in WordPress using **Elementor Pro** and the `elementor-lastras-de-cuellar-segovia` MCP server.

---

## 1. Core Architecture Principles

1. **Flexbox & Grid Containers**:
   - Always use Elementor Flexbox Containers (e-con) or Grid Containers. Never use legacy section/column wrappers.
   - Keep the DOM tree as shallow as possible (maximum 2-3 levels of nested containers).

2. **Global Design System First**:
   - Define and reuse Global Colors (`primary`, `secondary`, `text`, `accent`) and Global Fonts (Typography).
   - Use CSS classes or global styles instead of inline widget styling whenever repeating elements.

3. **Theme Builder for Scalability**:
   - Never duplicate headers, footers, or single post layouts manually across pages.
   - Use Elementor Pro Theme Builder site parts (`header`, `footer`, `single`, `single-post`, `single-page`, `archive`, `loop-item`, `error-404`).

4. **Responsive Breakpoints**:
   - Design Mobile-First or Desktop-First with explicit mobile/tablet adaptations.
   - In Elementor CSS rules, use breakpoint syntax `@media (--mobile)` or `@media (--tablet)` rather than arbitrary pixel queries.

---

## 2. Elementor MCP Tool Runbook

When using `elementor-lastras-de-cuellar-segovia`:

### A. Inspecting Existing Pages or Site Parts
- **List site parts**: Call `elementor-list-site-parts` to discover headers, footers, popups, and singles.
- **Inspect page structure**: Call `elementor-get-page-structure` with `post_id` to examine container hierarchy and element IDs.
- **List posts/pages**: Call `elementor-list-posts` to find page IDs, titles, and publication status.

### B. Theme Builder Templates (`elementor-manage-site-parts`)
- **Actions**:
  - `create`: Creates a draft site part (`section`, `popup`, `header`, `footer`, `single`, `single-post`, `single-page`, `archive`, `search-results`, `error-404`, `loop-item`).
  - `update`: Updates conditions (e.g., `include/general`, `include/singular/post`, `exclude/singular/post/42`) and popup triggers.
  - `delete`: Removes a site part.
- *Note*: Newly created site parts are drafts. Call `elementor-publish-document` to publish them when ready.

### C. Building & Editing Elements
- **Composition**: Use `elementor-build-composition` to generate layouts with semantic elements.
- **Surgical Edits**: Use `elementor-manage-elements` for bulk updates (up to 50 operations):
  - `action="update"`: Updates settings, layer names, plain-CSS string styles.
  - `action="delete"`: Removes element.
  - `action="move"`: Re-parents under `new_parent_id`.
  - `action="duplicate"`: Clones an element.
- *Caution*: Do NOT reuse old element IDs from an earlier read if `build-composition` was run in between.

### D. Global Variables & Classes
- Check and update global design tokens using:
  - `elementor-manage-global-variable`
  - `elementor-manage-classes`
  - `elementor-get-default-styles` / `elementor-manage-default-styles`

### E. Previewing & Publishing
- **Preview Link**: Generate an authenticated preview via `elementor-create-preview-link`.
- **Publish**: Call `elementor-publish-document` with `post_id` when the user approves changes.
- **Cache**: Call `elementor-clear-cache` only when troubleshooting stale CSS or front-end discrepancies, never systematically.

---

## 3. Elementor Pro Dynamic Content & Forms

- **Dynamic Tags**: For custom post meta (ACF, Pods, or native meta), bind widget content to dynamic tags instead of hardcoding text.
- **Form Widget**:
  - Configure form actions after submit (Email, Webhook, Redirect, Mailchimp, etc.).
  - Review form submissions with `elementor-list-form-submissions` and `elementor-manage-form-submissions`.
