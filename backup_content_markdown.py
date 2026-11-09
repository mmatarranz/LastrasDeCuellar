#!/usr/bin/env python3
"""
Sistema de Copia de Seguridad Editorial en Markdown (y JSON de Elementor)
para Lastras de Cuéllar (https://www.lastrasdecuellar.net).

Características:
- Exporta todas las Entradas (posts) y Páginas (pages) a archivos Markdown (.md)
  con Frontmatter YAML completo (ID, título, slug, fecha, modificación, estado,
  categorías legibles, etiquetas, enlace canónico, imagen destacada y modo Elementor).
- Para páginas maquetadas con Elementor, guarda además el respaldo estructural
  `_elementor_data` en `backups/markdown/elementor_json/` y extrae todos los textos
  de los widgets si el contenido estándar de WordPress está vacío.
- Sincronización incremental inteligente por defecto: consulta `orderby=modified`
  y descarga únicamente las entradas o páginas nuevas o modificadas desde la
  última ejecución (registradas en `backups/markdown/sync_manifest.json`).
- Genera un catálogo maestro en `backups/markdown/INDEX.md`.
- Sin dependencias externas (100% librería estándar de Python 3).

Uso:
  python3 backup_content_markdown.py            # Sincronización rápida (nuevas/modificadas)
  python3 backup_content_markdown.py --full     # Forzar respaldo completo de todo el sitio
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

BASE_URL = "https://www.lastrasdecuellar.net/wp-json/wp/v2"
BACKUP_ROOT = Path("backups/markdown")
POSTS_DIR = BACKUP_ROOT / "posts"
PAGES_DIR = BACKUP_ROOT / "pages"
ELEMENTOR_JSON_DIR = BACKUP_ROOT / "elementor_json"
MANIFEST_PATH = BACKUP_ROOT / "sync_manifest.json"
INDEX_PATH = BACKUP_ROOT / "INDEX.md"


def load_auth_header() -> str:
    """Obtiene la cabecera Authorization desde variable de entorno o .agents/mcp_config.json."""
    env_auth = os.environ.get("WP_AUTH_HEADER")
    if env_auth:
        val = env_auth.strip()
        if not val.lower().startswith("basic "):
            val = f"Basic {val}"
        return val

    config_path = Path(".agents/mcp_config.json")
    if not config_path.exists():
        raise FileNotFoundError(
            "No se encontró .agents/mcp_config.json ni la variable de entorno WP_AUTH_HEADER."
        )

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    servers = cfg.get("mcpServers", {})
    for server in servers.values():
        auth = server.get("headers", {}).get("Authorization")
        if auth:
            return auth
    raise KeyError("No se encontró cabecera Authorization en .agents/mcp_config.json")


class WPHTMLToMarkdown(HTMLParser):
    """Conversor ligero y limpio de HTML de WordPress/Elementor a Markdown."""

    IGNORE_TAGS = {"script", "style", "svg", "noscript", "iframe"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.ignore_depth = 0
        self.in_pre = False
        self.in_code = False
        self.list_stack = []  # 'ul' o 'ol'
        self.ol_counters = []
        self.link_stack = []  # urls
        self.blockquote_depth = 0

    def _append(self, text: str):
        if self.ignore_depth == 0 and text:
            self.out.append(text)

    def _ensure_newline(self, count: int = 1):
        if not self.out:
            return
        joined = "".join(self.out[-6:])
        trailing = len(joined) - len(joined.rstrip("\n"))
        if trailing < count:
            self.out.append("\n" * (count - trailing))

    def handle_starttag(self, tag: str, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if tag in self.IGNORE_TAGS:
            self.ignore_depth += 1
            return
        if self.ignore_depth > 0:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self._ensure_newline(2)
            self._append("#" * level + " ")
        elif tag == "p":
            self._ensure_newline(2)
            if self.blockquote_depth > 0:
                self._append("> " * self.blockquote_depth)
        elif tag == "br":
            self._append("  \n")
        elif tag == "hr":
            self._ensure_newline(2)
            self._append("---\n\n")
        elif tag in ("strong", "b"):
            self._append("**")
        elif tag in ("em", "i"):
            self._append("*")
        elif tag == "blockquote":
            self._ensure_newline(2)
            self.blockquote_depth += 1
            self._append("> " * self.blockquote_depth)
        elif tag == "ul":
            self._ensure_newline(1 if self.list_stack else 2)
            self.list_stack.append("ul")
            self.ol_counters.append(0)
        elif tag == "ol":
            self._ensure_newline(1 if self.list_stack else 2)
            self.list_stack.append("ol")
            self.ol_counters.append(0)
        elif tag == "li":
            self._ensure_newline(1)
            indent = "  " * max(0, len(self.list_stack) - 1)
            if self.list_stack and self.list_stack[-1] == "ol":
                self.ol_counters[-1] += 1
                self._append(f"{indent}{self.ol_counters[-1]}. ")
            else:
                self._append(f"{indent}- ")
        elif tag == "a":
            href = (attrs_dict.get("href") or "").strip()
            self.link_stack.append(href)
            self._append("[")
        elif tag == "img":
            src = (
                attrs_dict.get("data-lazy-src")
                or attrs_dict.get("data-src")
                or attrs_dict.get("src")
                or ""
            ).strip()
            if src and not src.startswith("data:image"):
                alt = (attrs_dict.get("alt") or "").strip().replace("\n", " ")
                self._ensure_newline(2)
                self._append(f"![{alt}]({src})\n\n")
        elif tag == "pre":
            self._ensure_newline(2)
            self.in_pre = True
            self._append("```\n")
        elif tag == "code":
            self.in_code = True
            if not self.in_pre:
                self._append("`")
        elif tag in ("div", "section", "article", "header", "footer", "figure", "figcaption", "tr"):
            self._ensure_newline(1)
        elif tag in ("td", "th"):
            self._append(" | ")

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in self.IGNORE_TAGS:
            self.ignore_depth = max(0, self.ignore_depth - 1)
            return
        if self.ignore_depth > 0:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._ensure_newline(2)
        elif tag == "p":
            self._ensure_newline(2)
        elif tag in ("strong", "b"):
            self._append("**")
        elif tag in ("em", "i"):
            self._append("*")
        elif tag == "blockquote":
            self.blockquote_depth = max(0, self.blockquote_depth - 1)
            self._ensure_newline(2)
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
                self.ol_counters.pop()
            self._ensure_newline(2)
        elif tag == "li":
            self._ensure_newline(1)
        elif tag == "a":
            href = self.link_stack.pop() if self.link_stack else ""
            if href:
                self._append(f"]({href})")
            else:
                self._append("]")
        elif tag == "pre":
            self._ensure_newline(1)
            self._append("```\n\n")
            self.in_pre = False
        elif tag == "code":
            if not self.in_pre:
                self._append("`")
            self.in_code = False
        elif tag in ("div", "section", "article", "figure", "figcaption", "table"):
            self._ensure_newline(2)

    def handle_data(self, data: str):
        if self.ignore_depth > 0:
            return
        if self.in_pre:
            self._append(data)
            return
        cleaned = re.sub(r"[ \t\r\f\v]+", " ", data)
        if "\n" in cleaned:
            cleaned = re.sub(r"\s*\n\s*", " ", cleaned)
        self._append(cleaned)

    def get_markdown(self) -> str:
        raw = "".join(self.out)
        # Limpiar espacios redundantes en marcas Markdown
        raw = re.sub(r"\*\*\s+\*\*", "", raw)
        raw = re.sub(r"\[\s*\]\([^)]*\)", "", raw)
        raw = re.sub(r"[ \t]+\n", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def html_to_markdown(html_content: str) -> str:
    if not html_content or not html_content.strip():
        return ""
    parser = WPHTMLToMarkdown()
    parser.feed(html_content)
    parser.close()
    return parser.get_markdown()


def extract_elementor_markdown(elementor_data_str: str) -> str:
    """Extrae de forma estructurada los textos e imágenes desde el árbol _elementor_data."""
    if not elementor_data_str:
        return ""
    try:
        elements = json.loads(elementor_data_str)
    except Exception:
        return ""

    blocks = []

    def walk(nodes):
        if not isinstance(nodes, list):
            return
        for node in nodes:
            if not isinstance(node, dict):
                continue
            widget_type = node.get("widgetType")
            settings = node.get("settings", {})
            if isinstance(settings, dict) and widget_type:
                if widget_type == "heading":
                    title = (settings.get("title") or "").strip()
                    size = (settings.get("header_size") or "h2").lower()
                    level = int(size[1]) if size in ("h1", "h2", "h3", "h4", "h5", "h6") else 2
                    if title:
                        clean_title = html_to_markdown(title).replace("\n", " ")
                        blocks.append(f"{'#' * level} {clean_title}")
                elif widget_type in ("text-editor", "html", "shortcode"):
                    raw_html = settings.get("editor") or settings.get("html") or settings.get("shortcode") or ""
                    md = html_to_markdown(raw_html)
                    if md:
                        blocks.append(md)
                elif widget_type in ("icon-box", "image-box"):
                    t = (settings.get("title_text") or "").strip()
                    d = (settings.get("description_text") or "").strip()
                    parts = []
                    if t:
                        parts.append(f"### {html_to_markdown(t)}")
                    if d:
                        parts.append(html_to_markdown(d))
                    if parts:
                        blocks.append("\n\n".join(parts))
                elif widget_type == "button":
                    btn_text = (settings.get("text") or "").strip()
                    link_obj = settings.get("link") or {}
                    url = link_obj.get("url", "") if isinstance(link_obj, dict) else ""
                    if btn_text:
                        blocks.append(f"- **Botón**: [{btn_text}]({url})" if url else f"- **Botón**: {btn_text}")
                elif widget_type == "image":
                    img = settings.get("image") or {}
                    url = img.get("url", "") if isinstance(img, dict) else ""
                    caption = (settings.get("caption") or "").strip()
                    if url:
                        blocks.append(f"![{caption}]({url})")
                elif widget_type in ("accordion", "toggle"):
                    tabs = settings.get("tabs") or []
                    if isinstance(tabs, list):
                        for tab in tabs:
                            if isinstance(tab, dict):
                                tt = (tab.get("tab_title") or "").strip()
                                tc = (tab.get("tab_content") or "").strip()
                                if tt or tc:
                                    blocks.append(f"### {html_to_markdown(tt)}\n\n{html_to_markdown(tc)}")

            children = node.get("elements")
            if isinstance(children, list) and children:
                walk(children)

    walk(elements)
    return "\n\n".join(b for b in blocks if b.strip())


def api_get(url: str, auth_header: str, retries: int = 3):
    headers = {
        "Authorization": auth_header,
        "User-Agent": "LastrasMarkdownBackup/1.0",
        "Accept": "application/json",
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                total_pages = int(resp.headers.get("X-WP-TotalPages", "1") or "1")
                total_items = int(resp.headers.get("X-WP-Total", "0") or "0")
                return data, total_pages, total_items
        except urllib.error.HTTPError as e:
            if e.code == 400:
                return [], 0, 0
            if attempt + 1 == retries:
                raise
            time.sleep(1.5 * (attempt + 1))
        except Exception:
            if attempt + 1 == retries:
                raise
            time.sleep(1.5 * (attempt + 1))
    return [], 0, 0


def fetch_taxonomy_map(taxonomy: str, auth_header: str) -> dict:
    """Descarga el mapa {id: nombre} para categorías o etiquetas."""
    mapping = {}
    page = 1
    while True:
        url = f"{BASE_URL}/{taxonomy}?per_page=100&page={page}"
        items, total_pages, _ = api_get(url, auth_header)
        if not items:
            break
        for item in items:
            mapping[item["id"]] = html.unescape(item.get("name", ""))
        if page >= total_pages:
            break
        page += 1
    return mapping


def yaml_escape(val: str) -> str:
    if val is None:
        return '""'
    s = str(val).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()
    return f'"{s}"'


def sanitize_filename(slug: str, post_id: int, date_str: str = "", is_post: bool = True) -> str:
    clean_slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug or f"item-{post_id}").strip("-")
    if not clean_slug:
        clean_slug = f"item-{post_id}"
    clean_slug = clean_slug[:80]
    if is_post and date_str and len(date_str) >= 10:
        date_prefix = date_str[:10]
        return f"{date_prefix}_{clean_slug}_{post_id}.md"
    return f"{clean_slug}_{post_id}.md"


def format_markdown_document(item: dict, content_type: str, cat_map: dict, tag_map: dict) -> tuple[str, str | None]:
    """Construye el archivo Markdown con Frontmatter YAML y devuelve (markdown_text, elementor_data_raw)."""
    post_id = item.get("id")
    title_obj = item.get("title") or {}
    title_raw = title_obj.get("raw") or html.unescape(title_obj.get("rendered", ""))
    slug = item.get("slug") or f"id-{post_id}"
    status = item.get("status", "publish")
    date_local = item.get("date", "")
    modified_gmt = item.get("modified_gmt", "")
    link = item.get("link", "")
    featured_media = item.get("featured_media", 0)

    meta = item.get("meta") or {}
    elementor_mode = meta.get("_elementor_edit_mode", "") if isinstance(meta, dict) else ""
    elementor_data_raw = meta.get("_elementor_data", "") if isinstance(meta, dict) else ""

    cat_ids = item.get("categories") or []
    tag_ids = item.get("tags") or []
    cat_names = [cat_map.get(cid, str(cid)) for cid in cat_ids]
    tag_names = [tag_map.get(tid, str(tid)) for tid in tag_ids]

    excerpt_obj = item.get("excerpt") or {}
    excerpt_html = excerpt_obj.get("raw") or excerpt_obj.get("rendered") or ""
    excerpt_md = html_to_markdown(excerpt_html).replace("\n", " ").strip()

    content_obj = item.get("content") or {}
    content_html = content_obj.get("rendered") or content_obj.get("raw") or ""
    body_md = html_to_markdown(content_html)

    elementor_md = ""
    if elementor_mode == "builder" and elementor_data_raw:
        elementor_md = extract_elementor_markdown(elementor_data_raw)

    # Construir Frontmatter YAML
    frontmatter = [
        "---",
        f"id: {post_id}",
        f"title: {yaml_escape(title_raw)}",
        f"slug: {yaml_escape(slug)}",
        f"type: {yaml_escape(content_type)}",
        f"status: {yaml_escape(status)}",
        f"date: {yaml_escape(date_local)}",
        f"modified_gmt: {yaml_escape(modified_gmt)}",
        f"link: {yaml_escape(link)}",
        f"featured_media_id: {featured_media}",
        f"builder: {yaml_escape('elementor' if elementor_mode == 'builder' else 'gutenberg/classic')}",
    ]
    if cat_names:
        cats_yaml = ", ".join(yaml_escape(c) for c in cat_names)
        frontmatter.append(f"categories: [{cats_yaml}]")
    if tag_names:
        tags_yaml = ", ".join(yaml_escape(t) for t in tag_names)
        frontmatter.append(f"tags: [{tags_yaml}]")
    if excerpt_md:
        frontmatter.append(f"excerpt: {yaml_escape(excerpt_md[:300])}")
    frontmatter.append("---")

    sections = ["\n".join(frontmatter), f"# {title_raw.strip()}"]

    if body_md:
        sections.append(body_md)

    if elementor_md and (not body_md or len(elementor_md) > len(body_md) * 1.2):
        sections.append("## Contenido Estructurado (Widgets Elementor)\n\n" + elementor_md)

    final_md = "\n\n".join(sections).strip() + "\n"
    return final_md, (elementor_data_raw if elementor_mode == "builder" and elementor_data_raw else None)


def sync_endpoint(
    endpoint: str,
    content_type: str,
    target_dir: Path,
    auth_header: str,
    manifest: dict,
    cat_map: dict,
    tag_map: dict,
    full_sync: bool = False,
) -> dict:
    """Sincroniza posts o pages desde la REST API de WordPress."""
    target_dir.mkdir(parents=True, exist_ok=True)
    ELEMENTOR_JSON_DIR.mkdir(parents=True, exist_ok=True)

    bucket = manifest.setdefault(endpoint, {})
    stats = {"checked": 0, "created": 0, "updated": 0, "unchanged": 0}

    page = 1
    per_page = 50
    stop_early = False

    while not stop_early:
        query = (
            f"{BASE_URL}/{endpoint}?context=edit&status=any"
            f"&orderby=modified&order=desc&per_page={per_page}&page={page}"
        )
        items, total_pages, total_items = api_get(query, auth_header)
        if not items:
            break

        if page == 1:
            print(f"📦 [{endpoint.upper()}] Total en WordPress: {total_items} ({total_pages} páginas de API)")

        for item in items:
            stats["checked"] += 1
            post_id = str(item["id"])
            modified_gmt = item.get("modified_gmt") or item.get("date_gmt") or ""
            slug = item.get("slug") or f"id-{post_id}"
            date_local = item.get("date") or ""
            title_raw = (item.get("title") or {}).get("raw") or html.unescape(
                (item.get("title") or {}).get("rendered", "")
            )

            prev = bucket.get(post_id)
            filename = sanitize_filename(slug, item["id"], date_local, is_post=(content_type == "post"))
            file_path = target_dir / filename

            if (
                not full_sync
                and prev
                and prev.get("modified_gmt") == modified_gmt
                and Path(prev.get("path", "")).exists()
            ):
                stats["unchanged"] += 1
                # Como pedimos orderby=modified&order=desc, si ya encontramos varios sin cambios
                # y el total de elementos en el manifiesto coincide con total_items, podemos parar temprano
                if stats["unchanged"] >= 5 and len(bucket) >= total_items:
                    stop_early = True
                    break
                continue

            # Si cambió el slug/nombre de archivo respecto al anterior, eliminar archivo antiguo
            if prev and prev.get("path") and Path(prev["path"]).exists() and Path(prev["path"]) != file_path:
                try:
                    Path(prev["path"]).unlink()
                except OSError:
                    pass

            md_text, elementor_raw = format_markdown_document(item, content_type, cat_map, tag_map)
            file_path.write_text(md_text, encoding="utf-8")

            elementor_backup_rel = None
            if elementor_raw:
                el_path = ELEMENTOR_JSON_DIR / f"{content_type}_{post_id}_{slug[:50]}.json"
                try:
                    parsed_el = json.loads(elementor_raw)
                    el_path.write_text(json.dumps(parsed_el, ensure_ascii=False, indent=2), encoding="utf-8")
                except Exception:
                    el_path.write_text(elementor_raw, encoding="utf-8")
                elementor_backup_rel = str(el_path)

            is_new = prev is None
            if is_new:
                stats["created"] += 1
            else:
                stats["updated"] += 1

            bucket[post_id] = {
                "id": item["id"],
                "title": title_raw.strip(),
                "slug": slug,
                "status": item.get("status", "publish"),
                "date": date_local,
                "modified_gmt": modified_gmt,
                "link": item.get("link", ""),
                "path": str(file_path),
                "elementor_json": elementor_backup_rel,
            }

        print(
            f"   ↳ Página API {page}/{total_pages} procesada "
            f"(Nuevos: {stats['created']} | Actualizados: {stats['updated']} | Sin cambios: {stats['unchanged']})"
        )

        if page >= total_pages:
            break
        page += 1

    return stats


def generate_index(manifest: dict):
    """Genera backups/markdown/INDEX.md con el inventario completo de páginas y entradas."""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    pages_dict = manifest.get("pages", {})
    posts_dict = manifest.get("posts", {})

    pages_list = sorted(pages_dict.values(), key=lambda x: x.get("title", "").lower())
    posts_list = sorted(posts_dict.values(), key=lambda x: x.get("date", ""), reverse=True)

    lines = [
        "# 📚 Archivo Maestro de Contenidos en Markdown — Lastras de Cuéllar",
        "",
        f"- **Última sincronización**: `{now_str}`",
        f"- **Total de Páginas respaldadas**: **{len(pages_list)}**",
        f"- **Total de Entradas (Posts) respaldadas**: **{len(posts_list)}**",
        "",
        "## 📄 Páginas (`backups/markdown/pages/`)",
        "",
        "| ID | Título | Estado | Última Modificación (GMT) | Archivo Markdown | JSON Elementor |",
        "|---:|---|---|---|---|---|",
    ]

    for p in pages_list:
        rel_md = os.path.relpath(p["path"], BACKUP_ROOT)
        el_col = f"[JSON]({os.path.relpath(p['elementor_json'], BACKUP_ROOT)})" if p.get("elementor_json") else "—"
        title_clean = p.get("title", "").replace("|", "\\|")
        lines.append(
            f"| `{p['id']}` | {title_clean} | `{p.get('status')}` | `{p.get('modified_gmt', '')[:16]}` | [{os.path.basename(p['path'])}]({rel_md}) | {el_col} |"
        )

    lines.extend(
        [
            "",
            "## 📰 Entradas del Blog (`backups/markdown/posts/`)",
            "",
            "| Fecha | ID | Título | Estado | Archivo Markdown |",
            "|---|---:|---|---|---|",
        ]
    )

    for post in posts_list:
        rel_md = os.path.relpath(post["path"], BACKUP_ROOT)
        title_clean = post.get("title", "").replace("|", "\\|")
        date_short = (post.get("date") or "")[:10]
        lines.append(
            f"| `{date_short}` | `{post['id']}` | {title_clean} | `{post.get('status')}` | [{os.path.basename(post['path'])}]({rel_md}) |"
        )

    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza y respalda todas las entradas y páginas de WordPress en formato Markdown (.md)."
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Fuerza la descarga y regeneración completa de todas las entradas y páginas.",
    )
    args = parser.parse_args()

    start_t = time.time()
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    auth_header = load_auth_header()

    manifest = {"last_sync_utc": None, "pages": {}, "posts": {}}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    print("🔍 Cargando taxonomías (categorías y etiquetas)...")
    cat_map = fetch_taxonomy_map("categories", auth_header)
    tag_map = fetch_taxonomy_map("tags", auth_header)
    print(f"   ✓ {len(cat_map)} categorías y {len(tag_map)} etiquetas cargadas.\n")

    page_stats = sync_endpoint(
        "pages", "page", PAGES_DIR, auth_header, manifest, cat_map, tag_map, full_sync=args.full
    )
    print()
    post_stats = sync_endpoint(
        "posts", "post", POSTS_DIR, auth_header, manifest, cat_map, tag_map, full_sync=args.full
    )

    total_changes = (
        page_stats["created"]
        + page_stats["updated"]
        + post_stats["created"]
        + post_stats["updated"]
    )
    if total_changes > 0 or args.full or not INDEX_PATH.exists() or not MANIFEST_PATH.exists():
        manifest["last_sync_utc"] = datetime.now(timezone.utc).isoformat()
        MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        generate_index(manifest)

    elapsed = time.time() - start_t
    print("\n" + "=" * 68)
    print(f"✅ BACKUP MARKDOWN COMPLETADO EN {elapsed:.1f}s")
    print(
        f"   • Páginas : {len(manifest['pages'])} en total "
        f"(+{page_stats['created']} nuevas, ~{page_stats['updated']} actualizadas)"
    )
    print(
        f"   • Entradas: {len(manifest['posts'])} en total "
        f"(+{post_stats['created']} nuevas, ~{post_stats['updated']} actualizadas)"
    )
    print(f"   • Índice  : {INDEX_PATH}")
    print("=" * 68)


if __name__ == "__main__":
    main()
