#!/usr/bin/env python3
"""
Generador y publicador integral de la página monográfica:
'Alfareros y Tejeros de Lastras de Cuéllar: Historia, Barro y Fuego' (ID 26499).
"""

import json
import urllib.request
import re

PAGE_ID = 26499
PAGE_SLUG = "alfareros-y-tejeros-lastras-de-cuellar"
PAGE_TITLE = "Alfareros y Tejeros de Lastras de Cuéllar: Historia, Barro y Fuego"

URL_PAGE = f"https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/{PAGE_ID}?context=edit"
URL_HEADER = "https://www.lastrasdecuellar.net/wp-json/wp/v2/elementor_library/13859?context=edit"
URL_FOOTER = "https://www.lastrasdecuellar.net/wp-json/wp/v2/elementor_library/26318?context=edit"

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
auth_header = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

def fetch_json(url):
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def post_json(url, payload):
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))

def generate_html_content():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,400;1,600&display=swap');

:root {
  --pot-dark: #191412;
  --pot-dark-soft: #26201D;
  --pot-terracotta: #A84323;
  --pot-terracotta-hover: #8D361B;
  --pot-terracotta-soft: #F9EFEA;
  --pot-clay: #C25B35;
  --pot-ochre: #C07D2B;
  --pot-ochre-soft: #FDF6EC;
  --pot-pine: #264A3F;
  --pot-pine-soft: #EBF3F0;
  --pot-sand: #FAF7F2;
  --pot-sand-soft: #F3EFE8;
  --pot-card-bg: #FFFFFF;
  --pot-border: #E8E1D5;
  --pot-border-subtle: #F0EBE1;
  --pot-text: #2D2622;
  --pot-text-muted: #635A53;
  --pot-text-light: #8C8279;
  --pot-radius: 16px;
  --pot-radius-sm: 10px;
  --pot-shadow-sm: 0 4px 14px rgba(25, 20, 18, 0.05);
  --pot-shadow-md: 0 10px 28px rgba(25, 20, 18, 0.08);
  --pot-shadow-lg: 0 20px 48px rgba(25, 20, 18, 0.13);
}

.pot-wrap {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  color: var(--pot-text);
  background-color: var(--pot-sand);
  overflow-x: hidden;
  line-height: 1.7;
}

.pot-wrap * {
  box-sizing: border-box;
}

.pot-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ==========================================================================
   1. HERO SECTION
   ========================================================================== */
.pot-hero {
  position: relative;
  background: linear-gradient(135deg, #181311 0%, #291F1A 50%, #38241D 100%);
  color: #FFFFFF;
  padding: 72px 0 80px;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.pot-hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: 
    radial-gradient(circle at 15% 20%, rgba(194, 91, 53, 0.22) 0%, transparent 45%),
    radial-gradient(circle at 85% 80%, rgba(192, 125, 43, 0.18) 0%, transparent 50%);
  pointer-events: none;
}

.pot-hero-inner {
  position: relative;
  z-index: 2;
  max-width: 960px;
  margin: 0 auto;
  text-align: center;
}

.pot-breadcrumbs {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.65);
  margin-bottom: 24px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.pot-breadcrumbs a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.2s;
}

.pot-breadcrumbs a:hover {
  color: #FFFFFF;
}

.pot-badge {
  display: inline-block;
  background: rgba(194, 91, 53, 0.25);
  color: #FFAE8A;
  border: 1px solid rgba(194, 91, 53, 0.45);
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 22px;
}

.pot-hero h1 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.4rem, 5vw, 3.8rem);
  font-weight: 800;
  line-height: 1.15;
  margin: 0 0 24px;
  color: #FFFFFF;
  letter-spacing: -0.02em;
}

.pot-hero-lead {
  font-size: clamp(1.08rem, 2vw, 1.25rem);
  color: rgba(255, 255, 255, 0.88);
  font-weight: 400;
  line-height: 1.65;
  margin: 0 auto 48px;
  max-width: 840px;
}

/* Stats Grid */
.pot-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 20px;
}

.pot-stat-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--pot-radius-sm);
  padding: 20px 16px;
  text-align: center;
  transition: transform 0.25s ease, background 0.25s ease;
}

.pot-stat-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.1);
}

.pot-stat-num {
  display: block;
  font-family: 'Playfair Display', serif;
  font-size: 1.9rem;
  font-weight: 800;
  color: #FFAE8A;
  line-height: 1.1;
  margin-bottom: 6px;
}

.pot-stat-lbl {
  font-size: 0.78rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  line-height: 1.35;
}

/* ==========================================================================
   2. COMMON SECTION STYLES
   ========================================================================== */
.pot-section {
  padding: 88px 0;
}

.pot-section-soft {
  background-color: var(--pot-sand-soft);
  border-top: 1px solid var(--pot-border-subtle);
  border-bottom: 1px solid var(--pot-border-subtle);
}

.pot-sec-header {
  text-align: center;
  max-width: 780px;
  margin: 0 auto 56px;
}

.pot-sec-tag {
  display: inline-block;
  color: var(--pot-terracotta);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.pot-sec-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2rem, 3.5vw, 2.7rem);
  font-weight: 800;
  color: var(--pot-dark);
  line-height: 1.22;
  margin: 0 0 16px;
}

.pot-sec-sub {
  font-size: 1.05rem;
  color: var(--pot-text-muted);
  line-height: 1.6;
  margin: 0;
}

/* ==========================================================================
   3. STORY SPLIT (Capítulo 1 & 4)
   ========================================================================== */
.pot-story-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 52px;
  align-items: center;
  margin-bottom: 30px;
}

.pot-story-split.reverse {
  grid-template-columns: 1fr 1fr;
}

