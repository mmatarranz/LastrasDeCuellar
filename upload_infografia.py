#!/usr/bin/env python3
import json
import urllib.request
import os

img_path = '/Users/miguelangelmatarranz/.gemini/antigravity/brain/62c85e4b-ac81-46b8-889c-fe32f3b2a22a/.user_uploaded/media_1794165422430_7c7b0af6.jpg'
with open('.agents/mcp_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
auth_header = cfg['mcpServers']['lastras-de-cuellar-segovia-elementor']['headers']['Authorization']

url = 'https://www.lastrasdecuellar.net/wp-json/wp/v2/media'
with open(img_path, 'rb') as f:
    img_data = f.read()

filename = 'historia-alfareros-tejeros-lastras-de-cuellar.jpg'
headers = {
    'Authorization': auth_header,
    'Content-Type': 'image/jpeg',
    'Content-Disposition': f'attachment; filename="{filename}"'
}

req = urllib.request.Request(url, data=img_data, headers=headers, method='POST')
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print('Upload Success!')
        print('Media ID:', res.get('id'))
        print('Source URL:', res.get('source_url'))
        with open('uploaded_infografia.json', 'w') as out:
            json.dump(res, out, indent=2)
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code, e.read().decode('utf-8'))
except Exception as e:
    print('Error:', e)
