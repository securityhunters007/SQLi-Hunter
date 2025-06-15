# SQLi-Hunter: A Multi-Technique SQL Injection Scanner

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

SQLi-Hunter is a powerful and automated SQL Injection (SQLi) vulnerability scanner written in Python. It is designed to help security testers and developers identify potential SQLi flaws in web applications by using a variety of detection methods. The tool can intelligently probe URL parameters and HTML forms to uncover vulnerabilities that might be missed by manual testing.

## ✨ Key Features

-   **Multi-Technique Scanning:** Employs three different methods to detect SQLi vulnerabilities, ensuring wider coverage.
-   **Comprehensive Target Analysis:** Scans both URL parameters (`GET` requests) and HTML Forms (`POST`/`GET` requests).
-   **Error-Based Detection:** Tries to break SQL queries to force the database to reveal verbose error messages.
-   **Blind SQLi Detection:**
    -   **Boolean-Based:** Asks True/False questions to the database and analyzes changes in the page content.
    -   **Time-Based:** Asks the database to wait for a specific time and measures the response delay to confirm command execution.
-   **User-Friendly Interface:** Provides clean, readable, and colorful CLI output powered by the `rich` library.
-   **Save to File:** An option to save the complete scan log to a text file for later analysis.

## 🔬 Detection Techniques Explained

SQLi-Hunter uses the following three techniques to identify vulnerabilities:

1.  **Error-Based:** This is the simplest method. The scanner injects payloads (like `'` or `"` ) that are designed to disrupt the SQL query. If the server is misconfigured and leaks database errors onto the web page, the scanner detects these error strings.

2.  **Boolean-Based Blind:** When a server has error reporting turned off, this technique is used. The scanner appends True (`AND 1=1`) and False (`AND 1=2`) conditions to the query. If the page response for the True condition is different from the False condition, it confirms a vulnerability.

3.  **Time-Based Blind:** This is the stealthiest method, used when the page content does not change at all. The scanner injects a command that tells the database to sleep for a few seconds (e.g., `SLEEP(5)`). If the server's response is delayed by that amount of time, the scanner knows the command was executed.

## 🛠️ Installation & Setup

**Prerequisites:**
-   Python 3.7+
-   `pip` and `git`

**Installation Steps:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/securityhunters007/SQLi-Hunter.git
    cd SQLi-Hunter
    ```
    *(Note: Replace `your-username` with your actual GitHub username)*

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(You will need a `requirements.txt` file containing `requests`, `rich`, and `beautifulsoup4`)*

## 🚀 Usage

You can view all available options with the help command:
```bash
python sqli_hunter.py --help
```

### Example Commands

**1. Run a full scan on a vulnerable URL:**
This command will test the URL for Error, Boolean, and Time-based SQLi.
```bash
python sqli_hunter.py --url "[http://testphp.vulnweb.com/listproducts.php?cat=1](http://testphp.vulnweb.com/listproducts.php?cat=1)"
```

**2. Scan a page containing forms (like a login or search page):**
```bash
python sqli_hunter.py --url "[http://testphp.vulnweb.com/search.php](http://testphp.vulnweb.com/search.php)"
```

**3. Run a scan and save the output to a file:**
```bash
python sqli_hunter.py --url "[http://testphp.vulnweb.com/login.php](http://testphp.vulnweb.com/login.php)" --output scan_report.txt
```

## ⚠️ Disclaimer

This tool is intended for **educational purposes and for use in authorized security testing environments only**. Running this tool against websites without explicit permission from the owner is illegal and unethical. The author is not responsible for any misuse or damage caused by this program.

## 📄 License

This project is licensed under the MIT License. 
