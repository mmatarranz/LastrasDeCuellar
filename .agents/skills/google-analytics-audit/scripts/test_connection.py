#!/usr/bin/env python3
"""
Script de verificación de conexión con Google Analytics 4 (GA4).
Comprueba la existencia y validez del archivo de credenciales de la Service Account,
la obtención del token OAuth2 y la conectividad con la propiedad de Lastras de Cuéllar.
"""

import sys
import os
import json
from ga4_client import GA4Client, DEFAULT_CREDENTIALS_PATHS

def main():
    print("=" * 65)
    print("🔍 VERIFICACIÓN DE CONEXIÓN CON GOOGLE ANALYTICS 4 (GA4)")
    print("=" * 65)

    client = GA4Client()

    if not client.credentials_path or not os.path.exists(client.credentials_path):
        print("\n❌ ARCHIVO DE CREDENCIALES NO ENCONTRADO")
        print("\nPara conectar con Google Analytics 4, sigue estos pasos:")
        print("1. En Google Cloud Console, crea una Service Account y genera una clave JSON.")
        print("2. En Google Analytics > Administrador > Acceso a la propiedad:")
        print("   Añade el correo de la Service Account con rol 'Lector' (Viewer).")
        print("3. Guarda el archivo JSON en:")
        print(f"   👉 {DEFAULT_CREDENTIALS_PATHS[0]}")
        print("   (o define la variable de entorno GA4_CREDENTIALS_JSON / GOOGLE_APPLICATION_CREDENTIALS)")
        print("4. Asegúrate de incluir el 'property_id' de GA4 dentro del JSON o como variable de entorno GA4_PROPERTY_ID.")
        print("\nPuedes ver un ejemplo en: .agents/ga4_credentials.example.json\n")
        sys.exit(1)

    print(f"✅ Archivo de credenciales detectado: {client.credentials_path}")

    # Validar campos mínimos del JSON
    try:
        with open(client.credentials_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            client_email = data.get("client_email")
            proj_id = data.get("project_id")
            prop_id = client.property_id
            print(f"   • Service Account Email: {client_email}")
            print(f"   • Google Cloud Project:  {proj_id}")
            print(f"   • GA4 Property ID:       {prop_id or '⚠️ NO DEFINIDO'}")

            if not client_email or not data.get("private_key"):
                print("❌ El archivo JSON no tiene la estructura de una Service Account válida (falta client_email o private_key).")
                sys.exit(1)

            if not prop_id:
                print("❌ Falta el Property ID de GA4.")
                print("   Añade \"property_id\": \"TU_ID_NUMERICO\" al archivo JSON o exporta GA4_PROPERTY_ID.")
                sys.exit(1)
    except Exception as e:
        print(f"❌ Error al parsear JSON: {e}")
        sys.exit(1)

    # Probar obtención de token OAuth2
    print("\n🔑 Solicitando token de autenticación a Google OAuth2...")
    try:
        token = client.get_access_token()
        print(f"✅ Token OAuth2 obtenido con éxito (primeros caracteres: {token[:12]}...)")
    except Exception as e:
        print(f"❌ Error en autenticación con Google: {e}")
        sys.exit(1)

    # Probar consulta mínima a la API de GA4
    print(f"\n📊 Probando consulta a Google Analytics Data API para propiedad {client.property_id}...")
    try:
        overview = client.get_overview(days=7)
        print("✅ Conexión con Google Analytics 4 exitosa y operativa.")
        print("\n📈 Muestra rápida de KPIs (últimos 7 días):")
        print(f"   • Usuarios Totales:    {overview.get('totalUsers', 0):,}")
        print(f"   • Usuarios Activos:    {overview.get('activeUsers', 0):,}")
        print(f"   • Sesiones:            {overview.get('sessions', 0):,}")
        print(f"   • Páginas Vistas:      {overview.get('screenPageViews', 0):,}")
        print(f"   • Tasa de Interacción: {float(overview.get('engagementRate', 0))*100:.2f}%")
        print("\n✨ ¡La skill está lista para ejecutar análisis completos!")
    except Exception as e:
        print(f"❌ Error al consultar la API de GA4: {e}")
        print("\n💡 Diagnóstico habitual:")
        print("1. Verifica que hayas invitado al email de la Service Account en GA4 Admin:")
        print(f"   Email: {client_email}")
        print(f"   Propiedad: {client.property_id}")
        print("2. Rol necesario: 'Lector' (Viewer) o superior.")
        print("3. Comprueba que la Google Analytics Data API esté habilitada en Google Cloud Console.")
        sys.exit(1)

if __name__ == "__main__":
    main()