.pot-story-content h3 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.6rem, 2.5vw, 2.1rem);
  font-weight: 700;
  color: var(--pot-dark);
  line-height: 1.25;
  margin: 0 0 20px;
}

.pot-story-content p {
  color: var(--pot-text);
  font-size: 1.02rem;
  line-height: 1.75;
  margin-bottom: 18px;
}

.pot-story-content strong {
  color: var(--pot-dark);
  font-weight: 600;
}

.pot-story-media {
  position: relative;
}

.pot-story-img-frame {
  position: relative;
  border-radius: var(--pot-radius);
  overflow: hidden;
  box-shadow: var(--pot-shadow-lg);
  border: 1px solid var(--pot-border);
  background: #E8E2D8;
}

.pot-story-img-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.pot-story-img-frame:hover img {
  transform: scale(1.02);
}

.pot-media-caption {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(to top, rgba(25, 20, 18, 0.92) 0%, rgba(25, 20, 18, 0.6) 70%, transparent 100%);
  color: #FFFFFF;
  padding: 24px 20px 14px;
  font-size: 0.85rem;
  line-height: 1.45;
}

.pot-media-caption strong {
  color: #FFAE8A;
}

/* ==========================================================================
   4. INFOGRAFÍA SHOWCASE (El Diorama y su análisis)
   ========================================================================== */
.pot-infografia-wrap {
  background: var(--pot-card-bg);
  border-radius: var(--pot-radius);
  border: 1px solid var(--pot-border);
  box-shadow: var(--pot-shadow-lg);
  overflow: hidden;
  margin-bottom: 44px;
}

.pot-infografia-img-box {
  position: relative;
  background: #ECE5DC;
  text-align: center;
  padding: 12px;
}

.pot-infografia-img-box img {
  width: 100%;
  height: auto;
  max-height: 650px;
  object-fit: contain;
  display: block;
  border-radius: calc(var(--pot-radius) - 4px);
}

.pot-infografia-bar {
  background: var(--pot-dark-soft);
  color: #FFFFFF;
  padding: 18px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.pot-infografia-bar-text {
  font-size: 0.92rem;
  color: rgba(255, 255, 255, 0.85);
}

.pot-infografia-bar-text strong {
  color: #FFAE8A;
}

.pot-infografia-bar-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--pot-terracotta);
  color: #FFFFFF !important;
  text-decoration: none;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 9px 18px;
  border-radius: 6px;
  transition: background 0.2s;
}

.pot-infografia-bar-btn:hover {
  background: var(--pot-terracotta-hover);
}

/* Timeline Cards below Infografía */
.pot-era-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.pot-era-card {
  background: var(--pot-card-bg);
  border-radius: var(--pot-radius);
  border: 1px solid var(--pot-border);
  padding: 28px 24px;
  box-shadow: var(--pot-shadow-sm);
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  position: relative;
}

.pot-era-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--pot-shadow-md);
  border-color: var(--pot-clay);
}

.pot-era-badge {
  display: inline-block;
  background: var(--pot-terracotta-soft);
  color: var(--pot-terracotta);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 12px;
  border-radius: 50px;
  width: fit-content;
  margin-bottom: 14px;
}

.pot-era-card h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--pot-dark);
  margin: 0 0 12px;
  line-height: 1.3;
}

.pot-era-card p {
  color: var(--pot-text-muted);
  font-size: 0.94rem;
  line-height: 1.65;
  margin: 0;
}

/* ==========================================================================
   5. DOCUMENTACIÓN HISTÓRICA (Parchment Grid)
   ========================================================================== */
.pot-docs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
}

.pot-doc-card {
  background: #FFFDF9;
  border-radius: var(--pot-radius);
  border: 1px solid var(--pot-border);
  border-left: 5px solid var(--pot-terracotta);
  padding: 30px;
  box-shadow: var(--pot-shadow-sm);
  transition: transform 0.25s ease;
}

.pot-doc-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--pot-shadow-md);
}

.pot-doc-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.pot-doc-year {
  font-family: 'Playfair Display', serif;
  font-size: 1.45rem;
  font-weight: 800;
  color: var(--pot-terracotta);
}

.pot-doc-tag {
  background: var(--pot-sand-soft);
  color: var(--pot-text-muted);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 3px 10px;
  border-radius: 4px;
  border: 1px solid var(--pot-border-subtle);
}

.pot-doc-card h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--pot-dark);
  margin: 0 0 12px;
  line-height: 1.3;
}

.pot-doc-card p {
  color: var(--pot-text);
  font-size: 0.95rem;
  line-height: 1.65;
  margin: 0 0 14px;
}

.pot-doc-quote {
  background: var(--pot-terracotta-soft);
  border-left: 3px solid var(--pot-clay);
  padding: 12px 16px;
  font-style: italic;
  font-size: 0.9rem;
  color: var(--pot-text);
  border-radius: 0 8px 8px 0;
  margin: 0;
}

/* ==========================================================================
   6. BENTO GRID (Tejería vs Alfarería)
   ========================================================================== */
.pot-bento-duo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.pot-bento-card {
  background: var(--pot-card-bg);
  border-radius: var(--pot-radius);
  border: 1px solid var(--pot-border);
  overflow: hidden;
  box-shadow: var(--pot-shadow-md);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.pot-bento-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--pot-shadow-lg);
}

.pot-bento-thumb {
  height: 280px;
  overflow: hidden;
  position: relative;
  background: #201A17;
}

.pot-bento-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.pot-bento-card:hover .pot-bento-thumb img {
  transform: scale(1.04);
}

.pot-bento-badge {
  position: absolute;
  top: 16px; left: 16px;
  background: rgba(25, 20, 18, 0.85);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  color: #FFAE8A;
  font-size: 0.74rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 5px 12px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.pot-bento-body {
  padding: 32px 28px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.pot-bento-body h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--pot-dark);
  margin: 0 0 14px;
  line-height: 1.25;
}

