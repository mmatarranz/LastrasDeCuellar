---
name: wordpress-custom-code
description: >-
  Use this skill when developing custom PHP, JavaScript, or CSS for WordPress,
  creating or modifying a child theme (e.g. Hello Elementor Child), writing custom hooks/filters,
  registering Custom Post Types (CPT) or custom taxonomies, integrating ACF with Elementor,
  or writing custom shortcodes and Elementor widgets.
---

# WordPress & Elementor Custom Development

This skill governs standard development practices for custom code in WordPress projects using **Elementor Pro** and a child theme (recommended: **Hello Elementor Child**).

---

## 1. Child Theme Architecture

Always place custom code in a child theme or a custom mu-plugin/plugin, never in the parent theme or core files.

```
wp-content/themes/hello-elementor-child/
├── style.css             # Theme header definition
├── functions.php         # Entry point for hooks & includes
├── inc/                  # Modular PHP includes
│   ├── cpt.php           # Custom Post Types & Taxonomies
│   ├── acf-fields.php    # ACF configuration / JSON sync
│   └── elementor.php     # Custom Elementor hooks or tags
└── assets/
    ├── css/custom.css    # Custom styles
    └── js/custom.js      # Custom scripts
```

### Enqueueing Scripts and Styles Properly
Always use `wp_enqueue_scripts` with dependency declarations, file modification timestamps for cache-busting, and `$in_footer = true` for scripts:

```php
add_action( 'wp_enqueue_scripts', function() {
    $theme_version = wp_get_theme()->get( 'Version' );
    
    wp_enqueue_style(
        'lastras-child-style',
        get_stylesheet_directory_uri() . '/assets/css/custom.css',
        [ 'hello-elementor' ],
        filemtime( get_stylesheet_directory() . '/assets/css/custom.css' )
    );

    wp_enqueue_script(
        'lastras-child-script',
        get_stylesheet_directory_uri() . '/assets/js/custom.js',
        [ 'jquery' ],
        filemtime( get_stylesheet_directory() . '/assets/js/custom.js' ),
        true
    );
} );
```

---

## 2. Custom Post Types & Taxonomies

- Register CPTs and Taxonomies inside the `init` action hook.
- Set `'show_in_rest' => true` to enable Block Editor and modern REST API support.
- Add `'elementor'` to `'supports'` array if direct Elementor editing is needed for that CPT:

```php
add_action( 'init', function() {
    register_post_type( 'noticia', [
        'labels' => [
            'name'          => __( 'Noticias', 'lastras-de-cuellar' ),
            'singular_name' => __( 'Noticia', 'lastras-de-cuellar' ),
        ],
        'public'       => true,
        'has_archive'  => true,
        'rewrite'      => [ 'slug' => 'noticias' ],
        'show_in_rest' => true,
        'supports'     => [ 'title', 'editor', 'thumbnail', 'excerpt', 'elementor' ],
        'menu_icon'    => 'dashicons-megaphone',
    ] );
} );
```

---

## 3. ACF & Elementor Pro Integration

- Use ACF Pro field groups for structured content (dates, location, contact, gallery, custom metadata).
- Render ACF fields dynamically in Elementor templates using **Elementor Pro Dynamic Tags**:
  - Elementor Text / Heading widget → Dynamic Tag → ACF Field.
  - Elementor Image widget → Dynamic Tag → ACF Image field.
  - Elementor Gallery widget → Dynamic Tag → ACF Gallery.
- When creating loop items (Elementor Pro Loop Builder), bind every inner element to dynamic post attributes or ACF fields.

---

## 4. Security & Best Practices

1. **Input Sanitization**:
   - `sanitize_text_field( $_POST['field'] )`
   - `sanitize_textarea_field( ... )`
   - `absint( ... )` / `intval( ... )`
   - `esc_url_raw( ... )`

2. **Output Escaping**:
   - `esc_html( $var )`
   - `esc_attr( $var )`
   - `esc_url( $var )`
   - `wp_kses_post( $html )`

3. **Nonces and Permissions**:
   - Always verify nonces on form submissions or AJAX endpoints (`check_admin_referer()` / `wp_verify_nonce()`).
   - Check current user capabilities (`current_user_can( 'edit_posts' )`).

4. **Database Queries**:
   - Prefer `WP_Query` or `get_posts()` over raw SQL.
   - If raw SQL is strictly required, always use `$wpdb->prepare()`.
