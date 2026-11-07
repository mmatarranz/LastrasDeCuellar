import json
import re
import urllib.request

# 1. Load backup
backup_file = "backup_page_5459_before_images_height_fix.json"
with open(backup_file, "r", encoding="utf-8") as f:
    page_data = json.load(f)

el_data = json.loads(page_data["meta"]["_elementor_data"])

# Find historia_styles_widget
styles_widget = None
for el in el_data:
    if el.get("id") == "historia_main_con":
        for child in el.get("elements", []):
            if child.get("id") == "historia_inner_con":
                for sub in child.get("elements", []):
                    if sub.get("id") == "historia_styles_widget":
                        styles_widget = sub
                        break

if not styles_widget:
    raise ValueError("Could not find historia_styles_widget!")

css = styles_widget["settings"]["html"]

# Old CSS block:
old_figure_block = """.historia-figure {
  margin: 0;
  background: #F8FAFC;
  border: 1px solid var(--hist-border);
  border-radius: var(--hist-radius-md);
  overflow: hidden;
}
.historia-figure img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  display: block;
}"""

if old_figure_block not in css:
    raise ValueError("Target old_figure_block not found in css!")

new_figure_block = """.historia-figure {
  margin: 0;
  background: #FFFFFF;
  border: 1px solid var(--hist-border);
  border-radius: var(--hist-radius-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: var(--hist-shadow);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.historia-figure:hover {
  transform: translateY(-2px);
  box-shadow: var(--hist-shadow-hover);
}
.historia-figure img {
  width: 100%;
  height: 520px;
  object-fit: contain;
  background: #F8FAFC;
  display: block;
  transition: transform 0.3s ease;
}
.historia-figure:hover img {
  transform: scale(1.015);
}"""

# Also ensure figcaption has margin-top: auto
old_figcaption_css = """.historia-figure figcaption {
  font-size: 0.84rem;
  color: #64748B;
  padding: 0.9rem 1.1rem;
  line-height: 1.45;
}"""

new_figcaption_css = """.historia-figure figcaption {
  font-size: 0.84rem;
  color: #64748B;
  padding: 0.9rem 1.1rem;
  line-height: 1.45;
  background: #FFFFFF;
  border-top: 1px solid var(--hist-border);
  margin-top: auto;
}"""

# Replace base figure
css = css.replace(old_figure_block, new_figure_block)
if old_figcaption_css in css:
    css = css.replace(old_figcaption_css, new_figcaption_css)

# Update mobile media query:
old_mobile_grid = """.historia-images-grid {
    grid-template-columns: 1fr;
  }"""

new_mobile_grid = """.historia-images-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
  .historia-figure img {
    height: 420px;
  }"""

if old_mobile_grid in css:
    css = css.replace(old_mobile_grid, new_mobile_grid)
    print("Mobile media query updated successfully.")
else:
    print("Warning: old_mobile_grid not found, checking alternatives...")

styles_widget["settings"]["html"] = css
print("CSS updated successfully in styles_widget.")

with open(".agents/mcp_config.json", "r", encoding="utf-8") as f:
    mcp_config = json.load(f)
auth_header = mcp_config["mcpServers"]["lastras-de-cuellar-segovia-elementor"]["headers"]["Authorization"]

def deploy():
    url = "https://www.lastrasdecuellar.net/wp-json/wp/v2/pages/5459"
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "meta": {
            "_elementor_data": json.dumps(el_data, ensure_ascii=False)
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        print(f"Update response code: {resp.status}")
        resp_json = json.loads(resp.read().decode("utf-8"))
        print("Page updated successfully! Title:", resp_json.get("title", {}).get("rendered"))

    # Also purge LiteSpeed cache for the page
    purge_url = "https://www.lastrasdecuellar.net/lastras-de-cuellar/historia-de-lastras-de-cuellar/"
    purge_req = urllib.request.Request(
        purge_url,
        headers={
            "User-Agent": "LastrasAntigravityCacheAgent/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-LiteSpeed-Purge": purge_url,
            "Authorization": auth_header
        }
    )
    try:
        with urllib.request.urlopen(purge_req) as p_resp:
            print("LiteSpeed purge status code:", p_resp.status)
            print("LiteSpeed purge cache header:", p_resp.headers.get("X-LiteSpeed-Cache", "None"))
    except Exception as e:
        print("Note on LiteSpeed purge:", e)

if __name__ == "__main__":
    import sys
    if "--deploy" in sys.argv:
        print("Deploying changes to WordPress...")
        deploy()
    else:
        print("Dry run completed. Run with --deploy to apply.")