.pot-bento-body p {
  color: var(--pot-text-muted);
  font-size: 0.98rem;
  line-height: 1.7;
  margin-bottom: 20px;
}

.pot-bento-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pot-bento-list li {
  font-size: 0.92rem;
  color: var(--pot-text);
  display: flex;
  align-items: flex-start;
  gap: 10px;
  line-height: 1.5;
}

.pot-bento-list li::before {
  content: '✔';
  color: var(--pot-terracotta);
  font-weight: bold;
  font-size: 0.85rem;
  margin-top: 1px;
}

.pot-bento-link {
  margin-top: auto;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--pot-terracotta);
  font-weight: 700;
  font-size: 0.92rem;
  text-decoration: none;
  transition: gap 0.2s, color 0.2s;
}

.pot-bento-link:hover {
  color: var(--pot-terracotta-hover);
  gap: 12px;
}

/* ==========================================================================
   7. PROCESO ARTESANAL (4 Pasos)
   ========================================================================== */
.pot-process-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.pot-process-card {
  background: var(--pot-card-bg);
  border-radius: var(--pot-radius);
  border: 1px solid var(--pot-border);
  padding: 26px 20px;
  box-shadow: var(--pot-shadow-sm);
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease;
  position: relative;
}

.pot-process-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--pot-shadow-md);
  border-color: var(--pot-clay);
}

.pot-step-number {
  font-family: 'Playfair Display', serif;
  font-size: 2.2rem;
  font-weight: 800;
  color: #FFAE8A;
  line-height: 1;
  margin-bottom: 12px;
}

.pot-process-card h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1.22rem;
  font-weight: 700;
  color: var(--pot-dark);
  margin: 0 0 10px;
  line-height: 1.3;
}

.pot-process-card p {
  color: var(--pot-text-muted);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
}

/* ==========================================================================
   8. ROSTROS Y MEMORIA (Ignacio Sanz y los Alfareros)
   ========================================================================== */
.pot-masters-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 48px;
}

.pot-master-card {
  background: var(--pot-card-bg);
  border-radius: var(--pot-radius);
  border: 1px solid var(--pot-border);
  padding: 28px 24px;
  box-shadow: var(--pot-shadow-sm);
}

.pot-master-role {
  color: var(--pot-terracotta);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
  display: block;
}

.pot-master-card h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--pot-dark);
  margin: 0 0 12px;
}

.pot-master-card p {
  color: var(--pot-text-muted);
  font-size: 0.92rem;
  line-height: 1.65;
  margin: 0;
}

/* Quote Box Ignacio Sanz */
.pot-quote-box {
  background: linear-gradient(135deg, #261F1C 0%, #1A1513 100%);
  color: #FFFFFF;
  border-radius: var(--pot-radius);
  padding: 44px 48px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: var(--pot-shadow-lg);
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 40px;
  align-items: center;
}

.pot-quote-text blockquote {
  margin: 0 0 16px;
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.2rem, 2vw, 1.45rem);
  font-style: italic;
  line-height: 1.55;
  color: #FFFFFF;
}

.pot-quote-author {
  font-size: 0.92rem;
  color: #FFAE8A;
  font-weight: 600;
}

.pot-quote-author span {
  display: block;
  color: rgba(255, 255, 255, 0.65);
  font-size: 0.82rem;
  font-weight: 400;
  margin-top: 4px;
}

.pot-quote-frame {
  border-radius: var(--pot-radius-sm);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--pot-shadow-md);
}

.pot-quote-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ==========================================================================
   9. CALL TO ACTION / ARCHIVO COLABORATIVO
   ========================================================================== */
.pot-cta-section {
  padding: 96px 0;
  background: linear-gradient(135deg, #A84323 0%, #8D361B 100%);
  color: #FFFFFF;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.pot-cta-section::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(circle at 50% 30%, rgba(255, 255, 255, 0.15) 0%, transparent 60%);
  pointer-events: none;
}

.pot-cta-inner {
  position: relative;
  z-index: 2;
  max-width: 760px;
  margin: 0 auto;
}

.pot-cta-section h2 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2rem, 3.5vw, 2.7rem);
  font-weight: 800;
  margin: 0 0 18px;
  color: #FFFFFF;
  line-height: 1.2;
}

.pot-cta-section p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.7;
  margin: 0 auto 36px;
}

.pot-cta-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.pot-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  text-decoration: none;
  min-height: 48px;
  transition: all 0.25s ease;
}

.pot-btn-primary {
  background: #FFFFFF;
  color: var(--pot-dark) !important;
  box-shadow: var(--pot-shadow-md);
}

.pot-btn-primary:hover {
  background: #FAF7F2;
  transform: translateY(-2px);
  box-shadow: var(--pot-shadow-lg);
}

.pot-btn-outline {
  background: transparent;
  color: #FFFFFF !important;
  border: 1.5px solid rgba(255, 255, 255, 0.7);
}

.pot-btn-outline:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: #FFFFFF;
  transform: translateY(-2px);
}

/* ==========================================================================
   10. RESPONSIVE BREAKPOINTS (Mobile-First / Anti-Overflow)
   ========================================================================== */
@media (max-width: 960px) {
  .pot-story-split, 
  .pot-story-split.reverse {
    grid-template-columns: 1fr;
    gap: 36px;
  }
  .pot-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .pot-era-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .pot-docs-grid {
    grid-template-columns: 1fr;
  }
  .pot-bento-duo {
    grid-template-columns: 1fr;
    gap: 28px;
  }
  .pot-process-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .pot-masters-grid {
    grid-template-columns: 1fr;
  }
  .pot-quote-box {
    grid-template-columns: 1fr;
    padding: 32px 24px;
    text-align: center;
  }
  .pot-quote-frame {
    max-width: 220px;
    margin: 0 auto;
  }
}

