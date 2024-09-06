import re

# Обновленные регулярные выражения для различных уязвимостей
patterns = {
    "random_generated_password": r"'[A-Za-z0-9_]+':\s*['\"]([A-Za-z0-9@#\$%\^\&\*\(\)\-_\+=!]{8,})['\"]",
    "random_digits": r'\b\d{10,}\b',  # Набор случайных цифр (10+ цифр)
    "ssh_key": r'ssh-(rsa|dss) [A-Za-z0-9+/=]{100,}',  # SSH ключ
    "git_token": r'[A-Za-z0-9_-]{20,40}',  # Git токен длиной 20-40 символов
    "warning_message": r'WARNING:.*'  # Сообщение с предупреждением "WARNING"
}


# Основная функция для обработки данных
def process_data(data_list):
    vulnerabilities = {
        "random_generated_password": [],
        "random_digits": [],
        "ssh_key": [],
        "git_token": [],
        "warning_message": [],
        "other": []
    }

    for data in data_list:
        if "vulnerability_line" in data:
            line = data["vulnerability_line"]

            # Проверка на SSH-ключи
            if re.search(patterns["ssh_key"], line):
                data["reason"] = "SSH key detected"
                vulnerabilities["ssh_key"].append(data)
            # Проверка на Git-токен
            elif re.search(patterns["git_token"], line):
                print(line)
                try:
                    value = line.split('=')[1].strip().strip("'")
                    print(value)
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
            # Проверка на предупреждение "WARNING"
            elif re.search(patterns["warning_message"], line):
                data["reason"] = "Warning message detected: possible secret key or sensitive data"
                vulnerabilities["warning_message"].append(data)
            else:
                data["reason"] = "No specific vulnerability detected"
                vulnerabilities["other"].append(data)

    return vulnerabilities
