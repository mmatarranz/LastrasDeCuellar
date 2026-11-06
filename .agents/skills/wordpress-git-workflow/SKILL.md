---
name: wordpress-git-workflow
description: >-
  Use this skill when versioning code, exporting Elementor templates, managing commits,
  updating git configurations, or pushing changes to the GitHub repository (LastrasDeCuellar).
---

# WordPress & Elementor Git Workflow

This skill defines the repository management, versioning, and synchronization procedures for the **Lastras de Cuéllar** WordPress project (`https://github.com/mmatarranz/LastrasDeCuellar.git`).

---

## 1. What to Track vs. What to Ignore

### Tracked in Git:
- **Child Theme**: Custom code, templates, functions, CSS, JS (`wp-content/themes/hello-elementor-child/`).
- **Custom Plugins / Must-Use Plugins**: Custom post types, integrations (`wp-content/mu-plugins/` or custom plugin folders).
- **Elementor Template Exports**: Exported JSON templates (Theme Builder headers, footers, popups, kits) stored under an `elementor-templates/` directory for version-controlled backups and portability.
- **Project Documentation & Skills**: `.agents/skills/`, `README.md`, changelogs, architecture notes.

### Ignored in Git (`.gitignore`):
- `wp-config.php` and any files containing database passwords or salts.
- WordPress Core files (`wp-admin/`, `wp-includes/`, root WordPress php files).
- Media uploads (`wp-content/uploads/`).
- Cache directories (`wp-content/cache/`, `wp-content/et-cache/`, etc.).
- Third-party plugins and themes installed from official repositories (track Composer/dependency lists instead if applicable).
- Environment secrets (`.env`, `*.local`).

---

## 2. Elementor Template Versioning Workflow

Because Elementor stores page content in the WordPress database (post meta `_elementor_data`), use this procedure to track key layouts in Git:

1. **Export Critical Templates**:
   - Export Theme Builder parts (Header, Footer, Single Post, Archive) or Page Kits as JSON files.
   - Save them into `templates/elementor/` in the workspace:
     ```
     templates/elementor/
     ├── header-site.json
     ├── footer-site.json
     ├── single-noticia.json
     └── site-settings-kit.json
     ```
2. **Commit and Version**:
   - Commit template JSON alongside relevant custom CSS/PHP changes so that design and code revisions align.

---

## 3. Commit & Push Procedures

- **Semantic Commit Messages**:
  - `feat(theme): add custom taxonomy for events`
  - `style(elementor): update global typography tokens`
  - `fix(header): correct sticky header layout shift on mobile`
  - `docs(skills): add elementor performance runbook`

- **Pushing via SSH**:
  - The repository remote is configured with SSH: `git@github.com:mmatarranz/LastrasDeCuellar.git`.
  - Always verify status before committing:
    ```bash
    git status
    git add <modified-files>
    git commit -m "<semantic message>"
    git push origin main
    ```
