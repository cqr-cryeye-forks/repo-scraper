import re
from repo_scraper.constants.regex import (
    REGEX_URL,
    REGEX_PASSWORD,
    REGEX_PWD,
    REGEX_BASE_64,
    REGEX_GIT_TOKEN,
    REGEX_SSH_KEY,
    REGEX_STRONG_PASSWORD,
    REGEX_SECRET_KEY,
    REGEX_IP,
)


def multi_matcher(s, *matchers):
    results = [m(s) for m in matchers]
    has_match = any(r[0] for r in results)
    matches = [match for r in results if r[1] for match in r[1]]
    return has_match, matches or None


def base64_matcher(s, remove=False):
    matches = re.findall(REGEX_BASE_64, s)
    has_base64 = len(matches) > 0
    return (has_base64, re.sub(REGEX_BASE_64, '""', s)) if remove else (has_base64, matches)


def password_matcher(s):
    pwd = re.compile(REGEX_PWD, re.IGNORECASE)
    pass_ = re.compile(REGEX_PASSWORD, re.IGNORECASE)
    urls = re.compile(REGEX_URL, re.IGNORECASE)
    secret_key = re.compile(REGEX_SECRET_KEY, re.IGNORECASE)

    matches = []

    for i, line in enumerate(s.splitlines(), 1):
        if pwd.search(line) or pass_.search(line) or urls.search(line) or secret_key.search(line):
            matches.append((i, line.strip()))

    return bool(matches), matches


def create_domain_matcher(domain):
    """Возвращает функцию, которая служит матчером для данного домена"""

    def domain_matcher(s):
        regex = r'\S+\.' + domain.replace('.', r'\.')
        matches = re.findall(regex, s)
        return (True, matches) if matches else (False, None)

    return domain_matcher


def ip_matcher(s):
    """Ищет IP-адреса в строке."""
    ips = re.findall(REGEX_IP, s)
    # Удаляем очевидные безопасные IP-адреса
    allowed_ips = ['127.0.0.1', '0.0.0.0']
    ips = [ip for ip in ips if ip not in allowed_ips]
    return (True, ips) if ips else (False, None)


def git_token_matcher(s):
    """Ищет Git-токены в строке"""
    matches = re.findall(REGEX_GIT_TOKEN, s)
    return (True, matches) if matches else (False, None)


def ssh_key_matcher(s):
    """Ищет SSH-ключи в строке"""
    matches = re.findall(REGEX_SSH_KEY, s)
    return (True, matches) if matches else (False, None)


def strong_password_matcher(s):
    """Ищет сильные пароли (8-32 символа) в строке"""
    matches = re.findall(REGEX_STRONG_PASSWORD, s)
    return (True, matches) if matches else (False, None)
