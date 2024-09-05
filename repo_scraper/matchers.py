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
    REGEX_API_KEY,
)


def multi_matcher(s, *matchers):
    results = [m(s) for m in matchers]
    has_match = any(r[0] for r in results)
    matches = [match for r in results if r[1] for match in r[1]]
    return has_match, matches or None


def base64_matcher(s, remove=False):
    matches = re.findall(REGEX_BASE_64, s)
    if matches and remove:
        for match in matches:
            s = s.replace(match, "")
        return False, s
    return bool(matches), matches


def password_matcher(s):
    matches = re.findall(REGEX_PASSWORD, s)
    return bool(matches), matches


def url_matcher(s):
    matches = re.findall(REGEX_URL, s)
    return bool(matches), matches


def pwd_matcher(s):
    matches = re.findall(REGEX_PWD, s)
    return bool(matches), matches


def git_token_matcher(s):
    matches = re.findall(REGEX_GIT_TOKEN, s)
    return bool(matches), matches


def ssh_key_matcher(s):
    matches = re.findall(REGEX_SSH_KEY, s)
    return bool(matches), matches


def strong_password_matcher(s):
    matches = re.findall(REGEX_STRONG_PASSWORD, s)
    return bool(matches), matches


def secret_key_matcher(s):
    matches = re.findall(REGEX_SECRET_KEY, s)
    return bool(matches), matches


def api_key_matcher(s):
    matches = re.findall(REGEX_API_KEY, s)
    return bool(matches), matches


def ip_matcher(s):
    matches = re.findall(REGEX_IP, s)
    return bool(matches), matches