@media (max-width: 600px) {
  .pot-hero {
    padding: 48px 0 56px;
  }
  .pot-section {
    padding: 60px 0;
  }
  .pot-stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .pot-stat-card {
    padding: 14px 10px;
  }
  .pot-stat-num {
    font-size: 1.55rem;
  }
  .pot-stat-lbl {
    font-size: 0.7rem;
  }
  .pot-process-grid {
    grid-template-columns: 1fr;
  }
  .pot-doc-card {
    padding: 22px 18px;
  }
  .pot-bento-body {
    padding: 24px 20px;
  }
  .pot-cta-section {
    padding: 68px 0;
  }
}
</style>

<div class="pot-wrap">

  <!-- =====================================================================
       1. HERO DE PORTADA
       ===================================================================== -->
  <header class="pot-hero">
    <div class="pot-container">
      <div class="pot-hero-inner">
        <nav class="pot-breadcrumbs" aria-label="Migas de pan">
          <a href="https://www.lastrasdecuellar.net/">Inicio</a>
          <span>›</span>
          <a href="https://www.lastrasdecuellar.net/lastras-de-cuellar/cultura-y-tradicion/">Cultura y Tradición</a>
          <span>›</span>
          <span>Alfareros y Tejeros</span>
        </nav>

        <span class="pot-badge">OFICIO Y PATRIMONIO HISTÓRICO • TIERRA DE PINARES</span>

        <h1>Tierra, Barro y Fuego: Historia de Alfareros y Tejeros en Lastras de Cuéllar</h1>

        <p class="pot-hero-lead">
          Mucho antes de que el pinar y las fábricas de resina marcaran el ritmo de la comarca, el barro ya había fundado Lastras. De las lomas arcillosas de <em>Los Barreros</em> a las cubiertas mudéjares de toda la provincia, esta es la historia viva de los artesanos que convirtieron la arcilla roja en el marchamo eterno de nuestra identidad.
        </p>

        <!-- Stats Grid -->
        <div class="pot-stats-grid">
          <div class="pot-stat-card">
            <span class="pot-stat-num">1210</span>
            <span class="pot-stat-lbl">Primera cita documental por Alfonso VIII</span>
          </div>
          <div class="pot-stat-card">
            <span class="pot-stat-num">100.000</span>
            <span class="pot-stat-lbl">Maravedíes: tasación del horno en 1523</span>
          </div>
          <div class="pot-stat-card">
            <span class="pot-stat-num">Ley 139</span>
            <span class="pot-stat-lbl">Ordenanzas de 1546 de Villa y Tierra</span>
          </div>
          <div class="pot-stat-card">
            <span class="pot-stat-num">Media Docena</span>
            <span class="pot-stat-lbl">Alfares familiares activos en el siglo XX</span>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- =====================================================================
       2. CAPÍTULO I: EL BARRO QUE FUNDÓ UN PUEBLO (ORÍGENES)
       ===================================================================== -->
  <main>
    <section class="pot-section" id="origenes">
      <div class="pot-container">
        <div class="pot-story-split">
          <div class="pot-story-content">
            <span class="pot-sec-tag">Capítulo I • Orígenes y Asentamiento Medieval</span>
            <h3>De la Leyenda al Altozano: El Barro que Fundó un Pueblo</h3>
            <p>
              La tradición oral y la memoria colectiva de Lastras de Cuéllar guardan un relato fundacional indisociable de la arcilla. En la Edad Media, los primitivos pobladores habitaban núcleos cercanos enclavados en los valles bajos —como <strong>San Esteban</strong> o <strong>Santa María de Salcedón</strong>—. Sin embargo, las humedades estancadas, las fiebres y las plagas de aquellas vegas obligaron a una migración paulatina.
            </p>
            <p>
              Día tras día, los antiguos tejeros subían a trabajar al altozano ventoso o <em>cotarro</em> donde afloraban los ricos depósitos de barro. Comprendieron que allí, donde corría el aire sano y seco y la tierra roja ofrecía sustento ilimitado, era el lugar idóneo para levantar sus casas. Así nació el asentamiento definitivo de <strong>La Lastra</strong>.
            </p>
            <p>
              El enciclopedista Sebastián Miñano (1826) atribuyó el inicio del oficio a <em>"artesanos navarros"</em> que descubrieron la calidad de las vetas. Hoy la investigación histórica matiza esa leyenda: en realidad se trataba de los colonos del norte traídos en el siglo XII por el <strong>Conde Pedro Ansúrez</strong> desde sus señoríos en <strong>Liébana</strong> y tierras palentinas, verdaderos maestros en el arte del ladrillo y la teja.
            </p>
          </div>

          <div class="pot-story-media">
            <div class="pot-story-img-frame">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/alfareros-lastras-de-cuellar.jpg" alt="Alfareros tradicionales de Lastras de Cuéllar trabajando en el taller" loading="lazy" />
              <div class="pot-media-caption">
                <strong>Alfares de Lastras:</strong> Transmisión hereditaria de un oficio secular arraigado en el altozano arcilloso del pueblo.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =====================================================================
         3. EJE CENTRAL: INFOGRAFÍA Y CRONOLOGÍA (EL DIORAMA)
         ===================================================================== -->
    <section class="pot-section pot-section-soft" id="cronologia">
      <div class="pot-container">
        <div class="pot-sec-header">
          <span class="pot-sec-tag">Eje Cronológico • Diorama Etnográfico</span>
          <h2 class="pot-sec-title">El Legado Barro y Fuego: Ocho Siglos de Historia</h2>
          <p class="pot-sec-sub">
            Una reconstrucción visual que conecta la fundación medieval, el monopolio proveedor de la Tierra de Pinares y el ocaso industrial recogido por la memoria viva.
          </p>
        </div>

        <!-- Infografía Box -->
        <div class="pot-infografia-wrap">
          <div class="pot-infografia-img-box">
            <img src="https://www.lastrasdecuellar.net/wp-content/uploads/historia-alfareros-tejeros-lastras-de-cuellar.jpg" alt="Infografía diorama: Historia de Alfareros y Tejeros en Lastras de Cuéllar" loading="lazy" />
          </div>
          <div class="pot-infografia-bar">
            <div class="pot-infografia-bar-text">
              <strong>Infografía Oficial del Archivo:</strong> Síntesis diorama de las tres grandes eras históricas y el ciclo tradicional del barro en Lastras de Cuéllar.
            </div>
            <a href="https://www.lastrasdecuellar.net/wp-content/uploads/historia-alfareros-tejeros-lastras-de-cuellar.jpg" target="_blank" rel="noopener noreferrer" class="pot-infografia-bar-btn">
              <span>🔍 Ver en Alta Resolución</span>
            </a>
          </div>
        </div>

        <!-- 3 Eras Grid -->
        <div class="pot-era-grid">
          <div class="pot-era-card">
            <span class="pot-era-badge">Siglos XII – XIII</span>
            <h4>Orígenes y Asentamiento</h4>
            <p>
              Surgimiento del poblado en el cotarro alto junto a los barreros para escapar de las fiebres. En <strong>1210</strong>, Alfonso VIII delimita términos con Sepúlveda registrando formalmente el topónimo <em>La Lastra</em>. Primeros hornos de leña y teja curva árabe.
            </p>
          </div>

          <div class="pot-era-card">
            <span class="pot-era-badge">Siglos XVI – XIX</span>
            <h4>Apogeo y Suministro Comarcal</h4>
            <p>
              Lastras se consagra como la gran "fábrica" de material cerámico de la comarca. La <strong>Ley 139</strong> de las Ordenanzas de Cuéllar (1546) regula su producción. Exportación masiva de tejas y vasijas a Cuéllar, Calabazas, Sepúlveda y Fuentepiñel.
            </p>
          </div>

          <div class="pot-era-card">
            <span class="pot-era-badge">Siglo XX</span>
            <h4>Cénit, Ocaso y Rescate</h4>
            <p>
              Convivencia de media docena de alfares familiares y mecanización parcial con la "galletera" de Los Moscos. Hacia 1970 la industria moderna silencia los tornos, pero ceramistas como <strong>Ignacio Sanz</strong> documentan su memoria eterna.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- =====================================================================
         4. CAPÍTULO II: DOCUMENTACIÓN Y MARCO LEGAL PROTECCIONISTA
         ===================================================================== -->
    <section class="pot-section" id="documentos">
      <div class="pot-container">
        <div class="pot-sec-header">
          <span class="pot-sec-tag">Capítulo II • Archivos y Pergaminos</span>
          <h2 class="pot-sec-title">Una Industria Blindada por Ley y Tasada en Oro</h2>
          <p class="pot-sec-sub">
            Los pergaminos notariales, ordenanzas comarcales y libros de fábrica demuestran que la cerámica lastreña no era una tarea de subsistencia, sino una formidable potencia económica.
          </p>
        </div>

        <div class="pot-docs-grid">
          <!-- Doc 1 -->
          <div class="pot-doc-card">
            <div class="pot-doc-meta">
              <span class="pot-doc-year">1523</span>
              <span class="pot-doc-tag">Testamento Notarial</span>
            </div>
            <h4>El Horno de Teja de los 100.000 Maravedíes</h4>
            <p>
              El 14 de enero de 1523, el ilustre regidor cuellarano Martín López de Córdoba Hinestrosa otorga su testamento. En el inventario de bienes figura expresamente la posesión de un horno industrial en el pueblo.
            </p>
            <p class="pot-doc-quote">
              «Item declaro que tengo un orno de teja en La Lastra, el qual mando que se venda... apreciado en çien mil maravedís.»
            </p>
          </div>

          <!-- Doc 2 -->
          <div class="pot-doc-card">
            <div class="pot-doc-meta">
              <span class="pot-doc-year">1546</span>
              <span class="pot-doc-tag">Ordenanzas de Cuéllar</span>
            </div>
            <h4>La Ley 139: Control de Calidad y Exportación</h4>
            <p>
              La Comunidad de Villa y Tierra de Cuéllar aprobó un reglamento exhaustivo para supervisar las medidas, el punto de cocción y la venta de tejas y ladrillos, ratificando a Lastras como el motor fabril indispensable de todo el territorio.
            </p>
            <p class="pot-doc-quote">
              «Ley CXXXIX: De los que hazen teja e ladrillo en los términos desta Villa... que ninguno sea osado de vender teja cruda ni hendida so pena de perdimiento de la dicha teja.»
            </p>
          </div>

          <!-- Doc 3 -->
          <div class="pot-doc-card">
            <div class="pot-doc-meta">
              <span class="pot-doc-year">1499</span>
              <span class="pot-doc-tag">Privilegio Forestal</span>
            </div>
            <h4>El Combustible: Barrujo y Ramera de los Pinares</h4>
            <p>
              Para alimentar los voraces hornos morunos se requerían toneladas de combustión. Las ordenanzas concejiles de 1499 protegieron los pinares comunales pero garantizaron el derecho exclusivo de tejeros y caleros a recoger la pinocha caída (<em>barrujo</em>) y leña menuda.
            </p>
            <p class="pot-doc-quote">
              Una alianza ecológica y jurídica perfecta entre la explotación forestal del pino y la cocción al fuego de la arcilla.
            </p>
          </div>

          <!-- Doc 4 -->
          <div class="pot-doc-card">
            <div class="pot-doc-meta">
              <span class="pot-doc-year">1591–1865</span>
              <span class="pot-doc-tag">Libros Parroquiales</span>
            </div>
            <h4>La Huella en los Templos de la Comarca</h4>
            <p>
              Las cuentas de las parroquias vecinas registran compras continuadas: la iglesia de <strong>Calabazas de Fuentidueña</strong> adquirió 400 tejas lastreñas en 1591 y partidas en 1721; en <strong>Aldeasoña</strong> consta teja en 1602; y en 1865 se contrata expresamente a <strong>Luis Matarranz</strong>, «maestro tejero de Lastras de Cuéllar», para las obras de Fuentepiñel.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- =====================================================================
         5. BENTO GRID: DOS VERTES PRODUCTIVAS (TEJERÍA VS RESINA)
         ===================================================================== -->
    <section class="pot-section pot-section-soft" id="produccion">
      <div class="pot-container">
        <div class="pot-sec-header">
          <span class="pot-sec-tag">Producción Artesanal • Dos Almas del Mismo Barro</span>
          <h2 class="pot-sec-title">Tejería Pesada y Alfarería Resinera</h2>
          <p class="pot-sec-sub">
            La arcilla de Lastras no solo levantó tejados y espadañas mudéjares; fue la herramienta clave que permitió recolectar el oro líquido de los pinares.
          </p>
        </div>

        <div class="pot-bento-duo">
          <!-- Card 1: Tejería -->
          <div class="pot-bento-card">
            <div class="pot-bento-thumb">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/tejas.jpg" alt="Tejas curvas tradicionales de Lastras de Cuéllar" loading="lazy" />
              <span class="pot-bento-badge">Construcción y Arquitectura</span>
            </div>
            <div class="pot-bento-body">
              <h3>La Tejería Pesada: Barro para el Mudéjar</h3>
              <p>
                Especializada en la fabricación de <strong>teja árabe curva de canal y cobija</strong>, ladrillo macizo tosco y baldosas de barro. Su dureza y resistencia a las heladas castellanas vistieron los campanarios, caserones y soportales de toda la comarca de Cuéllar y Sepúlveda.
              </p>
              <ul class="pot-bento-list">
                <li><strong>Moldeado a mano:</strong> En gradillas de madera espolvoreadas con arena fina para evitar la adherencia.</li>
                <li><strong>Marcas de tejero:</strong> Tejas con incisiones digitales o señas gremiales familiares cocidas en el horno.</li>
                <li><strong>Durabilidad centenaria:</strong> Piezas que siguen coronando bodegas y viviendas centenarias del pueblo.</li>
              </ul>
              <a href="https://www.lastrasdecuellar.net/reportajes-especiales/la-arquitectura-popular/" class="pot-bento-link">
                <span>Descubrir la Arquitectura Popular de Lastras →</span>
              </a>
            </div>
          </div>

          <!-- Card 2: Pote Resinero y Alfarería -->
          <div class="pot-bento-card">
            <div class="pot-bento-thumb">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/pote-de-barro-resinero-tradicional.jpg" alt="Pote tradicional resinero de barro cocido de Lastras de Cuéllar" loading="lazy" />
              <span class="pot-bento-badge">Oficio Resinero y Menaje</span>
            </div>
            <div class="pot-bento-body">
              <h3>El Pote Resinero y la Vajilla Doméstica</h3>
              <p>
                Junto a los cántaros de agua, botijos y pucheros de lumbre, los alfares de Lastras produjeron por decenas de miles la pieza reina del monte: <strong>el pote resinero de barro cocido</strong>, tiesto cónico sin desagüe que recogía la miera pura del pino.
              </p>
              <ul class="pot-bento-list">
                <li><strong>Térmica perfecta:</strong> El barro mantenía fresca la resina bajo el sol canicular y no la alteraba químicamente.</li>
                <li><strong>Anclaje y peso:</strong> Su grosor y labio superior impedían que las rachas de viento derribaran el pote del tronco.</li>
                <li><strong>Abastecimiento total:</strong> Surtían a los pinares de Lastras, Cantalejo, Hontalbilla, Cuéllar y Zarzuela.</li>
              </ul>
              <a href="https://www.lastrasdecuellar.net/la-huella-resinera/" class="pot-bento-link">
                <span>Explorar el Monográfico de La Huella Resinera →</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =====================================================================
         6. CAPÍTULO III: LOS BARREROS Y EL PROCESO TRADICIONAL
         ===================================================================== -->
    <section class="pot-section" id="proceso">
      <div class="pot-container">
        <div class="pot-sec-header">
          <span class="pot-sec-tag">Capítulo III • La Materia Prima y el Trabajo Físico</span>
          <h2 class="pot-sec-title">Los Barreros y la Alquimia de los Cuatro Elementos</h2>
          <p class="pot-sec-sub">
            Al noreste de Lastras, el paraje de <em>Los Barreros</em> guardaba el secreto: una arcilla roja ferruginosa de excepcional plasticidad cuya extracción durante siglos acabó creando las características lagunas y charcas del entorno.
          </p>
        </div>

        <div class="pot-process-grid">
          <!-- Paso 1 -->
          <div class="pot-process-card">
            <span class="pot-step-number">01</span>
            <h4>Extracción Selectiva</h4>
            <p>
              A pico y pala se retiraba la "flor de tierra" superficial para alcanzar la veta pura de arcilla roja en profundidad. Las hondonadas históricas de extracción originaron las charcas y lagunas del paraje.
            </p>
          </div>

          <!-- Paso 2 -->
          <div class="pot-process-card">
            <span class="pot-step-number">02</span>
            <h4>La Inverneada</h4>
            <p>
              El barro extraído pasaba meses expuesto a la intemperie. Las heladas del invierno castellano quebraban los terrones y purificaban la masa de sales y caliches mediante la acción del hielo.
            </p>
          </div>

          <!-- Paso 3 -->
          <div class="pot-process-card">
            <span class="pot-step-number">03</span>
            <h4>Amasado a Pie Descalzo</h4>
            <p>
              Tras triturarse con mazas de madera y decantarse en pilas de agua, cuadrillas enteras pisaban la arcilla con pies descalzos durante horas hasta conseguir una pasta elástica, sedosa y uniforme.
            </p>
          </div>

          <!-- Paso 4 -->
          <div class="pot-process-card">
            <span class="pot-step-number">04</span>
            <h4>Cocción en Horno Árabe</h4>
            <p>
              En hornos morunos de doble cámara u "hormigueros", se apilaban miles de piezas. Durante días, turnos ininterrumpidos alimentaban las hogueras con <em>barrujo</em> y leña hasta alcanzar los 1000 ºC.
            </p>
          </div>
        </div>

        <!-- Horno Árabe Story Split -->
        <div class="pot-story-split" style="margin-top: 64px;">
          <div class="pot-story-media">
            <div class="pot-story-img-frame">
              <img src="https://www.lastrasdecuellar.net/wp-content/uploads/Horno-arabe1-reducida.jpg" alt="Antiguo horno moruno árabe de cocer barro en Lastras de Cuéllar" loading="lazy" />
              <div class="pot-media-caption">
                <strong>Horno Árabe Tradicional:</strong> Bóvedas de cocción donde las llamas de leña de pino transformaban el barro crudo en terracota indestructible.
              </div>
            </div>
          </div>

          <div class="pot-story-content">
            <span class="pot-sec-tag">Arquitectura del Fuego</span>
            <h3>El Rito de la Cochura: Cuando el Pueblo no Dormía</h3>
            <p>
              Cocer una hornada era el momento cumbre del año alfarero. Exigía una concentración sobrehumana: si la temperatura subía demasiado rápido, las piezas estallaban; si caía el tiro, el barro quedaba "moro" o crudo y se desmoronaba con las lluvias.
            </p>
            <p>
              Día y noche, los fogoneros lastreños se relevaban ante la boca ardiente. El humo oloroso a resina y pinocha cubría el caserío, anunciando a toda la comarca que una nueva remesa de miles de tejas y vasijas estaba a punto de nacer de las cenizas.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- =====================================================================
         7. CAPÍTULO IV: LOS ÚLTIMOS MAESTROS Y EL RESCATE DE IGNACIO SANZ
         ===================================================================== -->
    <section class="pot-section pot-section-soft" id="memoria">
      <div class="pot-container">
        <div class="pot-sec-header">
          <span class="pot-sec-tag">Capítulo IV • Memoria Viva y Etnografía</span>
          <h2 class="pot-sec-title">Los Últimos Alfareros: Nombres que Desafiaron al Olvido</h2>
          <p class="pot-sec-sub">
            Hasta mediados del siglo XX, media docena de talleres familiares mantenían vivos los tornos y las tejeras de Lastras antes de la irrupción del plástico y el fibrocemento.
          </p>
        </div>

        <div class="pot-masters-grid">
          <!-- Moscos -->
          <div class="pot-master-card">
            <span class="pot-master-role">Taller Innovador</span>
            <h4>«Los Moscos» (Carlos Avial y Valentina Callejo)</h4>
            <p>
              El alfar y tejera más emblemático del siglo XX. Pioneros al modernizar la producción e incorporar la máquina "galletera" para extruir tejas y ladrillos. Inmortalizados en la memoria popular por el sacrificio y entrega de Valentina, quien dejaba la escuela en marzo para trabajar el barro y volvía en noviembre.
            </p>
          </div>

          <!-- Cachacantos y Zamaca -->
          <div class="pot-master-card">
            <span class="pot-master-role">Maestría de Torno</span>
            <h4>Moisés «Cachacantos» y Doroteo «Zamaca»</h4>
            <p>
              Artesanos de precisión legendaria capaces de alzar en el torno cántaros y pucheros con paredes finas como cáscaras de huevo. Sus piezas abastecían las alhacenas campesinas de toda la provincia de Segovia.
            </p>
          </div>

          <!-- Pichito y Serafín -->
          <div class="pot-master-card">
            <span class="pot-master-role">Linaje Tejero</span>
            <h4>El Tío «Pichito» y la Familia del Sr. Serafín</h4>
            <p>
              Representantes del esfuerzo físico en las tejeras de verano. Cuadrillas que moldearon millones de tejas bajo el sol implacable de Castilla para reconstruir pueblos enteros tras la Guerra Civil.
            </p>
          </div>
        </div>

        <!-- Quote Box Ignacio Sanz -->
        <div class="pot-quote-box">
          <div class="pot-quote-text">
            <blockquote>
              «La alfarería concedió marchamo de singularidad a Lastras de Cuéllar. Sus cacharreros viejos, de manos curtidas en el barro y ojos avezados al fuego, custodiaron un saber medieval que dio dignidad y sustento a generaciones enteras.»
            </blockquote>
            <div class="pot-quote-author">
              Ignacio Sanz
              <span>Escritor, ceramista y cronista etnográfico de los alfares segovianos</span>
            </div>
          </div>
          <div class="pot-quote-frame">
            <img src="https://www.lastrasdecuellar.net/wp-content/uploads/IMG_5743.jpg" alt="Homenaje a los alfareros y tejeros en Lastras de Cuéllar" loading="lazy" />
          </div>
        </div>
      </div>
    </section>

    <!-- =====================================================================
         8. LLAMAMIENTO: ARCHIVO COMUNITARIO Y COLABORACIÓN
         ===================================================================== -->
    <section class="pot-cta-section" id="colaborar">
      <div class="pot-container">
        <div class="pot-cta-inner">
          <span class="pot-badge" style="background: rgba(255,255,255,0.2); color: #FFFFFF; border-color: rgba(255,255,255,0.4);">MEMORIA COLECTIVA DE LASTRAS</span>
          <h2>¿Guardas una pieza de barro, una foto o un recuerdo familiar?</h2>
          <p>
            El archivo histórico de Lastras de Cuéllar lo construimos entre todos los vecinos y familias. Si en tu casa, bodega o desván conservas un pote resinero, un cántaro antiguo, tejas con marcas de tejero o fotografías de los viejos alfares, ayúdanos a catalogarlo digitalmente.
          </p>
          <div class="pot-cta-buttons">
            <a href="https://www.lastrasdecuellar.net/colaborar-con-la-web/" class="pot-btn pot-btn-primary">
              <span>✍ Colaborar con el Archivo Digital</span>
            </a>
            <a href="https://www.lastrasdecuellar.net/la-huella-resinera/" class="pot-btn pot-btn-outline">
              <span>🌲 Ver La Huella Resinera</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>
