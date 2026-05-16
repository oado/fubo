"""Deploy a single HTML file to Netlify as a public site (no auth required)."""
import sys
import os
import json
import zipfile
import tempfile

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

def deploy(html_path):
    # Create a temp zip with the HTML file as index.html
    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp.close()
    zip_path = tmp.name

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(html_path, 'index.html')

    # Deploy to Netlify - send zip as raw body
    url = "https://api.netlify.com/api/v1/sites"
    headers = {"Content-Type": "application/zip"}

    with open(zip_path, 'rb') as f:
        resp = requests.post(url, data=f.read(), headers=headers)

    os.unlink(zip_path)

    print(f"Status: {resp.status_code}")

    if resp.status_code in (200, 201):
        data = resp.json()
        site_url = data.get("url", "unknown")
        site_id = data.get("id", "unknown")
        site_name = data.get("name", "unknown")
        print(f"SUCCESS!")
        print(f"URL: {site_url}")
        print(f"Site ID: {site_id}")

        # Save info
        info_path = os.path.join(os.path.dirname(os.path.abspath(html_path)), "deploy_info.json")
        with open(info_path, "w") as f:
            json.dump({"url": site_url, "id": site_id, "name": site_name}, f, indent=2)
        return site_url
    else:
        print(f"Netlify failed: {resp.text[:300]}")
        return None

if __name__ == "__main__":
    html_path = sys.argv[1]
    deploy(html_path)
