#!/usr/bin/env python3
"""
CLI de Análisis y Auditoría de Google Analytics 4 para Lastras de Cuéllar.
Permite extraer métricas de tráfico, páginas más visitadas, fuentes de adquisición,
dispositivos y generar informes ejecutivos en formato Markdown o JSON.
"""

import sys
import os
import json
import argparse
from datetime import datetime
from ga4_client import GA4Client

def format_duration(seconds: float) -> str:
    secs = int(seconds)
    mins = secs // 60
    rem_secs = secs % 60
    return f"{mins}m {rem_secs:02d}s"

def get_mock_data(report_type: str, days: int = 30) -> dict:
    """Genera datos representativos de prueba para Lastras de Cuéllar (modo mock/preview)."""
    return {
        "overview": {
            "totalUsers": 3840,
            "activeUsers": 3520,
            "newUsers": 2980,
            "sessions": 5120,
            "screenPageViews": 14280,
            "averageSessionDuration": 162.4,
            "bounceRate": 0.384,
            "engagementRate": 0.616,
        },
        "top_pages": [
            {"pagePath": "/", "pageTitle": "Inicio — Lastras de Cuéllar", "screenPageViews": 5420, "activeUsers": 2180, "averageSessionDuration": 95.2, "bounceRate": 0.31, "engagementRate": 0.69},
            {"pagePath": "/el-rio-cega/", "pageTitle": "El Río Cega y sus Sendas Naturales", "screenPageViews": 2150, "activeUsers": 940, "averageSessionDuration": 210.5, "bounceRate": 0.28, "engagementRate": 0.72},
            {"pagePath": "/historia-y-patrimonio/", "pageTitle": "Historia, Iglesia de Santa María Magdalena y Esgrafiados", "screenPageViews": 1840, "activeUsers": 780, "averageSessionDuration": 185.0, "bounceRate": 0.34, "engagementRate": 0.66},
            {"pagePath": "/bodegas-de-lastras/", "pageTitle": "Las Tradicionales Bodegas Subterráneas de Lastras", "screenPageViews": 1290, "activeUsers": 610, "averageSessionDuration": 145.8, "bounceRate": 0.39, "engagementRate": 0.61},
            {"pagePath": "/noticias/fiestas-patronales-2026/", "pageTitle": "Programa Oficial Fiestas Patronales", "screenPageViews": 1120, "activeUsers": 590, "averageSessionDuration": 130.1, "bounceRate": 0.25, "engagementRate": 0.75},
            {"pagePath": "/lagunas-de-lastras-de-cuellar/", "pageTitle": "Lagunas y Humedales de Lastras", "screenPageViews": 890, "activeUsers": 430, "averageSessionDuration": 160.0, "bounceRate": 0.36, "engagementRate": 0.64},
            {"pagePath": "/la-chimenea-de-cuchifre-y-las-fabricas-de-resina/", "pageTitle": "La Chimenea de Cuchifre y la Tradición Resinera", "screenPageViews": 750, "activeUsers": 380, "averageSessionDuration": 172.4, "bounceRate": 0.35, "engagementRate": 0.65},
            {"pagePath": "/actualidad/", "pageTitle": "Noticias y Novedades del Municipio", "screenPageViews": 520, "activeUsers": 290, "averageSessionDuration": 88.0, "bounceRate": 0.42, "engagementRate": 0.58},
        ],
        "channels": [
            {"sessionDefaultChannelGroup": "Organic Search", "sessions": 2940, "activeUsers": 2150, "engagementRate": 0.68},
            {"sessionDefaultChannelGroup": "Direct", "sessions": 1280, "activeUsers": 820, "engagementRate": 0.59},
            {"sessionDefaultChannelGroup": "Organic Social", "sessions": 590, "activeUsers": 410, "engagementRate": 0.52},
            {"sessionDefaultChannelGroup": "Referral", "sessions": 310, "activeUsers": 210, "engagementRate": 0.64},
        ],
        "devices": [
            {"deviceCategory": "mobile", "sessions": 3480, "activeUsers": 2420},
            {"deviceCategory": "desktop", "sessions": 1490, "activeUsers": 990},
            {"deviceCategory": "tablet", "sessions": 150, "activeUsers": 110},
        ],
        "geo": [
            {"city": "Madrid", "region": "Community of Madrid", "sessions": 2120, "activeUsers": 1450},
            {"city": "Segovia", "region": "Castile and León", "sessions": 1180, "activeUsers": 780},
            {"city": "Valladolid", "region": "Castile and León", "sessions": 640, "activeUsers": 430},
            {"city": "Cuéllar", "region": "Castile and León", "sessions": 420, "activeUsers": 290},
            {"city": "Barcelona", "region": "Catalonia", "sessions": 210, "activeUsers": 140},
        ],
        "realtime": {
            "totalActiveUsers": 14,
            "screens": [
                {"unifiedScreenName": "Inicio — Lastras de Cuéllar", "activeUsers": 6},
                {"unifiedScreenName": "El Río Cega y sus Sendas Naturales", "activeUsers": 4},
                {"unifiedScreenName": "Las Tradicionales Bodegas Subterráneas", "activeUsers": 2},
                {"unifiedScreenName": "Programa Oficial Fiestas Patronales", "activeUsers": 2},
            ]
        }
    }

