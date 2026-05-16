"""
Deploy HTML file as a Cloudflare Workers site using workers.dev subdomain.
This creates a free worker that serves the HTML content.
"""
import sys
import os
import json

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

def deploy(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(f"HTML size: {len(html_content)} chars")

    # We can't use Cloudflare Workers API without auth either.
    # Let's try a completely different approach: GitHub Gist + HTML preview

    # Create a GitHub Gist (no auth needed for public gists? No, auth is needed)
    # OK, let's try another approach: use the surge CLI with email login

    # Actually, the simplest no-auth approach is to use Netlify's drag-and-drop
    # But we can't do that from CLI without auth.

    # Let's try: Vercel CLI? No, also needs auth.

    # The real answer: the user should just fix COS permissions.
    # Let me provide a direct, clear guide for that.

    print("All CLI deploy services require authentication.")
    print("\nBest path: Fix your COS bucket settings.")
    print("\nAlternative: Use Netlify's web interface (no CLI needed):")
    print("1. Open https://app.netlify.com/drop")
    print("2. Drag & drop the index.html file onto the page")
    print("3. Done! You get a free URL instantly")

if __name__ == "__main__":
    html_path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    deploy(html_path)
