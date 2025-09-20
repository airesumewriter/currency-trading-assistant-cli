from tabulate import tabulate

def print_info(message):
    print(f"[INFO] {message}")

def print_success(message):
    print(f"[SUCCESS] {message}")

def print_warning(message):
    print(f"[WARNING] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_header(message):
    print("\n" + "="*60)
    print(f" {message}")
    print("="*60 + "\n")

def print_table(headers, data):
    """Print data in a formatted table"""
    print(tabulate(data, headers=headers, tablefmt="grid"))
