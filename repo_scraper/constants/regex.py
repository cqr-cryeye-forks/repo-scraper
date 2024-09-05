# Регулярные выражения для поиска URL с авторизацией
REGEX_URL = r'\b[a-zA-Z0-9-_]+://[a-zA-Z0-9-_]+:[a-zA-Z0-9-_]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+'

# Регулярные выражения для поиска паролей и ключей
REGEX_PASSWORD = r'\b(?:pass|password|SECRET_KEY)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'
REGEX_PWD = r'\b(?:pwd|pass)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'
REGEX_SECRET_KEY = r'\b(?:secret|SECRET_KEY|private_key|PRIVATE_KEY|api_key|API_KEY|access_key|ACCESS_KEY)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'
REGEX_API_KEY = r'\b(?:api_key|API_KEY|access_key|ACCESS_KEY)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'

# Регулярное выражение для поиска IP-адресов, исключая 127.0.0.1 и 0.0.0.0
REGEX_IP = r'\b(?!127\.0\.0\.1\b)(?!0\.0\.0\.0\b)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

# Регулярное выражение для поиска длинных Base64 строк
REGEX_BASE_64 = r'(?:"|\')?[A-Za-z0-9+/=]{40,}(?:"|\')?'

# Регулярные выражения для поиска файлов и их расширений
REGEX_FILE_NAME = r'["\']?(?:\.\/)?([\w.-]+)["\']?'
REGEX_EXTENSION = r'\.(\w+)$'

# Регулярное выражение для поиска GitHub репозиториев
REGEX_GIT = r'^(https:\/\/|git@)github\.com[/:][\w.-]+\/[\w.-]+\.git'

# Регулярное выражение для поиска GitHub токенов
REGEX_GIT_TOKEN = r'\bghp_[a-zA-Z0-9]{36}\b'

# Регулярное выражение для поиска SSH ключей
REGEX_SSH_KEY = r'(ssh-(rsa|ed25519|dss)|ecdsa-sha2-nistp\d{3}) [A-Za-z0-9+/=]{100,}'

# Регулярное выражение для поиска сильных паролей (8-32 символа, с цифрами и спецсимволами)
REGEX_STRONG_PASSWORD = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]).{8,32}'

# Исключение строк, которые не должны быть матчами
REGEX_EXCLUDE = r'\b(?:display_name|metadata)\b'
