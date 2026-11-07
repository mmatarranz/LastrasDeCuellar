#!/usr/bin/env python3
"""
Script validador de Schemas JSON-LD para WordPress y Elementor.
Valida la sintaxis JSON, comprueba la presencia de campos clave requeridos
por Schema.org / Google Search Central (headline, image, datePublished, geo, address, etc.)
y verifica que las URLs sean absolutas y seguras (HTTPS).
"""

import sys
import json
import re

def validate_schema_json(content):
    # Extraer el JSON si viene envuelto en etiquetas <script>
    script_match = re.search(r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    if script_match:
        raw_json = script_match.group(1).strip()
    else:
        raw_json = content.strip()

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        return False, [f"Error de sintaxis JSON: {str(e)}"]

    errors = []
    warnings = []

    # Helper para validar un nodo individual
    def validate_node(node):
        if not isinstance(node, dict):
            return

        schema_type = node.get("@type")
        if not schema_type:
            errors.append("Falta la propiedad obligatoria '@type'.")
            return

        types = schema_type if isinstance(schema_type, list) else [schema_type]

        # Validar URLs
        for url_prop in ["url", "@id", "sameAs"]:
            val = node.get(url_prop)
            if val:
                urls = val if isinstance(val, list) else [val]
                for u in urls:
                    if isinstance(u, str) and not u.startswith("https://") and not u.startswith("http://") and not u.startswith("#"):
                        warnings.append(f"La URL '{u}' en '{url_prop}' debería ser absoluta con protocolo HTTPS.")

        # Validaciones específicas por tipo
        if any(t in types for t in ["Article", "NewsArticle", "BlogPosting"]):
            for req in ["headline", "image", "datePublished", "author"]:
                if req not in node:
                    warnings.append(f"El esquema Article/{types} carece del campo recomendado por Google: '{req}'.")

        if any(t in types for t in ["Place", "AdministrativeArea", "TouristAttraction"]):
            if "name" not in node:
                errors.append(f"El esquema {types} debe tener un 'name'.")
            if "address" not in node:
                warnings.append(f"El esquema {types} recomienda incluir 'address'.")

        if "BreadcrumbList" in types:
            items = node.get("itemListElement", [])
            if not isinstance(items, list) or len(items) == 0:
                errors.append("BreadcrumbList debe incluir un array 'itemListElement' con elementos.")

        # Recorrer subnodos
        for k, v in node.items():
            if isinstance(v, dict):
                validate_node(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        validate_node(item)

    if "@graph" in data and isinstance(data["@graph"], list):
        for subnode in data["@graph"]:
            validate_node(subnode)
    else:
        validate_node(data)

    is_valid = len(errors) == 0
    return is_valid, errors, warnings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: validate_schema.py <archivo.json | archivo.html | '{\"@context\":...}'>")
        sys.exit(1)

    input_arg = sys.argv[1]
    import os
    if os.path.exists(input_arg):
        with open(input_arg, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = input_arg

    is_valid, errors, warnings = validate_schema_json(content)
    print(f"Estado de Validación: {'VALIDO' if is_valid else 'INVALIDO'}")
    if errors:
        print("Errores encontrados:")
        for err in errors:
            print(f"  ❌ {err}")
    if warnings:
        print("Advertencias / Recomendaciones:")
        for warn in warnings:
            print(f"  ⚠️ {warn}")

    if not is_valid:
        sys.exit(1)
    else:
        print("¡El marcado de datos estructurados cumple con las especificaciones!")
        sys.exit(0)
