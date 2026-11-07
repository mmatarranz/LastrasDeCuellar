---
name: elementor-post-sync
description: >-
  Protocolo del ciclo de vida de persistencia, reconciliación de metadatos de WordPress (_elementor_edit_mode = 'builder'), regeneración de caché CSS de Elementor y rollback automático si la API falla tras mutar _elementor_data.
---

# Skill: Elementor Post-Sync & Rollback Protocol

## 1. Propósito y Activación
- **Propósito**: Ejecutar el ciclo de vida completo de persistencia, reconciliación de metadatos de WordPress y regeneración de caché CSS tras la inyección del árbol JSON en Elementor, garantizando persistencia atómica y tolerancia a fallos mediante rollback automático si la API falla.
- **Cuándo invocar esta skill**:
  - Inmediatamente después de generar o mutar el payload `_elementor_data` para un post, página, landing o plantilla (Theme Builder).
  - Al sincronizar plantillas globales (`header`, `footer`, `single`, `archive`).
  - Durante cualquier proceso de despliegue automatizado donde se requiera asegurar que el editor visual de Elementor reconozca el post como nativo y sin modo texto corrupto.

---

## 2. Requisitos Previos y Tools MCP Requeridas
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-update-page-settings`: Para actualizar configuraciones específicas del documento (layout, canvas, title, etc.).
  - `elementor-publish-document`: Para cambiar el estado a publicado si procede.
  - `elementor-clear-cache`: Para invalidar la caché de CSS generada por Elementor y forzar la recreación del archivo `uploads/elementor/css/post-{id}.css`.
  - `elementor-manage-revisions`: Para leer la última revisión estable antes del cambio y restaurarla en caso de error.
  - REST API WordPress (`/wp/v2/pages/{id}` o `/wp/v2/posts/{id}`): Para sincronización de `meta` nativos.

---

## 3. Reglas Estrictas y Restricciones Operativas

### DOs (Obligatorio)
1. **Paso 0: Snapshot Obligatorio Previo (Safety Backup)**:
   - ANTES de enviar el nuevo payload, el agente DEBE leer y almacenar en memoria o en un archivo temporal local (`backup_page_{id}_{timestamp}.json`) el contenido exacto existente de `_elementor_data` y sus metadatos asociados.
2. **Sincronización Estricta de Metadatos de Elementor en `wp_postmeta`**:
   Toda inyección DEBE actualizar atómicamente los siguientes 4 metadatos esenciales:
   - `_elementor_edit_mode`: Valor `"builder"`. (Si no se establece en `"builder"`, WordPress interpretará el contenido como texto clásico de TinyMCE/Gutenberg y no compilará los widgets).
   - `_elementor_template_type`: Asignar el tipo de plantilla exacto correspondiente:
     * `"wp-page"` para páginas estándar.
     * `"wp-post"` para entradas individuales.
     * `"header"` o `"footer"` para cabeceras y pies de Theme Builder.
     * `"single-post"`, `"archive"` o `"popup"` para templates específicos.
   - `_elementor_version`: Versión de Elementor Core activa (ej. `"3.28.0"` o la devuelta por el sistema).
   - `_elementor_pro_version`: Versión de Elementor Pro si está instalado.
3. **Invalidación Inmediata de Caché de Estilos**:
   - Tras recibir respuesta exitosa de la actualización del post, invocar inmediatamente la herramienta MCP `elementor-clear-cache`.
   - Si la herramienta `elementor-clear-cache` no estuviera disponible, ejecutar la regeneración mediante el endpoint REST o comando WP-CLI (`wp elementor flush-css`).
4. **Protocolo de Rollback Automatizado**:
   - Si la API responde con códigos de error HTTP:
     * `401 Unauthorized` / `403 Forbidden`: Error de credenciales o nonce expirado. Detener el flujo, registrar diagnóstico y NO sobreescribir archivos locales.
     * `500 Internal Server Error` / `502 Bad Gateway`: Posible fallo de memoria en PHP, timeout o json malformado.
     * Iniciar procedimiento de reversión inmediata:
       1. Reinyectar el snapshot previo (`backup_page_{id}_{timestamp}.json`).
       2. Restaurar `_elementor_edit_mode: "builder"`.
       3. Invocar `elementor-clear-cache`.
       4. Notificar el fallo exacto con stack trace o código HTTP retornado.

### DONTs (Prohibiciones Críticas)
1. **PROHIBIDO actualizar `_elementor_data` sin actualizar `_elementor_edit_mode = "builder"`**: Dejar este valor en blanco desactiva el renderizador de Elementor en el frontend, mostrando la página vacía o con shortcodes sin resolver.
2. **PROHIBIDO omitir el borrado de caché tras publicar**: Elementor almacena las reglas CSS precalculadas en disco. Si no se ejecuta `elementor-clear-cache`, los visitantes verán el diseño visual roto o con estilos de la versión anterior a pesar de que el JSON en base de datos esté actualizado.
3. **PROHIBIDO ignorar respuestas con errores parciales**: Cualquier aviso de fallo en deserialización en la respuesta de WP debe considerarse un fallo crítico que active el rollback.

---

## 4. Diagrama del Flujo de Sincronización y Recuperación

```
[Inicio de Despliegue]
       │
       ▼
