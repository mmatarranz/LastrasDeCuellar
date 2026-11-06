# Directrices de Desarrollo y Tema Hijo

Guía para desarrolladores y agentes al incorporar nuevo código, estilos o componentes en **Lastras de Cuéllar**.

---

## 1. Recomendación Principal: Implementación de Tema Hijo

El informe de sistema de Elementor detectó:
```json
{
  "theme": {
    "name": "Hello Elementor",
    "version": "3.5.1",
    "is_child_theme": "No",
    "recommendation": "Si quieres modificar el código fuente de tu tema, te recomendamos utilizar un tema hijo."
  }
}
```

### Estructura Recomendada para `hello-elementor-child`
Cuando se implemente el tema hijo, la estructura debe ser:

```
wp-content/themes/hello-elementor-child/
├── style.css             # Metadatos del tema y dependencia de hello-elementor
├── functions.php         # Encolado de scripts y modularización de includes
├── inc/
│   ├── custom-post-types.php
│   ├── elementor-custom.php
│   └── hooks.php
└── assets/
    ├── css/
    │   └── custom.css
    └── js/
        └── custom.js
```

### Contenido de `style.css`
```css
/*
 Theme Name:   Hello Elementor Child - Lastras de Cuéllar
 Theme URI:    https://www.lastrasdecuellar.net/
 Description:  Tema hijo de Hello Elementor para el proyecto Lastras de Cuéllar
 Author:       Equipo Lastras de Cuéllar
 Author URI:   https://www.lastrasdecuellar.net/
 Template:     hello-elementor
 Version:      1.0.0
 Text Domain:  lastras-de-cuellar
*/
```

---

## 2. Flujo de Control de Versiones con Git

- **Repositorio**: `git@github.com:mmatarranz/LastrasDeCuellar.git`
- **Rama principal**: `main`

### Qué se versiona:
1. Plantillas exportadas de Elementor en formato JSON (`templates/elementor/`).
2. Archivos del tema hijo (`functions.php`, `style.css`, módulos PHP).
3. Documentación técnica y especificaciones de agentes (`.agents/skills/`, `docs/`, `README.md`).
4. Scripts de compilación o utilidades locales.

### Qué se excluye rigurosamente (`.gitignore`):
- Archivos de configuración con credenciales de base de datos (`wp-config.php`).
- Carpetas de medios de subida (`wp-content/uploads/`).
- Copias de seguridad de base de datos (`*.sql`, `*.sql.gz`).
- Núcleo de WordPress y plugins de terceros comerciales descargados.

---

## 3. Seguridad y Buenas Prácticas

1. **Firewall Wordfence**:
   - El sitio cuenta con **Wordfence Security 9.0.2**. Cualquier nueva llamada AJAX o endpoint REST debe usar nonces (`wp_create_nonce` / `check_ajax_referer`) para evitar bloqueos del firewall.
2. **Acceso de Administración Oculto**:
   - Con **WPS Hide Login (1.9.19)**, la URL por defecto `wp-login.php` está redirigida para mitigar ataques de fuerza bruta.
3. **Cabeceras HTTP**:
   - El plugin **HTTP Headers (1.19.6)** aplica políticas estrictas de seguridad (evitar ataques XSS, Clickjacking y Sniffing de MIME).
