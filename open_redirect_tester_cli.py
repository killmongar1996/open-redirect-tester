import requests
import sys
from urllib.parse import urlparse, urljoin

# List of common redirect parameter names
REDIRECT_PARAMS = [
    "redirect", "url", "next", "return", "dest", "destination", "continue", "redir", "goto"
]

# Test redirect target
EVIL_URL = "https://evil.com"

def test_open_redirect(base_url):
    for param in REDIRECT_PARAMS:
        # Add the parameter to the URL
        if "?" in base_url:
            test_url = f"{base_url}&{param}={EVIL_URL}"
        else:
            test_url = f"{base_url}?{param}={EVIL_URL}"
        try:
            # Don't follow redirects automatically
            resp = requests.get(test_url, allow_redirects=False, timeout=7)
            location = resp.headers.get("Location")
            if location and EVIL_URL in location:
                print(f"[VULNERABLE] Possible open redirect with parameter '{param}': {test_url}")
            else:
                print(f"[SAFE] Parameter '{param}' did not trigger a redirect.")
        except Exception as e:
            print(f"[ERROR] Could not test {test_url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python open_redirect_tester_cli.py <URL>")
        sys.exit(1)
    test_open_redirect(sys.argv[1])