def print_table(headers, rows):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(val)))

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    hdr_line = "| " + " | ".join(h.ljust(col_widths[idx]) for idx, h in enumerate(headers)) + " |"

    print(sep)
    print(hdr_line)
    print(sep)
    for row in rows:
        print("| " + " | ".join(str(val).ljust(col_widths[idx]) for idx, val in enumerate(row)) + " |")
    print(sep)

def build_markdown_report(data: dict, days: int, is_mock: bool = False) -> str:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mock_banner = "> ⚠️ **Nota:** Informe generado con datos simulados (Modo Mock). Conecta credenciales en `.agents/ga4_credentials.json` para datos en tiempo real.\n\n" if is_mock else ""

    overview = data.get("overview", {})
    top_pages = data.get("top_pages", [])
    channels = data.get("channels", [])
    devices = data.get("devices", [])
    geo = data.get("geo", [])

    total_sessions = overview.get("sessions", 1) or 1
    total_users = overview.get("totalUsers", 0)
    page_views = overview.get("screenPageViews", 0)
    eng_rate = float(overview.get("engagementRate", 0)) * 100
    avg_duration = format_duration(float(overview.get("averageSessionDuration", 0)))
    bounce_rate = float(overview.get("bounceRate", 0)) * 100

    md = f"""# 📊 Informe de Analítica Web — Lastras de Cuéllar
*Generado:* {now_str} | *Periodo analizado:* Últimos {days} días  
*URL Web:* [https://www.lastrasdecuellar.net](https://www.lastrasdecuellar.net)

{mock_banner}---

## 1. KPIs Globales de Tráfico

| Métrica | Valor | Descripción / Impacto |
| :--- | :--- | :--- |
| **Usuarios Totales** | **{total_users:,}** | Audiencia alcanzada en el periodo |
| **Usuarios Activos** | **{overview.get('activeUsers', 0):,}** | Visitantes con interacción real |
| **Sesiones Totales** | **{total_sessions:,}** | Visitas completas al portal |
| **Páginas Vistas** | **{page_views:,}** | Volumen total de consumo de contenidos |
| **Tasa de Interacción** | **{eng_rate:.1f}%** | Porcentaje de sesiones no rebotadas |
| **Tasa de Rebote** | **{bounce_rate:.1f}%** | Sesiones sin interacción de más de 10s |
| **Duración Media Sesión** | **{avg_duration}** | Tiempo de permanencia por visitante |

---

## 2. Contenidos y Páginas Más Populares

| Página | Vistas | Usuarios | Duración Media | Tasa Interacción |
| :--- | :--- | :--- | :--- | :--- |
"""
    for p in top_pages:
        p_views = p.get("screenPageViews", 0)
        p_users = p.get("activeUsers", 0)
        p_dur = format_duration(float(p.get("averageSessionDuration", 0)))
        p_eng = float(p.get("engagementRate", 0)) * 100
        path = p.get("pagePath", "")
        title = p.get("pageTitle", path)
        md += f"| [`{path}`]({path}) <br> *{title}* | {p_views:,} | {p_users:,} | {p_dur} | {p_eng:.1f}% |\n"

    md += """
---

## 3. Canales de Adquisición de Tráfico

| Canal de Tráfico | Sesiones | % del Total | Usuarios | Interacción |
| :--- | :--- | :--- | :--- | :--- |
"""
    for ch in channels:
        ch_name = ch.get("sessionDefaultChannelGroup", "Otros")
        ch_sess = ch.get("sessions", 0)
        ch_pct = (ch_sess / total_sessions) * 100
        ch_users = ch.get("activeUsers", 0)
        ch_eng = float(ch.get("engagementRate", 0)) * 100
        md += f"| **{ch_name}** | {ch_sess:,} | {ch_pct:.1f}% | {ch_users:,} | {ch_eng:.1f}% |\n"

    md += """
---

## 4. Dispositivos y Audiencia Geográfica

### Desglose por Dispositivo
"""
    for dev in devices:
        d_name = dev.get("deviceCategory", "Unknown").capitalize()
        d_sess = dev.get("sessions", 0)
        d_pct = (d_sess / total_sessions) * 100
        md += f"- **{d_name}**: {d_sess:,} sesiones ({d_pct:.1f}%)\n"

    md += "\n### Principales Ciudades / Regiones de Origen\n\n| Ciudad | Región | Sesiones | Usuarios |\n| :--- | :--- | :--- | :--- |\n"
    for g in geo:
        c = g.get("city", "Desconocida")
        r = g.get("region", "")
        s = g.get("sessions", 0)
        u = g.get("activeUsers", 0)
        md += f"| {c} | {r} | {s:,} | {u:,} |\n"

    md += """
---

## 5. Recomendaciones Estratégicas para Elementor & SEO

1. **Diseño Mobile-First Prioritario**:
   - Si el tráfico móvil supera el 65%, cualquier rediseño de Elementor debe verificarse en resoluciones de 375px a 414px con la skill `elementor-responsive-breakpoints`.
2. **Potenciación de Rutas de Naturaleza y Patrimonio**:
   - Las páginas de alto tráfico como `/el-rio-cega/` o bodegas deben incluir enlaces internos cruzados (Bento Cards) hacia comercios locales, historia y agenda cultural.
3. **Core Web Vitals en Páginas Críticas**:
   - Monitorear el LCP y eliminar bloqueos de renderizado en las páginas principales mediante `elementor-performance-cwv`.
"""
    return md

