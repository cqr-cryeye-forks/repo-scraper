REGEX_URL = r'\b[a-zA-Z0-9-_]+://[a-zA-Z0-9-_]+:[a-zA-Z0-9-_]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+'

REGEX_PASSWORD = r'\b(?:pass|password|SECRET_KEY)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'
REGEX_PWD = r'\b(?:pwd|pass)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'
REGEX_SECRET_KEY = r'\b(?:secret|SECRET_KEY|private_key|PRIVATE_KEY|api_key|API_KEY|access_key|ACCESS_KEY)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'
REGEX_API_KEY = r'\b(?:api_key|API_KEY|access_key|ACCESS_KEY)\b\s*(?:=|<-|:)\s*[\'"][^\'"]+[\'"]'

REGEX_IP = r'\b(?!127\.0\.0\.1\b)(?!0\.0\.0\.0\b)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

REGEX_BASE_64 = r'(?:"|\')?[A-Za-z0-9+/=]{40,}(?:"|\')?'

REGEX_FILE_NAME = r'["\']?(?:\.\/)?([\w.-]+)["\']?'
REGEX_EXTENSION = r'\.(\w+)$'

REGEX_GIT = r'^(https:\/\/|git@)github\.com[/:][\w.-]+\/[\w.-]+\.git'

REGEX_GIT_TOKEN = r'\bghp_[a-zA-Z0-9]{36}\b'

REGEX_SSH_KEY = r'(ssh-(rsa|ed25519|dss)|ecdsa-sha2-nistp\d{3}) [A-Za-z0-9+/=]{100,}'

REGEX_STRONG_PASSWORD = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]).{8,32}'

REGEX_EXCLUDE = r'\b(?:display_name|metadata)\b'
