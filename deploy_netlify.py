"""Deploy a zip file to Netlify (anonymous, no auth needed)."""
import sys
import json

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

zip_path = sys.argv[1] if len(sys.argv) > 1 else "deploy.zip"

url = "https://api.netlify.com/api/v1/sites"

with open(zip_path, "rb") as f:
    resp = requests.post(url, files={"file": ("deploy.zip", f, "application/zip")})

print(f"Status: {resp.status_code}")

if resp.status_code in (200, 201):
    data = resp.json()
    site_url = data.get("url", "unknown")
    site_id = data.get("id", "unknown")
    site_name = data.get("name", "unknown")
    print(f"URL: {site_url}")
    print(f"Site ID: {site_id}")
    print(f"Name: {site_name}")
    # Save info for later use
    with open("deploy_info.json", "w") as f:
        json.dump({"url": site_url, "id": site_id, "name": site_name}, f, indent=2)
else:
    print(f"Error: {resp.text[:500]}")
