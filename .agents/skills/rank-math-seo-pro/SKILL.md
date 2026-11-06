---
name: rank-math-seo-pro
description: >-
  Use this skill when managing on-page SEO, rich schema markup (JSON-LD), XML sitemaps,
  redirects, and metadata for WordPress & Elementor Pro using Rank Math SEO PRO.
---

# Rank Math SEO PRO & Elementor Integration

This skill outlines guidelines and workflows for managing SEO, schema markup, and metadata on **Lastras de Cuéllar** (`https://www.lastrasdecuellar.net`) using **Rank Math SEO PRO**.

---

## 1. Schema Markup (JSON-LD) Strategy

Because this is a municipal/regional portal (Lastras de Cuéllar, Segovia), apply proper structured data:

1. **LocalBusiness / GovernmentOrganization / Place**:
   - Primary entity for village / council / tourism services.
   - Include geo-coordinates, address (40749 Lastras de Cuéllar, Segovia), official contact, and logo.

2. **Articles / News (`Single Post`)**:
   - Integrate with Elementor Single Post template (`ID 22328`).
   - Primary schema: `Article` or `NewsArticle`.
   - Ensure `headline`, `image`, `datePublished`, `dateModified`, and `author` map correctly.

3. **Events (`Event` schema)**:
   - For local festivities (Fiestas patronales, eventos culturales), configure the `Event` schema with `startDate`, `endDate`, `location`, and `eventStatus`.

---

## 2. On-Page SEO in Elementor

- **Elementor Editor Integration**:
  - Rank Math integrates into the Elementor left sidebar panel under the SEO icon.
  - Review Focus Keyword density, Title snippet, Meta description, and Social previews (OpenGraph & Twitter Card).

- **Breadcrumbs**:
  - Use Rank Math Breadcrumbs widget or shortcode `[rank_math_breadcrumb]` inside Elementor single templates.
  - Improves UX and enables rich Google SERP breadcrumb pathways.

---

## 3. Redirections & 404 Monitoring

- With **Rank Math SEO PRO**:
  - Automatically track 404 errors (useful when old URL structures or attachments are changed).
  - Set up 301 Permanent Redirects for modified slugs or migrated content.
  - Keep XML Sitemaps updated and submitted to Google Search Console via Site Kit.
