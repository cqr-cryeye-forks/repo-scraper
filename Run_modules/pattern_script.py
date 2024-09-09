import datetime
import re

# Обновленные регулярные выражения для различных уязвимостей
patterns = {
    "random_generated_password": r"'[A-Za-z0-9_]+':\s*['\"]([A-Za-z0-9@#\$%\^\&\*\(\)\-_\+=!]{8,})['\"]",
    "random_digits": r'\b\d{10,}\b',  # Набор случайных цифр (8+ цифр)
    "ssh_key": r'ssh-(rsa|dss) [A-Za-z0-9+/=]{100,}',  # SSH ключ
    "git_token": r'[A-Za-z0-9_-]{20,40}',  # Git токен длиной 20-40 символов
}


def generate_password_variants(keywords):
    current_year = datetime.datetime.now().year
    numbers = ["123", "456", "789", "000", "111", "1234", "12345", ]
    variants = []

    for keyword in keywords:
        variants.append(keyword)  # Оригинальный пароль
        for num in numbers:
            variants.append(f"{keyword}{num}")  # Добавляем цифры к концу
            variants.append(f"{num}{keyword}")  # Добавляем цифры к началу
        # Добавляем год и текущий год
        variants.append(f"{keyword}{current_year}")
        variants.append(f"{current_year}{keyword}")
        # Пробуем разные комбинации с годовыми цифрами
        variants.append(f"{keyword}{str(current_year)[-2:]}")  # Последние две цифры года
        variants.append(f"{str(current_year)[-2:]}{keyword}")

    return variants


def check_password_in_line(line, password_variants):
    for variant in password_variants:
        if variant in line:
            return variant
    return False


# Основная функция для обработки данных
def process_data(data_list):
    vulnerabilities = {
        "random_generated_password": [],
        "random_digits": [],
        "ssh_key": [],
        "git_token": [],
        "other": [],
        "password_detected": [],
    }

    # Пример использования
    keywords = ["password", "admin", "secret", "my_key", "test", "qwerty"]
    password_variants = generate_password_variants(keywords)

    for data in data_list:
        if "vulnerability_line" in data:
            line = data["vulnerability_line"]

            # Проверка на SSH-ключи
            if re.search(patterns["ssh_key"], line):
                data["reason"] = "SSH key detected"
                vulnerabilities["ssh_key"].append(data)
            # Проверка на Git-токен
            elif re.search(patterns["git_token"], line):
                try:
                    value = line.split('=')[1].strip().strip("'")
                    if value.startswith('ghp_'):
                        data["reason"] = "Git token detected: starts with 'ghp_'"
                        vulnerabilities["git_token"].append(data)
                    else:
                        raise IndexError
                except IndexError:
                    data["reason"] = "Detected a randomly generated password"
                    vulnerabilities["random_generated_password"].append(data)
            # Проверка на случайно сгенерированный пароль
            elif re.search(patterns["random_generated_password"], line):
                data["reason"] = "Detected a randomly generated password"
                vulnerabilities["random_generated_password"].append(data)
            # Проверка на набор случайных цифр
            elif re.search(patterns["random_digits"], line):
                data["reason"] = "Detected a sequence of random digits (potential sensitive data)"
                vulnerabilities["random_digits"].append(data)
            elif variant := check_password_in_line(line, password_variants):
                data["reason"] = f"Detected a password variant: {variant}"
                vulnerabilities["password_detected"].append(data)
            else:
                data["reason"] = "No specific vulnerability detected"
                vulnerabilities["other"].append(data)

    return vulnerabilities
