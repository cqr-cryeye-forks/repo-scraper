import re
from functools import reduce

from repo_scraper.constants.regex import REGEX_URL, REGEX_PASSWORD, REGEX_PWD, REGEX_BASE_64, REGEX_IP


def multi_matcher(s, *matchers):
    """Получает matchers как параметры и применяет их все"""
    results = [m(s) for m in matchers]
    has_match = [r[0] for r in results]
    at_least_one = reduce(lambda x, y: x or y, has_match)
    list_of_lists = [r[1] for r in results if r[1] is not None]
    matches = [match for single_list in list_of_lists for match in single_list]
    matches = matches or None
    return at_least_one, matches


def password_matcher(s):
    pwd = re.compile(REGEX_PWD)
    pass_ = re.compile(REGEX_PASSWORD)
    urls = re.compile(REGEX_URL)

    matches = []

    for i, line in enumerate(s.splitlines(), 1):
        if pwd.search(line) or pass_.search(line) or urls.search(line):
            matches.append((i, line.strip()))

    return bool(matches), matches


def base64_matcher(s, remove=False):
    base64images = re.compile(REGEX_BASE_64).findall(s)
    has_base64 = len(base64images) > 0
    return (has_base64, re.sub(REGEX_BASE_64, '""', s)) if remove else has_base64


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
