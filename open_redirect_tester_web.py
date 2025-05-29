from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

REDIRECT_PARAMS = [
    "redirect", "url", "next", "return", "dest", "destination", "continue", "redir", "goto"
]
EVIL_URL = "https://evil.com"

TEMPLATE = """
<!doctype html>
<title>Open Redirect Tester</title>
<h2>Test for Open Redirect Vulnerabilities</h2>
<form method="POST">
  URL: <input name="url" style="width:350px" placeholder="https://example.com/page" required>
  <input type="submit" value="Test">
</form>
{% if results %}
  <h3>Results for {{ base_url }}</h3>
  <ul>
  {% for param, test_url, result in results %}
    <li>
      <b>{{ param }}</b>: 
      {% if result == "vulnerable" %}
        <span style="color:red">[VULNERABLE]</span> <a href="{{ test_url }}" target="_blank">{{ test_url }}</a>
      {% elif result == "error" %}
        <span style="color:gray">[ERROR]</span>
      {% else %}
        <span style="color:green">[SAFE]</span>
      {% endif %}
    </li>
  {% endfor %}
  </ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    base_url = ""
    if request.method == "POST":
        base_url = request.form["url"]
        for param in REDIRECT_PARAMS:
            if "?" in base_url:
                test_url = f"{base_url}&{param}={EVIL_URL}"
            else:
                test_url = f"{base_url}?{param}={EVIL_URL}"
            try:
                resp = requests.get(test_url, allow_redirects=False, timeout=7)
                location = resp.headers.get("Location")
                if location and EVIL_URL in location:
                    results.append((param, test_url, "vulnerable"))
                else:
                    results.append((param, test_url, "safe"))
            except Exception:
                results.append((param, test_url, "error"))
    return render_template_string(TEMPLATE, results=results, base_url=base_url)

if __name__ == "__main__":
    app.run(debug=True)