</div>

<!-- =====================================================================
     DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)
     ===================================================================== -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://www.lastrasdecuellar.net/alfareros-y-tejeros-lastras-de-cuellar/#article",
      "isPartOf": {
        "@type": "WebPage",
        "@id": "https://www.lastrasdecuellar.net/alfareros-y-tejeros-lastras-de-cuellar/"
      },
      "headline": "Alfareros y Tejeros de Lastras de Cuéllar: Historia, Barro y Fuego",
      "description": "Historia y patrimonio de la alfarería y tejería en Lastras de Cuéllar: de los orígenes medievales y las ordenanzas de 1546 a Los Barreros, los potes resineros y los alfares de Los Moscos.",
      "image": "https://www.lastrasdecuellar.net/wp-content/uploads/historia-alfareros-tejeros-lastras-de-cuellar.jpg",
      "inLanguage": "es",
      "publisher": {
        "@type": "Organization",
        "name": "Lastras de Cuéllar",
        "url": "https://www.lastrasdecuellar.net"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.lastrasdecuellar.net/alfareros-y-tejeros-lastras-de-cuellar/#breadcrumbs",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Inicio",
          "item": "https://www.lastrasdecuellar.net/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Cultura y Tradición",
          "item": "https://www.lastrasdecuellar.net/lastras-de-cuellar/cultura-y-tradicion/"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Alfareros y Tejeros",
          "item": "https://www.lastrasdecuellar.net/alfareros-y-tejeros-lastras-de-cuellar/"
        }
      ]
    }
  ]
}
</script>
"""

def main():
    print("1. Cargando plantillas maestras de Header y Footer...")
    t_head = fetch_json(URL_HEADER)
    t_foot = fetch_json(URL_FOOTER)

    raw_head = t_head.get("meta", {}).get("_elementor_data", "[]")
    el_head = json.loads(raw_head) if isinstance(raw_head, str) else raw_head
    master_header = el_head[0]

    raw_foot = t_foot.get("meta", {}).get("_elementor_data", "[]")
    el_foot = json.loads(raw_foot) if isinstance(raw_foot, str) else raw_foot
    master_footer_container = el_foot[0]
    master_footer_styles = el_foot[1]

    print("2. Construyendo el contenedor de contenido de Alfareros...")
    html_content = generate_html_content()

    alfar_container = {
        "id": "alfar_content_container",
        "elType": "container",
        "settings": {
            "content_width": "full",
            "padding": {
                "unit": "px",
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0",
                "isLinked": True
            }
        },
        "elements": [
            {
                "id": "alfar_html_widget",
                "elType": "widget",
                "settings": {
                    "html": html_content
                },
                "elements": [],
                "widgetType": "html"
            }
        ],
        "isInner": False
    }

    print("3. Ensamblando el árbol _elementor_data de 4 nodos...")
    full_elementor_data = [
        master_header,
        alfar_container,
        master_footer_container,
        master_footer_styles
    ]

    payload = {
        "title": PAGE_TITLE,
        "slug": PAGE_SLUG,
        "status": "publish",
        "template": "elementor_canvas",
        "meta": {
            "_elementor_edit_mode": "builder",
            "_elementor_template_type": "wp-page",
            "_elementor_data": json.dumps(full_elementor_data, ensure_ascii=False),
            "_elementor_page_settings": {
                "hide_title": "yes"
            },
            "rank_math_title": "Alfareros y Tejeros de Lastras de Cuéllar | Historia, Barro y Fuego",
            "rank_math_description": "Historia y patrimonio de alfareros y tejeros en Lastras de Cuéllar: orígenes medievales, ordenanzas de 1546, Los Barreros, potes resineros y Los Moscos.",
            "rank_math_focus_keyword": "alfareros lastras de cuellar, alfareria lastras de cuellar, tejeros"
        }
    }

    print("4. Enviando payload a la API REST de WordPress...")
    status, res = post_json(URL_PAGE, payload)
    print(f"Respuesta de actualización: Código HTTP {status}")
    print(f"Página ID: {res.get('id')}")
    print(f"Slug: {res.get('slug')}")
    print(f"Enlace público: {res.get('link')}")

    # Guardar copia del estado final
    with open("backup_page_26499_published_alfareros.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Copia de seguridad del estado publicado guardada en backup_page_26499_published_alfareros.json")

if __name__ == "__main__":
    main()