[1. Snapshot de Seguridad] ──► Guardar _elementor_data actual a archivo de backup
       │
       ▼
[2. Envío de Payload] ───────► POST /wp/v2/pages/{id}
                               ├─ meta._elementor_data = JSON.stringify(elements)
                               ├─ meta._elementor_edit_mode = "builder"
                               └─ meta._elementor_template_type = "wp-page"
       │
       ├─────────────────────────────────┐
       ▼ (Éxito HTTP 200)                ▼ (Fallo HTTP 401, 403, 500, Timeout)
[3. Regenerar Caché]              [ROUTINE: ROLLBACK]
   Tool: `elementor-clear-cache`         │
       │                                 ├─ 1. Reinyectar Backup Snapshot
       ▼                                 ├─ 2. Forzar _elementor_edit_mode = "builder"
[4. Verificación Frontend]               ├─ 3. Tool: `elementor-clear-cache`
   GET preview_link / HTTP 200           └─ 4. Lanzar Excepción Detallada
       │
       ▼
[FIN: Despliegue Concluido]
```

---

## 5. Ejemplo de Flujo de Llamada y Script de Sincronización

Ejemplo representativo en Python utilizando llamadas MCP o cliente REST autorizado:

```python
import json
import requests

def sync_elementor_document(post_id, new_elements_tree, base_url, auth_headers):
    """
    Sincroniza un árbol de elementos en Elementor asegurando metadatos y caché.
    Incluye snapshot previo y rollback automático.
    """
    endpoint = f"{base_url}/wp-json/wp/v2/pages/{post_id}"
    
    # 1. Snapshot previo de seguridad
    get_res = requests.get(endpoint, headers=auth_headers)
    if get_res.status_code != 200:
        raise RuntimeError(f"Imposible crear snapshot previo: HTTP {get_res.status_code}")
    
    current_data = get_res.json()
    backup_data = {
        "_elementor_data": current_data.get("meta", {}).get("_elementor_data", "[]"),
        "_elementor_edit_mode": current_data.get("meta", {}).get("_elementor_edit_mode", "builder"),
        "_elementor_template_type": current_data.get("meta", {}).get("_elementor_template_type", "wp-page")
    }
    
    # 2. Payload con metadatos indispensables
    serialized_elements = json.dumps(new_elements_tree, ensure_ascii=False)
    payload = {
        "meta": {
            "_elementor_data": serialized_elements,
            "_elementor_edit_mode": "builder",
            "_elementor_template_type": "wp-page"
        }
    }
    
    try:
        # Envío de la mutación
        post_res = requests.post(endpoint, headers=auth_headers, json=payload, timeout=30)
        
        if post_res.status_code != 200:
            raise requests.HTTPError(f"Fallo en actualización: {post_res.status_code} - {post_res.text}")
        
        # 3. Invocación de la Tool MCP para purgado de caché CSS
        # En Antigravity MCP: elementor-clear-cache()
        flush_endpoint = f"{base_url}/wp-json/elementor/v1/flush-cache" # o Tool MCP directa
        requests.post(flush_endpoint, headers=auth_headers, timeout=10)
        
        print(f"[SUCCESS] Página {post_id} sincronizada y caché CSS regenerada exitosamente.")
        return True
        
    except Exception as exc:
        print(f"[ALERT] Error detectado durante la inyección ({exc}). Iniciando ROLLBACK...")
        # Ejecución del Rollback
        rollback_payload = {
            "meta": backup_data
        }
        rollback_res = requests.post(endpoint, headers=auth_headers, json=rollback_payload, timeout=30)
        if rollback_res.status_code == 200:
            print(f"[ROLLBACK OK] Estado original restaurado para la página {post_id}.")
        else:
            print(f"[FATAL] Falló el rollback en página {post_id}: {rollback_res.text}")
        raise exc
```

---

## 6. Criterio de Validación de Éxito
1. **Comprobación de Metadatos en Base de Datos**:
   - `get_post_meta(post_id, '_elementor_edit_mode', true) === 'builder'`.
   - `get_post_meta(post_id, '_elementor_template_type', true)` coincide con el tipo de plantilla esperado.
2. **Generación Efectiva de CSS**:
   - El archivo de caché `uploads/elementor/css/post-{id}.css` tiene un timestamp de modificación posterior al segundo de inyección del payload.
3. **Respuesta Frontend sin Errores**:
   - Código HTTP `200` en la URL pública o enlace de previsualización generado (`elementor-create-preview-link`).
   - Cero trazas de texto crudo JSON de Elementor visible en el cuerpo HTML de la página.