def main():
    parser = argparse.ArgumentParser(description="Auditoría de analítica web con Google Analytics 4 para Lastras de Cuéllar")
    parser.add_argument("--type", choices=["overview", "top-pages", "channels", "devices", "realtime", "full-audit"], default="overview", help="Tipo de consulta")
    parser.add_argument("--days", type=int, default=30, help="Rango de días para el análisis (por defecto: 30)")
    parser.add_argument("--limit", type=int, default=15, help="Límite de registros para listas (top-pages, etc.)")
    parser.add_argument("--output", type=str, help="Ruta de archivo para guardar el informe (.md o .json)")
    parser.add_argument("--mock", action="store_true", help="Usa datos de demostración si las credenciales aún no están conectadas")
    parser.add_argument("--credentials", type=str, help="Ruta manual al archivo JSON de Service Account")
    parser.add_argument("--property-id", type=str, help="Property ID numérico de GA4")

    args = parser.parse_args()

    client = GA4Client(credentials_path=args.credentials, property_id=args.property_id)
    use_mock = args.mock

    if not client.is_configured() and not use_mock:
        print("[!] No se detectó configuración de credenciales de Google Analytics 4.")
        print("[!] Ejecutando en MODO DEMOSTRACIÓN (--mock) con datos simulados de Lastras de Cuéllar.")
        print("[!] Para conectar datos reales, crea .agents/ga4_credentials.json (ver .agents/ga4_credentials.example.json).")
        print("-" * 65)
        use_mock = True

    try:
        if use_mock:
            mock_data = get_mock_data(args.type, args.days)

            if args.type == "overview":
                data = mock_data["overview"]
                print(f"\n📊 RESUMEN GENERAL GA4 (ÚLTIMOS {args.days} DÍAS) [MODO MOCK]")
                headers = ["Métrica", "Valor"]
                rows = [
                    ["Usuarios Totales", f"{data['totalUsers']:,}"],
                    ["Usuarios Activos", f"{data['activeUsers']:,}"],
                    ["Sesiones", f"{data['sessions']:,}"],
                    ["Páginas Vistas", f"{data['screenPageViews']:,}"],
                    ["Duración Media Sesión", format_duration(data['averageSessionDuration'])],
                    ["Tasa de Rebote", f"{data['bounceRate']*100:.1f}%"],
                    ["Tasa de Interacción", f"{data['engagementRate']*100:.1f}%"],
                ]
                print_table(headers, rows)

            elif args.type == "top-pages":
                pages = mock_data["top_pages"][:args.limit]
                print(f"\n📄 PÁGINAS MÁS VISITADAS (ÚLTIMOS {args.days} DÍAS) [MODO MOCK]")
                headers = ["URL", "Vistas", "Usuarios", "Duración Media", "Interacción"]
                rows = [
                    [p["pagePath"], f"{p['screenPageViews']:,}", f"{p['activeUsers']:,}", format_duration(p["averageSessionDuration"]), f"{p['engagementRate']*100:.1f}%"]
                    for p in pages
                ]
                print_table(headers, rows)

            elif args.type == "channels":
                ch = mock_data["channels"]
                print(f"\n🌐 CANALES DE ADQUISICIÓN (ÚLTIMOS {args.days} DÍAS) [MODO MOCK]")
                headers = ["Canal", "Sesiones", "Usuarios", "Tasa Interacción"]
                rows = [
                    [c["sessionDefaultChannelGroup"], f"{c['sessions']:,}", f"{c['activeUsers']:,}", f"{c['engagementRate']*100:.1f}%"]
                    for c in ch
                ]
                print_table(headers, rows)

            elif args.type == "devices":
                dev = mock_data["devices"]
                print(f"\n📱 DESGLOSE POR DISPOSITIVO [MODO MOCK]")
                headers = ["Dispositivo", "Sesiones", "Usuarios"]
                rows = [[d["deviceCategory"].capitalize(), f"{d['sessions']:,}", f"{d['activeUsers']:,}"] for d in dev]
                print_table(headers, rows)

            elif args.type == "realtime":
                rt = mock_data["realtime"]
                print(f"\n⚡ ACTIVIDAD EN TIEMPO REAL (ÚLTIMOS 30 MIN) [MODO MOCK]")
                print(f"👥 Usuarios activos ahora mismo: {rt['totalActiveUsers']}")
                headers = ["Pantalla / Página", "Usuarios Activos"]
                rows = [[s["unifiedScreenName"], s["activeUsers"]] for s in rt["screens"]]
                print_table(headers, rows)

            elif args.type == "full-audit":
                print(f"\n📋 GENERANDO AUDITORÍA COMPLETA GA4...")
                md_content = build_markdown_report(mock_data, args.days, is_mock=True)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    print(f"✅ Auditoría completa guardada en: {args.output}")
                else:
                    print(md_content)

        else:
            # Modo Live con API de Google Analytics
            if args.type == "overview":
                data = client.get_overview(days=args.days)
                print(f"\n📊 RESUMEN GENERAL GA4 (ÚLTIMOS {args.days} DÍAS) — Propiedad {client.property_id}")
                headers = ["Métrica", "Valor"]
                rows = [
                    ["Usuarios Totales", f"{data.get('totalUsers', 0):,}"],
                    ["Usuarios Activos", f"{data.get('activeUsers', 0):,}"],
                    ["Sesiones", f"{data.get('sessions', 0):,}"],
                    ["Páginas Vistas", f"{data.get('screenPageViews', 0):,}"],
                    ["Duración Media Sesión", format_duration(float(data.get('averageSessionDuration', 0)))],
                    ["Tasa de Rebote", f"{float(data.get('bounceRate', 0))*100:.1f}%"],
                    ["Tasa de Interacción", f"{float(data.get('engagementRate', 0))*100:.1f}%"],
                ]
                print_table(headers, rows)

            elif args.type == "top-pages":
                pages = client.get_top_pages(days=args.days, limit=args.limit)
                print(f"\n📄 PÁGINAS MÁS VISITADAS (ÚLTIMOS {args.days} DÍAS)")
                headers = ["URL", "Vistas", "Usuarios", "Duración Media", "Interacción"]
                rows = [
                    [p.get("pagePath", ""), f"{p.get('screenPageViews', 0):,}", f"{p.get('activeUsers', 0):,}", format_duration(float(p.get("averageSessionDuration", 0))), f"{float(p.get('engagementRate', 0))*100:.1f}%"]
                    for p in pages
                ]
                print_table(headers, rows)

            elif args.type == "channels":
                ch = client.get_traffic_channels(days=args.days)
                print(f"\n🌐 CANALES DE ADQUISICIÓN (ÚLTIMOS {args.days} DÍAS)")
                headers = ["Canal", "Sesiones", "Usuarios", "Tasa Interacción"]
                rows = [
                    [c.get("sessionDefaultChannelGroup", ""), f"{c.get('sessions', 0):,}", f"{c.get('activeUsers', 0):,}", f"{float(c.get('engagementRate', 0))*100:.1f}%"]
                    for c in ch
                ]
                print_table(headers, rows)

            elif args.type == "devices":
                dg = client.get_devices_and_geo(days=args.days)
                print(f"\n📱 DESGLOSE POR DISPOSITIVO")
                headers = ["Dispositivo", "Sesiones", "Usuarios"]
                rows = [[d.get("deviceCategory", "").capitalize(), f"{d.get('sessions', 0):,}", f"{d.get('activeUsers', 0):,}"] for d in dg.get("devices", [])]
                print_table(headers, rows)

                print(f"\n📍 PRINCIPALES CIUDADES")
                geo_headers = ["Ciudad", "Región", "Sesiones"]
                geo_rows = [[g.get("city", ""), g.get("region", ""), f"{g.get('sessions', 0):,}"] for g in dg.get("geo", [])]
                print_table(geo_headers, geo_rows)

            elif args.type == "realtime":
                rt = client.get_realtime()
                print(f"\n⚡ ACTIVIDAD EN TIEMPO REAL (ÚLTIMOS 30 MIN)")
                print(f"👥 Usuarios activos ahora mismo: {rt.get('totalActiveUsers', 0)}")
                headers = ["Pantalla / Página", "Usuarios Activos"]
                rows = [[s.get("unifiedScreenName", ""), s.get("activeUsers", 0)] for s in rt.get("screens", [])]
                print_table(headers, rows)

            elif args.type == "full-audit":
                print(f"\n📋 EXTRACIENDO DATOS EN VIVO DE GOOGLE ANALYTICS 4...")
                overview = client.get_overview(days=args.days)
                top_pages = client.get_top_pages(days=args.days, limit=args.limit)
                channels = client.get_traffic_channels(days=args.days)
                dev_geo = client.get_devices_and_geo(days=args.days)

                aggregated = {
                    "overview": overview,
                    "top_pages": top_pages,
                    "channels": channels,
                    "devices": dev_geo.get("devices", []),
                    "geo": dev_geo.get("geo", []),
                }

                md_content = build_markdown_report(aggregated, args.days, is_mock=False)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    print(f"✅ Auditoría completa guardada en: {args.output}")
                else:
                    print(md_content)

    except Exception as e:
        print(f"\n❌ ERROR AL EJECUTAR EL REPORTE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
