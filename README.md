# Open Redirect Tester

A simple tool for penetration testers and developers to identify open redirect vulnerabilities in web applications.  
Includes both a **command-line script** and a **web application**.

---

## Features

- Tests for open redirect vulnerabilities using common parameter names.
- CLI for quick automation.
- Web interface for easy manual testing and reporting.

---

## Requirements

- Python 3.7+
- `requests` library (for both)
- `flask` library (for web version)

Install dependencies with:

```bash
pip install requests flask
```

---

## Usage

### 1. Command-Line Tool

```bash
python open_redirect_tester_cli.py "https://target.com/page"
```

### 2. Web Application

```bash
python open_redirect_tester_web.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## How it Works

- Appends common redirect parameters (e.g., `redirect`, `url`, `next`, etc.) with a test value `https://evil.com` to the target URL.
- Checks if the application returns a redirect (`Location` header) to the test URL.
- Flags possible vulnerabilities.

---

## Reporting

See `open_redirect_report.md` for a sample report template.

---

## Contributing

Pull requests are welcome! Please open issues or suggestions for improvements.

---

## License

MIT License