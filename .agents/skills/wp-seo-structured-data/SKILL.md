---
name: wp-seo-structured-data
description: >-
  Generación, inyección y validación de esquemas de datos estructurados Schema.org en formato JSON-LD para WordPress y Elementor: AdministrativeArea, TouristAttraction, Event, NewsArticle y BreadcrumbList para el portal de Lastras de Cuéllar.
---

# Skill: WordPress & Elementor SEO Structured Data (Schema.org / JSON-LD)

## 1. Propósito y Activación
- **Propósito**: Maximizar la visibilidad semántica, presencia en Google Rich Results (fragmentos enriquecidos), E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) y Knowledge Graph del portal municipal y divulgativo de **Lastras de Cuéllar (Segovia)** mediante la inyección y validación de esquemas de datos estructurados Schema.org en formato JSON-LD.
- **Cuándo invocar esta skill**:
  - Al crear o actualizar páginas pilar de patrimonio, historia o naturaleza (`Historia`, `Naturaleza`, `Cultura y Tradición`, `Arquitectura Popular`).
  - Al publicar o maquetar reportajes monográficos (`reportajes-especiales`) o notas de prensa en `actualidad`.
  - Al estructurar eventos festivos, culturales o deportivos (Fiestas de San Jerónimo, Santo Cristo del Humilladero, Romerías).
  - Al auditar el marcado semántico y las migas de pan (`Breadcrumbs`) de cualquier plantilla de Theme Builder de Elementor.

---

## 2. Requisitos Previos y Tools MCP
- **MCP Server**: `lastras-de-cuellar-segovia-elementor`
- **Herramientas MCP operativas**:
  - `elementor-get-page-structure`: Para inspeccionar si ya existe un widget `html` con JSON-LD inyectado.
  - `elementor-update-page-settings` / `elementor-manage-elements`: Para inyectar o actualizar el bloque con el script estructurado.
- **Herramientas locales**:
  - Script validador: `scripts/validate_schema.py` para verificar que el JSON-LD cumple con la especificación de Schema.org antes de publicarlo.

---

## 3. Esquemas Canónicos para Lastras de Cuéllar

### A. Entidad Local / Municipio (`AdministrativeArea` & `Place`)
Aplicable a la Portada Principal (`inicio`, ID 26169) y páginas corporativas:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["Place", "AdministrativeArea"],
      "@id": "https://www.lastrasdecuellar.net/#place",
      "name": "Lastras de Cuéllar",
      "description": "Municipio histórico de la comarca Tierra de Pinares en la provincia de Segovia, España. Destacado por su patrimonio arquitectónico, tradición resinera y entorno natural de lagunas y pinares.",
      "url": "https://www.lastrasdecuellar.net",
      "address": {
        "@type": "PostalAddress",
        "postalCode": "40352",
        "addressLocality": "Lastras de Cuéllar",
        "addressRegion": "Segovia",
        "addressCountry": "ES"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 41.2986,
        "longitude": -4.1136
      },
      "sameAs": [
        "https://es.wikipedia.org/wiki/Lastras_de_Cu%C3%A9llar",
        "https://www.wikidata.org/wiki/Q1948831"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.lastrasdecuellar.net/#website",
      "url": "https://www.lastrasdecuellar.net",
      "name": "Lastras de Cuéllar — Portal Web & Sistema Editorial",
      "publisher": {
        "@id": "https://www.lastrasdecuellar.net/#place"
      },
      "inLanguage": "es-ES"
    }
  ]
}
</script>
```

---

### B. Atracción Turística y Patrimonio (`TouristAttraction` / `LandmarksOrHistoricalBuildings`)
Aplicable a monumentos y espacios naturales (Iglesia de San Jerónimo, Ermita de Salcedón, Lagunas):
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TouristAttraction",
  "name": "Iglesia Parroquial de San Jerónimo",
  "description": "Templo parroquial de Lastras de Cuéllar que alberga el retablo barroco y tallas de gran valor artístico, epicentro religioso e histórico de la villa.",
  "url": "https://www.lastrasdecuellar.net/la-arquitectura-popular/",
  "touristType": ["Turismo Cultural", "Patrimonio Religioso"],
  "isAccessibleForFree": true,
  "publicAccess": true,
  "containedInPlace": {
    "@type": "Place",
    "name": "Lastras de Cuéllar",
    "address": {
      "@type": "PostalAddress",
      "postalCode": "40352",
      "addressLocality": "Lastras de Cuéllar",
      "addressRegion": "Segovia",
      "addressCountry": "ES"
    }
  }
}
</script>
```

---

### C. Artículos y Reportajes de Fondo (`Article` / `NewsArticle`)
Aplicable a la plantilla Theme Builder de artículos (`single`, ID 22328 / 5755) y monográficos de investigación:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.lastrasdecuellar.net/reportajes-especiales/resina-pinares/"
  },
  "headline": "La Memoria Viva de los Pinares y el Oficio Resinero",
  "description": "Monográfico histórico sobre la transformación económica y cultural de la resina en Lastras de Cuéllar durante los siglos XIX y XX.",
  "image": [
    "https://www.lastrasdecuellar.net/wp-content/uploads/portada-resina.webp"
  ],
  "datePublished": "2026-11-01T10:00:00+01:00",
  "dateModified": "2026-11-04T18:00:00+01:00",
  "author": {
    "@type": "Person",
    "name": "Redacción Lastras de Cuéllar",
    "url": "https://www.lastrasdecuellar.net"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Portal de Lastras de Cuéllar",
    "url": "https://www.lastrasdecuellar.net",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.lastrasdecuellar.net/wp-content/uploads/logo-lastras.webp"
    }
  },
  "inLanguage": "es-ES"
}
</script>
```

---

### D. Migas de Pan Jerárquicas (`BreadcrumbList`)
Garantiza que Google indexe la jerarquía exacta de la arquitectura de la web:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Inicio",
      "item": "https://www.lastrasdecuellar.net"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Historia",
      "item": "https://www.lastrasdecuellar.net/historia-de-lastras-de-cuellar/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Arquitectura Popular",
      "item": "https://www.lastrasdecuellar.net/la-arquitectura-popular/"
    }
  ]
}
</script>
```

---

## 4. Método de Inyección en Elementor
Para inyectar Schema JSON-LD sin romper el diseño visual ni causar problemas de maquetación:

1. Insertar un widget de tipo `html` al inicio del contenedor principal o en el pie de página de la plantilla:
```json
{
  "id": "schm101",
  "elType": "widget",
  "isInner": false,
  "widgetType": "html",
  "settings": {
    "html": "<script type=\"application/ld+json\">\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"Place\",\n  ...\n}\n</script>"
  },
  "elements": []
}
```
2. Ejecutar siempre el script validador previo:
   `python3 .agents/skills/wp-seo-structured-data/scripts/validate_schema.py <archivo_o_json>`

---

## 5. Reglas de Validación de Calidad
1. **Sin errores de sintaxis JSON**: Asegurar que todas las comillas internas estén escapadas correctamente al serializar en `_elementor_data`.
2. **URLs Canónicas**: Toda URL en `@id`, `url`, `image` debe ser absoluta (comenzando por `https://www.lastrasdecuellar.net`).
3. **No dupliques bloques redundantes**: Si una plantilla global ya incluye la entidad `WebSite` o `Organization`, las páginas individuales solo deben inyectar el esquema específico (`Article`, `TouristAttraction`, `Event`).
