import datetime
import re

patterns = {
    "random_generated_password": r"'[A-Za-z0-9_]+':\s*['\"]([A-Za-z0-9@#\$%\^\&\*\(\)\-_\+=!]{8,})['\"]",
    "random_digits": r'\b\d{10,}\b',
    "ssh_key": r'ssh-(rsa|dss) [A-Za-z0-9+/=]{100,}',
    "git_token": r'[A-Za-z0-9_-]{20,40}',
}


def generate_password_variants(keywords):
    current_year = datetime.datetime.now().year
    numbers = ["123", "456", "789", "000", "111", "1234", "12345", ]
    variants = []

    for keyword in keywords:
        variants.append(keyword)
        for num in numbers:
            variants.append(f"{keyword}{num}")
            variants.append(f"{num}{keyword}")
        variants.append(f"{keyword}{current_year}")
        variants.append(f"{current_year}{keyword}")
        variants.append(f"{keyword}{str(current_year)[-2:]}")
        variants.append(f"{str(current_year)[-2:]}{keyword}")

    return variants


def check_password_in_line(line, password_variants):
    for variant in password_variants:
        if variant in line:
            return variant
    return False


def process_data(data_list):
    vulnerabilities = []

    keywords = ["password", "admin", "secret", "my_key", "test", "qwerty"]
    password_variants = generate_password_variants(keywords)

    for data in data_list:
        if "vulnerability_line" in data:
            line = data["vulnerability_line"]

            if re.search(patterns["ssh_key"], line):
                data["reason"] = "SSH key detected"
                vulnerabilities.append(data)

            elif re.search(patterns["git_token"], line):
                try:
                    value = line.split('=')[1].strip().strip("'")
                    if value.startswith('ghp_'):
                        data["reason"] = "Git token detected: starts with 'ghp_'"
                        vulnerabilities.append(data)
                    else:
                        raise IndexError
                except IndexError:
                    if split_assignment(line):
                        data["reason"] = "Detected a randomly generated password"
                        vulnerabilities.append(data)

            elif re.search(patterns["random_generated_password"], line):
                if split_assignment(line):
                    data["reason"] = "Detected a randomly generated password"
                    vulnerabilities.append(data)

            elif re.search(patterns["random_digits"], line):
                if split_assignment(line):
                    data["reason"] = "Detected a sequence of random digits (potential sensitive data)"
                    vulnerabilities.append(data)

            elif variant := check_password_in_line(line, password_variants):
                if split_assignment(line):
                    data["reason"] = f"Detected a password variant: {variant}"
                    vulnerabilities.append(data)

    return vulnerabilities


def split_assignment(line):
    if ':' in line:
        key_value = line.split(':', 1)
        if key_value[0].endswith("http") or key_value[0].endswith("https"):
            return None
        elif " " in key_value[0] or "." in key_value[0]:
            return None
        elif " " in key_value[1]:
            key_value = key_value[1].split(" ", 1)
            if " " in key_value[1] and len(key_value[1]) >= 8:
                return None
            elif "cve" in key_value[1].lower():
                return None
            elif is_date_format(key_value[1].split("'")[1]):
                return None
    elif '=' in line:
        key_value = line.split('=', 1)
        if key_value[0].endswith("href"):
            return None
        elif " " in key_value[0] or "." in key_value[0]:
            return None
        elif " " in key_value[1]:
            key_value = key_value[1].split(" ", 1)
            if " " in key_value[1] and len(key_value[1]) >= 8:
                return None
            elif "cve" in key_value[1].lower():
                return None
            elif is_date_format(key_value[1].split("'")[1]):
                return None
    else:
        return None

    return True

def is_date_format(key):
    date_formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%d.%m.%Y",
        "%H:%M:%S",
        "%H:%M",
        "%Y%m%d",
        "%d %b %Y",
        "%d %B %Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %b %Y %H:%M:%S",
        "%d %B %Y %H:%M:%S",
        "%A, %d %B %Y",
        "%a, %d %b %Y %H:%M:%S",
        "%I:%M %p",
        "%I:%M:%S %p",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y.%m.%d %H:%M:%S",
    ]

    for fmt in date_formats:
        try:
            datetime.datetime.strptime(key, fmt)
            return True
        except ValueError:
            continue

    return False
