"""Deploy HTML to Surge.sh using their API."""
import sys
import os
import json
import zipfile
import tempfile
import random
import string

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

def deploy(html_path):
    workspace = os.path.dirname(os.path.abspath(html_path))

    # Read the HTML content
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Generate a random subdomain
    subdomain = 'dailylist-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    # Create a deployment package - Surge uses a specific format
    # We need to upload files to Surge's CDN

    # Actually, let's try Tiiny.host API - simpler for single HTML files
    print(f"Trying tiiny.host...")

    # Create zip for upload
    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp.close()
    zip_path = tmp.name

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(html_path, 'index.html')

    # Try tiiny.host
    try:
        with open(zip_path, 'rb') as f:
            resp = requests.post(
                "https://api.tiiny.host/v1/project",
                files={"file": ("site.zip", f, "application/zip")},
                data={"name": subdomain}
            )
        print(f"Tiiny.host status: {resp.status_code}")
        if resp.status_code in (200, 201):
            data = resp.json()
            print(f"URL: https://{subdomain}.tiiny.site")
            os.unlink(zip_path)
            return f"https://{subdomain}.tiiny.site"
        else:
            print(f"Tiiny.host error: {resp.text[:300]}")
    except Exception as e:
        print(f"Tiiny.host failed: {e}")

    os.unlink(zip_path)

    # Fallback: try Render static site deploy
    print("\nAll free deploy APIs require auth now.")
    print("Suggesting alternative: start a local server + cloud tunnel")

    return None

if __name__ == "__main__":
    html_path = sys.argv[1]
    deploy(html_path)
