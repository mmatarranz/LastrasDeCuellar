#!/usr/bin/env python3
"""
Despliegue global del nuevo Footer 'Editorial Bento Dark' (Plantilla 26318 y páginas con footer integrado).
Cumple estrictamente con AGENTS.md:
1. Backups JSON previos antes de cualquier mutación.
2. Lectura de credenciales desde .agents/mcp_config.json.
3. Limpieza de estilos base64 heredados en nodos atómicos de Elementor v4.
4. Aplicación del diseño 'Editorial Bento Dark' (Desktop cohesivo en tarjetas Bento + Móvil compacto en grid 2x2).
5. Purga de caché LiteSpeed.
"""

import json
import os
import urllib.request
import sys

BASE_URL = "https://www.lastrasdecuellar.net"
URL_FOOTER_TPL = f"{BASE_URL}/wp-json/wp/v2/elementor_library/26318?context=edit"

# Leer credenciales desde .agents/mcp_config.json
with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
AUTH_HEADER = cfg["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]


def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": AUTH_HEADER,
            "User-Agent": "LastrasFooterDeployAgent/1.0"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def post_json(url, payload):
    data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Authorization": AUTH_HEADER,
            "Content-Type": "application/json",
            "User-Agent": "LastrasFooterDeployAgent/1.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))


SOCIAL_ROW_HTML = """<div class="footer-social-row">
  <span class="footer-social-label">Síguenos en redes</span>
  <div class="footer-social-strip">
    <a href="https://www.facebook.com/lastrasdecuellar.net" target="_blank" rel="noopener noreferrer" class="social-circle facebook" aria-label="Facebook de Lastras de Cuéllar" title="Facebook">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
    </a>
    <a href="https://www.instagram.com/lastrasdecuellar" target="_blank" rel="noopener noreferrer" class="social-circle instagram" aria-label="Instagram de Lastras de Cuéllar" title="Instagram">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
    </a>
    <a href="https://www.youtube.com/@lastrasdecuellar" target="_blank" rel="noopener noreferrer" class="social-circle youtube" aria-label="YouTube de Lastras de Cuéllar" title="YouTube">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
    </a>
  </div>
</div>"""

EDITORIAL_BENTO_FOOTER_CSS = """<style>
/* ==========================================================================
   LASTRAS DE CUÉLLAR — FOOTER "EDITORIAL BENTO DARK" (DESIGN SYSTEM 2026)
   ========================================================================== */

/* 0. CONTENEDOR PRINCIPAL DEL FOOTER + FILETE TRICOLOR EDITORIAL */
.elementor-element-45db84e0,
[data-id="45db84e0"],
footer.elementor-element-45db84e0,
.e-5b489b48-795c {
    position: relative !important;
    width: 100% !important;
    background: radial-gradient(circle at 18% 0%, #1A242B 0%, #0D1216 64%, #090D10 100%) !important;
    color: #F8FAFC !important;
    padding: 2.5rem 1.5rem 1.4rem 1.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    box-sizing: border-box !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    overflow: hidden !important;
}

.elementor-element-45db84e0::before,
[data-id="45db84e0"]::before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    height: 3px !important;
    background: linear-gradient(90deg, transparent 0%, rgba(184, 74, 40, 0.7) 24%, rgba(214, 158, 46, 0.95) 50%, rgba(23, 101, 83, 0.7) 76%, transparent 100%) !important;
    pointer-events: none !important;
    z-index: 3 !important;
}

/* CONTENEDOR INTERIOR (MAX 1240PX) */
.elementor-element-45db84e0 .elementor-element-42de61ce,
.elementor-element-42de61ce,
[data-id="42de61ce"],
.e-6f65c9a6-2b2c {
    max-width: 1240px !important;
    width: 100% !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 1.5rem !important;
    box-sizing: border-box !important;
}

/* GRILLA PRINCIPAL DE 4 BLOQUES (DESKTOP) */
.elementor-element-45db84e0 .elementor-element-12895df6,
.elementor-element-12895df6,
[data-id="12895df6"],
.e-5e7dbb08-7b27 {
    display: grid !important;
    grid-template-columns: 1.38fr 0.85fr 0.95fr 1.15fr !important;
    gap: 1.5rem !important;
    align-items: stretch !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

/* ==========================================================================
   1. COLUMNA 1: TARJETA BENTO DE IDENTIDAD (5708d5e5)
   ========================================================================== */
.elementor-element-45db84e0 .elementor-element-5708d5e5,
.elementor-element-5708d5e5,
[data-id="5708d5e5"],
.e-444b0895-33fa {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.4rem !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    gap: 0.75rem !important;
    max-width: none !important;
    width: 100% !important;
    box-sizing: border-box !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
}

/* Cabecera Escudo + Título */
.elementor-element-45db84e0 .elementor-element-48ff9119,
.elementor-element-48ff9119,
[data-id="48ff9119"],
.e-7268c606-9e75 {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    gap: 13px !important;
    margin: 0 !important;
    width: 100% !important;
}

img[data-id="3e1be382"],
.elementor-element-3e1be382,
.elementor-element-3e1be382 img,
.e-3ba99df-8212 {
    width: 44px !important;
    height: 46px !important;
    max-width: 44px !important;
    max-height: 46px !important;
    object-fit: contain !important;
    display: block !important;
    flex-shrink: 0 !important;
    padding: 5px !important;
    background: rgba(214, 158, 46, 0.12) !important;
    border: 1px solid rgba(214, 158, 46, 0.35) !important;
    border-radius: 11px !important;
    box-sizing: border-box !important;
    margin: 0 !important;
}

.elementor-element-45db84e0 .elementor-element-28f9ff02,
.elementor-element-28f9ff02,
[data-id="28f9ff02"] {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    gap: 2px !important;
}

[data-id="17a53cf2"],
.elementor-element-17a53cf2,
.elementor-element-17a53cf2 h3,
.e-6f8a3554-e96d {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    line-height: 1.15 !important;
    margin: 0 !important;
    letter-spacing: 0.01em !important;
}

[data-id="3417a0aa"],
.elementor-element-3417a0aa,
.elementor-element-3417a0aa p,
.e-26affe1e-39fe {
    font-family: 'Cinzel', serif !important;
    font-size: 0.63rem !important;
    font-weight: 700 !important;
    color: #D69E2E !important;
    letter-spacing: 0.13em !important;
    text-transform: uppercase !important;
    margin: 2px 0 0 0 !important;
    line-height: 1.2 !important;
}

/* Descripción del portal */
[data-id="2183f72e"],
.elementor-element-2183f72e,
.elementor-element-2183f72e p,
.e-41393db2-fcf6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.8rem !important;
    line-height: 1.56 !important;
    color: #CBD5E1 !important;
    margin: 0 !important;
    max-width: none !important;
}

/* Franja inferior de Redes Sociales dentro de la Tarjeta 1 */
.elementor-element-45db84e0 .elementor-element-48c8762a,
.elementor-element-48c8762a,
[data-id="48c8762a"],
.e-1566efed-8e1a {
    width: 100% !important;
    margin: 0.2rem 0 0 0 !important;
    padding-top: 0.7rem !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    display: block !important;
}

.elementor-element-footer_social_icons_svg,
[data-id="footer_social_icons_svg"] {
    width: 100% !important;
}

.footer-social-row {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    gap: 10px !important;
}

.footer-social-label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.74rem !important;
    font-weight: 500 !important;
    color: #94A3B8 !important;
}

.footer-social-strip {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px !important;
    align-items: center !important;
}

.elementor-element-45db84e0 .social-circle,
[data-id="45db84e0"] .social-circle {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 34px !important;
    height: 34px !important;
    border-radius: 10px !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(214, 158, 46, 0.32) !important;
    color: #E2E8F0 !important;
    text-decoration: none !important;
    transition: all 0.22s ease !important;
    padding: 0 !important;
}

.elementor-element-45db84e0 .social-circle svg,
[data-id="45db84e0"] .social-circle svg {
    width: 15px !important;
    height: 15px !important;
    fill: currentColor !important;
    display: block !important;
}

.elementor-element-45db84e0 .social-circle:hover,
[data-id="45db84e0"] .social-circle:hover {
    background: rgba(214, 158, 46, 0.22) !important;
    border-color: #D69E2E !important;
    color: #F6BE28 !important;
    transform: translateY(-2px) !important;
}

/* ==========================================================================
   2. COLUMNAS 2 Y 3: SECCIONES (2da1138d) Y PATRIMONIO & RUTAS (6c2fd869)
   ========================================================================== */
.elementor-element-45db84e0 .elementor-element-2da1138d,
.elementor-element-45db84e0 .elementor-element-6c2fd869,
[data-id="2da1138d"],
[data-id="6c2fd869"],
.e-b7c3d6a-c768,
.e-449d0485-7b43 {
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    justify-content: flex-start !important;
    gap: 0.2rem !important;
    padding: 0.35rem 0.25rem !important;
    margin: 0 !important;
    max-width: none !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

/* Cabeceras de Columna con Acento Corto en Oro Castellano */
[data-id="6be80c07"],
[data-id="32654282"],
[data-id="4b604c30"],
.e-309b3651-43cb,
.e-114128e3-22ef,
.e-8aa8698-ff44 {
    font-family: 'Cinzel', serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #D69E2E !important;
    margin: 0 0 0.65rem 0 !important;
    padding: 0 0 0.55rem 0 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    position: relative !important;
    display: block !important;
    width: 100% !important;
}

[data-id="6be80c07"]::after,
[data-id="32654282"]::after,
[data-id="4b604c30"]::after {
    content: "" !important;
    position: absolute !important;
    bottom: -1px !important;
    left: 0 !important;
    width: 36px !important;
    height: 2px !important;
    background: #D69E2E !important;
    border-radius: 2px !important;
}

/* Enlaces de Navegación con Chevron Editorial */
.elementor-element-45db84e0 [data-id="2da1138d"] a,
.elementor-element-45db84e0 [data-id="6c2fd869"] a,
[data-id="2da1138d"] a.e-button-base,
[data-id="6c2fd869"] a.e-button-base {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    color: #CBD5E1 !important;
    padding: 0.26rem 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    text-decoration: none !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
    transition: all 0.2s ease !important;
    width: fit-content !important;
}

.elementor-element-45db84e0 [data-id="2da1138d"] a::before,
.elementor-element-45db84e0 [data-id="6c2fd869"] a::before {
    content: "›" !important;
    color: #D69E2E !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    line-height: 1 !important;
    opacity: 0.8 !important;
    transition: transform 0.2s ease, color 0.2s ease !important;
}

.elementor-element-45db84e0 [data-id="2da1138d"] a:hover,
.elementor-element-45db84e0 [data-id="6c2fd869"] a:hover {
    color: #FFFFFF !important;
    transform: translateX(4px) !important;
}

.elementor-element-45db84e0 [data-id="2da1138d"] a:hover::before,
.elementor-element-45db84e0 [data-id="6c2fd869"] a:hover::before {
    color: #F6BE28 !important;
    opacity: 1 !important;
}

/* ==========================================================================
   3. COLUMNA 4: TARJETA BENTO DE ACCIÓN — CONTACTO & ARCHIVO (6e9e1e72)
   ========================================================================== */
.elementor-element-45db84e0 .elementor-element-6e9e1e72,
.elementor-element-6e9e1e72,
[data-id="6e9e1e72"],
.e-6befa9ea-da40 {
    background: linear-gradient(145deg, rgba(214, 158, 46, 0.07) 0%, rgba(184, 74, 40, 0.09) 100%) !important;
    border: 1px solid rgba(214, 158, 46, 0.26) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.4rem !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: stretch !important;
    gap: 0.6rem !important;
    max-width: none !important;
    width: 100% !important;
    box-sizing: border-box !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
}

[data-id="7d25aad0"],
[data-id="6de2fafa"],
.e-da834ec-bbaa,
.e-640ca470-60e8 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.81rem !important;
    color: #E2E8F0 !important;
    line-height: 1.48 !important;
    margin: 0 !important;
    padding: 0.35rem 0.6rem !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

/* Botón Principal CTA en Terracota Editorial */
.elementor-element-45db84e0 a[data-id="1c58c051"],
.elementor-element-6e9e1e72 a[data-id="1c58c051"],
a[data-id="1c58c051"].e-button-base,
.e-7e027a0f-9cfb {
    background: linear-gradient(135deg, #B84A28 0%, #9A3B1E 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 10px !important;
    padding: 0.68rem 1rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    text-align: center !important;
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    margin-top: auto !important;
    box-shadow: 0 4px 14px rgba(184, 74, 40, 0.38) !important;
    transition: all 0.25s ease !important;
    box-sizing: border-box !important;
}

.elementor-element-45db84e0 a[data-id="1c58c051"]:hover,
.elementor-element-6e9e1e72 a[data-id="1c58c051"]:hover,
a[data-id="1c58c051"].e-button-base:hover {
    background: linear-gradient(135deg, #CC542E 0%, #B84A28 100%) !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(184, 74, 40, 0.55) !important;
}

/* ==========================================================================
   4. SUB-FOOTER EN UNA SOLA BARRA HORIZONTAL (34570223)
   ========================================================================== */
.elementor-element-45db84e0 .elementor-element-34570223,
.elementor-element-34570223,
[data-id="34570223"],
.e-6442d2a3-23c9 {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    padding-top: 1.1rem !important;
    margin-top: 0 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    gap: 1rem !important;
    flex-wrap: wrap !important;
    box-sizing: border-box !important;
}

p[data-id="451c9277"],
.elementor-element-451c9277,
[data-id="451c9277"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.75rem !important;
    color: #94A3B8 !important;
    line-height: 1.5 !important;
    margin: 0 !important;
    text-align: left !important;
    width: auto !important;
    flex: 1 1 auto !important;
}

p[data-id="451c9277"] a,
[data-id="451c9277"] a {
    color: #D69E2E !important;
    font-weight: 600 !important;
    text-decoration: underline !important;
}

.elementor-element-45db84e0 .elementor-element-2c075820,
.elementor-element-2c075820,
[data-id="2c075820"],
.e-3322ea95-4077 {
    display: flex !important;
    flex-direction: row !important;
    justify-content: flex-end !important;
    align-items: center !important;
    width: auto !important;
    flex: 0 0 auto !important;
    gap: 0.2rem !important;
    margin: 0 !important;
    flex-wrap: wrap !important;
}

.elementor-element-45db84e0 [data-id="2c075820"] a,
[data-id="2c075820"] a.e-button-base {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: #CBD5E1 !important;
    padding: 0.15rem 0.2rem !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    text-decoration: none !important;
    display: inline-flex !important;
    align-items: center !important;
    transition: color 0.2s ease !important;
}

.elementor-element-45db84e0 [data-id="2c075820"] a:not(:last-child)::after {
    content: "·" !important;
    margin-left: 0.55rem !important;
    margin-right: 0.35rem !important;
    color: rgba(255, 255, 255, 0.25) !important;
    pointer-events: none !important;
}

.elementor-element-45db84e0 [data-id="2c075820"] a:hover {
    color: #D69E2E !important;
}

/* ==========================================================================
   5. RESPONSIVE TABLET (768px – 1024px)
   ========================================================================== */
@media (max-width: 1024px) and (min-width: 768px) {
    .elementor-element-45db84e0 .elementor-element-12895df6,
    [data-id="12895df6"] {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 1.25rem !important;
    }
}

/* ==========================================================================
   6. RESPONSIVE MÓVIL COMPACTO (< 768px) — GRID 2x2 ENLACES (-45% ALTURA)
   ========================================================================== */
@media (max-width: 767px) {
    .elementor-element-45db84e0,
    [data-id="45db84e0"],
    footer.elementor-element-45db84e0 {
        padding: 1.5rem 1rem 1.25rem 1rem !important;
    }

    .elementor-element-45db84e0 .elementor-element-42de61ce,
    [data-id="42de61ce"] {
        gap: 1rem !important;
    }

    /* Grid de 2 columnas en móvil:
       Fila 1: Identidad (ancho completo)
       Fila 2: Secciones (50% izq) + Patrimonio & Rutas (50% der)
       Fila 3: Contacto & Archivo (ancho completo) */
    .elementor-element-45db84e0 .elementor-element-12895df6,
    .elementor-element-12895df6,
    [data-id="12895df6"],
    .e-5e7dbb08-7b27 {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 0.85rem 0.75rem !important;
        align-items: start !important;
    }

    .elementor-element-45db84e0 .elementor-element-5708d5e5,
    [data-id="5708d5e5"] {
        grid-column: 1 / -1 !important;
        padding: 1rem 1.1rem !important;
        gap: 0.55rem !important;
    }

    .elementor-element-45db84e0 .elementor-element-2da1138d,
    [data-id="2da1138d"] {
        grid-column: 1 / 2 !important;
        padding: 0.25rem 0.15rem !important;
        margin-top: 0 !important;
        gap: 0.12rem !important;
    }

    .elementor-element-45db84e0 .elementor-element-6c2fd869,
    [data-id="6c2fd869"] {
        grid-column: 2 / 3 !important;
        padding: 0.25rem 0.15rem !important;
        margin-top: 0 !important;
        gap: 0.12rem !important;
    }

    .elementor-element-45db84e0 .elementor-element-6e9e1e72,
    [data-id="6e9e1e72"] {
        grid-column: 1 / -1 !important;
        padding: 1rem 1.1rem !important;
        gap: 0.5rem !important;
        margin-top: 0 !important;
    }

    [data-id="6be80c07"],
    [data-id="32654282"],
    [data-id="4b604c30"] {
        font-size: 0.66rem !important;
        letter-spacing: 0.08em !important;
        white-space: nowrap !important;
        margin-bottom: 0.45rem !important;
        padding-bottom: 0.4rem !important;
    }

    .elementor-element-45db84e0 [data-id="2da1138d"] a,
    .elementor-element-45db84e0 [data-id="6c2fd869"] a {
        font-size: 0.76rem !important;
        padding: 0.2rem 0 !important;
        line-height: 1.28 !important;
        align-items: flex-start !important;
    }

    [data-id="7d25aad0"],
    [data-id="6de2fafa"],
    .e-da834ec-bbaa,
    .e-640ca470-60e8 {
        font-size: 0.75rem !important;
        padding: 0.3rem 0.55rem !important;
    }

    /* Sub-footer compacto en móvil */
    .elementor-element-45db84e0 .elementor-element-34570223,
    [data-id="34570223"] {
        flex-direction: column-reverse !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        gap: 0.4rem !important;
        padding-top: 0.8rem !important;
    }

    p[data-id="451c9277"],
    [data-id="451c9277"] {
        text-align: center !important;
        font-size: 0.68rem !important;
        line-height: 1.4 !important;
    }

    .elementor-element-45db84e0 .elementor-element-2c075820,
    [data-id="2c075820"] {
        justify-content: center !important;
        width: 100% !important;
        gap: 0.1rem !important;
        margin-top: 0 !important;
    }

    .elementor-element-45db84e0 [data-id="2c075820"] a,
    [data-id="2c075820"] a.e-button-base {
        font-size: 0.72rem !important;
        padding: 0.1rem 0.15rem !important;
    }

    .elementor-element-45db84e0 [data-id="2c075820"] a:not(:last-child)::after {
        margin-left: 0.35rem !important;
        margin-right: 0.2rem !important;
    }
}
</style>"""


def clean_and_upgrade_footer_tree(node):
    """
    Limpia estilos base64 heredados e inline styles que entraban en conflicto,
    actualiza el bloque de redes sociales y corrige textos de botones/enlaces.
    """
    nid = node.get("id")

    # Eliminar atributo inline 'style' conflictivo si existe
    if "style" in node:
        del node["style"]

    # Vaciar custom_css.raw en styles locales atómicos para evitar !important antiguos
    if "styles" in node and isinstance(node["styles"], dict):
        for s_key, s_val in node["styles"].items():
            for variant in s_val.get("variants", []):
                if isinstance(variant.get("custom_css"), dict):
                    variant["custom_css"]["raw"] = ""
                elif variant.get("custom_css") is not None:
                    variant["custom_css"] = None

    # Asegurar semántica <footer> en el contenedor raíz 45db84e0
    if nid == "45db84e0":
        node.setdefault("settings", {})["html_tag"] = "footer"

    # Actualizar imagen del escudo en 3e1be382
    if nid == "3e1be382":
        node["settings"] = {
            "classes": {
                "$$type": "classes",
                "value": ["e-3ba99df-8212", "skip-lazy", "no-lazy"]
            },
            "image": {
                "$$type": "image",
                "value": {
                    "src": {
                        "$$type": "image-src",
                        "value": {
                            "url": {
                                "$$type": "url",
                                "value": "https://www.lastrasdecuellar.net/wp-content/uploads/cropped-escudo-lastras-sin-fondo.png"
                            },
                            "alt": {
                                "$$type": "string",
                                "value": "Escudo Oficial de Lastras de Cuéllar"
                            }
                        }
                    },
                    "size": {
                        "$$type": "string",
                        "value": "full"
                    }
                }
            }
        }

    # Actualizar el HTML de redes sociales con etiqueta "Síguenos en redes"
    if nid == "footer_social_icons_svg":
        node.setdefault("settings", {})["html"] = SOCIAL_ROW_HTML

    # Corregir tilde en "Fábricas de Resinas"
    if nid == "6aeb75f9":
        if "text" in node.get("settings", {}):
            node["settings"]["text"]["value"] = "Fábricas de Resinas"

    # Actualizar texto del botón de contacto a "Colaborar / Contacto →"
    if nid == "1c58c051":
        if "text" in node.get("settings", {}):
            node["settings"]["text"]["value"] = "Colaborar / Contacto \u2192"

    for child in node.get("elements", []):
        clean_and_upgrade_footer_tree(child)


def replace_footer_in_elements(elements_list, master_footer_container, master_footer_styles):
    """
    Busca '45db84e0' y 'luxury_footer_styles' en el nivel raíz o dentro del primer contenedor raíz
    y los reemplaza por las versiones maestras actualizadas.
    Retorna True si encontró y actualizó el footer.
    """
    updated = False

    # Caso 1: están en el nivel raíz de elements_list
    for idx, el in enumerate(elements_list):
        eid = el.get("id")
        if eid == "45db84e0":
            elements_list[idx] = master_footer_container
            updated = True
        elif eid == "luxury_footer_styles":
            elements_list[idx] = master_footer_styles
            updated = True

    if updated:
        # Asegurar que luxury_footer_styles esté presente
        if not any(el.get("id") == "luxury_footer_styles" for el in elements_list):
            elements_list.append(master_footer_styles)
        return True

    # Caso 2: están dentro de elements_list[0]['elements'] (como en la Portada 26169)
    if len(elements_list) > 0 and isinstance(elements_list[0].get("elements"), list):
        inner = elements_list[0]["elements"]
        for idx, el in enumerate(inner):
            eid = el.get("id")
            if eid == "45db84e0":
                inner[idx] = master_footer_container
                updated = True
            elif eid == "luxury_footer_styles":
                inner[idx] = master_footer_styles
                updated = True
        if updated and not any(el.get("id") == "luxury_footer_styles" for el in inner):
            inner.append(master_footer_styles)

    return updated


def main():
    print("==================================================================")
    print("  DESPLIEGUE FOOTER 'EDITORIAL BENTO DARK' — LASTRAS DE CUÉLLAR   ")
    print("==================================================================")

    # 1. Obtener y respaldar Plantilla 26318 (Footer Global)
    print("\n1. Obteniendo Plantilla Maestra 26318 (Footer Global)...")
    tpl_data = fetch_json(URL_FOOTER_TPL)
    backup_tpl_path = "backup_template_26318_before_editorial_bento_footer.json"
    if not os.path.exists(backup_tpl_path):
        with open(backup_tpl_path, "w", encoding="utf-8") as f:
            json.dump(tpl_data, f, ensure_ascii=False, indent=2)
        print(f"   [+] Backup guardado: {backup_tpl_path}")
    else:
        print(f"   [*] Backup original preservado: {backup_tpl_path}")

    raw_tpl = tpl_data.get("meta", {}).get("_elementor_data", "[]")
    tpl_elements = json.loads(raw_tpl) if isinstance(raw_tpl, str) else raw_tpl

    master_footer_container = tpl_elements[0]
    master_footer_styles = tpl_elements[1] if len(tpl_elements) > 1 else {
        "id": "luxury_footer_styles",
        "elType": "widget",
        "widgetType": "html",
        "settings": {"_title": "Estilos Footer Luxury", "html": ""},
        "elements": []
    }

    # 2. Limpiar y actualizar árbol del footer y su CSS
    print("2. Aplicando estructura y estilos 'Editorial Bento Dark'...")
    clean_and_upgrade_footer_tree(master_footer_container)
    master_footer_styles["settings"]["html"] = EDITORIAL_BENTO_FOOTER_CSS

    new_tpl_elements = [master_footer_container, master_footer_styles]
    code, _ = post_json(
        URL_FOOTER_TPL,
        {
            "meta": {
                "_elementor_data": json.dumps(new_tpl_elements, ensure_ascii=False),
                "_elementor_edit_mode": "builder"
            }
        }
    )
    print(f"   [+] Plantilla 26318 actualizada: HTTP {code}")

    # 3. Buscar todas las páginas que incrustan el footer (45db84e0) y sincronizarlas
    print("\n3. Escaneando páginas publicadas para sincronizar el footer incrustado...")
    pages_url = f"{BASE_URL}/wp-json/wp/v2/pages?per_page=100&context=edit"
    all_pages = fetch_json(pages_url)
    print(f"   [*] Total de páginas inspeccionadas: {len(all_pages)}")

    updated_pages = []
    for p in all_pages:
        pid = p.get("id")
        slug = p.get("slug", "")
        raw_p = p.get("meta", {}).get("_elementor_data", "")
        if not raw_p or "45db84e0" not in raw_p:
            continue

        print(f"   --> Sincronizando Página {pid} ({slug})...")
        backup_p_path = f"backup_page_{pid}_before_editorial_bento_footer.json"
        if not os.path.exists(backup_p_path):
            with open(backup_p_path, "w", encoding="utf-8") as f:
                json.dump(p, f, ensure_ascii=False, indent=2)

        p_elements = json.loads(raw_p) if isinstance(raw_p, str) else raw_p
        if replace_footer_in_elements(p_elements, master_footer_container, master_footer_styles):
            p_url = f"{BASE_URL}/wp-json/wp/v2/pages/{pid}?context=edit"
            p_code, _ = post_json(
                p_url,
                {
                    "meta": {
                        "_elementor_data": json.dumps(p_elements, ensure_ascii=False)
                    }
                }
            )
            print(f"       [+] Página {pid} ({slug}) actualizada: HTTP {p_code} (Backup: {backup_p_path})")
            updated_pages.append((pid, slug, p.get("link", f"{BASE_URL}/")))

    # 4. Purgar LiteSpeed Cache
    print("\n4. Purgando LiteSpeed Cache...")
    urls_to_purge = [f"{BASE_URL}/"] + [u for _, _, u in updated_pages if u]
    for u in urls_to_purge:
        try:
            purge_req = urllib.request.Request(
                u,
                headers={
                    "Authorization": AUTH_HEADER,
                    "User-Agent": "LastrasCacheAgent/1.0",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "X-LiteSpeed-Purge": "*"
                }
            )
            with urllib.request.urlopen(purge_req, timeout=15) as pr:
                print(f"   [+] Purga {u} -> HTTP {pr.getcode()}")
        except Exception as e:
            print(f"   [!] Aviso purga {u}: {e}")

    print("\n🎉 ¡DESPLIEGUE DEL FOOTER 'EDITORIAL BENTO DARK' COMPLETADO CON ÉXITO!")


if __name__ == "__main__":
    main()
