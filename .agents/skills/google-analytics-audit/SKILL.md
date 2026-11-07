---
name: google-analytics-audit
description: >-
  Conexión, consulta y auditoría de métricas de tráfico y comportamiento web con Google Analytics 4 (GA4) Data API para Lastras de Cuéllar: páginas más visitadas, canales de adquisición, desglose por dispositivo, audiencias geográficas y correlación con estrategias SEO y Elementor.
---

# Google Analytics 4 (GA4) Web Analytics & Audit Suite

Esta skill proporciona herramientas, flujos automatizados e instrucciones operativas para conectar el entorno de trabajo y los agentes de IA con **Google Analytics 4 (GA4)** mediante la **Google Analytics Data API (v1beta)**. Su objetivo es auditar el rendimiento del portal de **Lastras de Cuéllar** (`https://www.lastrasdecuellar.net`), monitorizar el impacto de rediseños en Elementor y priorizar mejoras de contenido y SEO técnico.

---

## 1. Arquitectura y Métricas Clave para Lastras de Cuéllar

El portal municipal y comarcal de Lastras de Cuéllar combina turismo rural, historia/patrimonio, servicios locales y noticias. El análisis analítico debe segmentarse en tres vertientes:

1. **Páginas de Atracción Turística y Patrimonio**:
   - Rutas naturales (`/el-rio-cega/`, `/lagunas-de-lastras-de-cuellar/`).
   - Patrimonio histórico (`/historia-y-patrimonio/`, `/bodegas-de-lastras/`, `/la-chimenea-de-cuchifre-y-las-fabricas-de-resina/`).
   - Métrica clave: *Duración media de sesión (>2 min)* y *Tasa de interacción (>65%)*.

2. **Actualidad y Eventos Municipales**:
   - Fiestas patronales, bandos, cultura y comunicados (`/actualidad/`, `/noticias/...`).
   - Métrica clave: *Picos de sesiones y nuevos usuarios por canal social y directo*.

3. **Experiencia de Usuario en Dispositivos Móviles (Mobile-First)**:
   - Más del 60-70% del tráfico procede de terminales móviles (excursionistas, vecinos y visitantes).
   - Métrica clave: *Tasa de rebote en móviles vs desktop*. Una tasa de rebote elevada en móvil indica posibles problemas de LCP, CLS o maquetación responsiva.

---

## 2. Configuración de Credenciales y Seguridad

> [!CRITICAL]
> **Regla de Seguridad**: Nunca expongas ni subas a repositorios Git públicos las claves privadas de Google Cloud (`.agents/ga4_credentials.json`). Este archivo está registrado obligatoriamente en `.gitignore`.

### Pasos para conectar la API de GA4:

1. **Google Cloud Console**:
   - Crear o seleccionar un proyecto en GCP.
   - Habilitar la **Google Analytics Data API v1beta**.
   - Ir a **IAM y administración > Cuentas de servicio**, crear una Service Account (ej. `lastras-analytics-sa@...iam.gserviceaccount.com`).
   - Generar una clave en formato **JSON** y descargarla.

2. **Google Analytics 4 (Admin)**:
   - Ir a [Google Analytics](https://analytics.google.com/) > **Administrar**.
   - En **Acceso y gestión de la propiedad**, hacer clic en **+** y añadir el correo de la Service Account.
   - Asignar el rol **Lector (Viewer)**.
   - Copiar el **ID de la propiedad** (un número de 9 o 10 dígitos, ej. `428192841`).

3. **Ubicación del archivo de credenciales en el proyecto**:
   - Guardar el archivo descargado como:
     ```
     .agents/ga4_credentials.json
     ```
   - Añadir la propiedad `"property_id": "TU_ID_NUMERICO"` dentro del JSON o exportar la variable de entorno:
     ```bash
     export GA4_PROPERTY_ID="TU_ID_NUMERICO"
     ```

---

## 3. Scripts Ejecutables de la Skill

Los scripts se encuentran en `.agents/skills/google-analytics-audit/scripts/`:

### A. Diagnóstico y Comprobación de Conexión
```bash
python3 .agents/skills/google-analytics-audit/scripts/test_connection.py
```
- Valida la sintaxis del JSON y la clave privada RSA.
- Solicita un token OAuth2 a los servidores de Google.
- Ejecuta una consulta de prueba a la propiedad de GA4 y muestra un resumen de los últimos 7 días.

### B. Extracción de Métricas y Generación de Informes (`run_report.py`)

#### 1. Resumen General (Overview)
```bash
# Últimos 30 días (por defecto)
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --type overview

# Últimos 90 días
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --type overview --days 90
```

#### 2. Páginas y Artículos Más Populares
```bash
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --type top-pages --limit 20
```

#### 3. Canales de Adquisición (SEO Orgánico, Directo, Redes Sociales)
```bash
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --type channels
```

#### 4. Dispositivos y Origen Geográfico
```bash
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --type devices
```

#### 5. Usuarios en Tiempo Real
```bash
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --type realtime
```

#### 6. Auditoría Completa y Exportación en Markdown
```bash
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --type full-audit --days 30 --output scratch/informe_analitica_ga4.md
```

#### 7. Modo Demostración / Mock
Si aún no se han configurado las claves de Google Cloud, añade el flag `--mock` para generar una muestra estructurada completa basada en el catálogo real de URLs de Lastras:
```bash
python3 .agents/skills/google-analytics-audit/scripts/run_report.py --mock --type full-audit
```

---

## 4. Sinergia con Elementor y Rank Math SEO

| Señal Analítica en GA4 | Causa Probable | Acción con Skills de Antigravity |
| :--- | :--- | :--- |
| **Alto tráfico en página con baja interacción (<45%)** | Contenido poco accesible, maquetación densa o enlaces rotos. | Rediseñar con `elementor-json-builder` en formato Bento Grid y optimizar jerarquía de encabezados con `elementor-seo-semantic`. |
| **Tasa de rebote móvil significativamente superior a desktop** | Desbordamiento horizontal o fuentes diminutas. | Auditar en 375px con `elementor-responsive-breakpoints` y pasar `elementor-visual-qa-audit`. |
| **Página con alto LCP y tiempo de carga > 3s en GA4** | Imágenes sin optimizar o CSS no depurado. | Aplicar `elementor-performance-cwv` e invalidar caché LiteSpeed con `litespeed-cache-control`. |
| **Artículos de patrimonio con baja adquisición orgánica** | Falta de marcado semántico o palabras clave. | Enriquecer Schema JSON-LD con `wp-seo-structured-data` y optimizar metadatos con `rank-math-seo-pro`. |

---

## 5. Checklist para el Agente tras una Auditoría Web

- [ ] ¿Se identificaron las 5 páginas con mayor volumen de visitas?
- [ ] ¿Se verificó que los rediseños recientes de Elementor mantienen o mejoran la tasa de interacción?
- [ ] ¿Se detectó si el porcentaje de visitas móviles supera el 60% para priorizar la experiencia móvil?
- [ ] ¿Se cruzaron las páginas de mayor tráfico con la auditoría de Core Web Vitals?
- [ ] ¿Se guardó el informe de conclusiones en formato Markdown para consulta del usuario?
