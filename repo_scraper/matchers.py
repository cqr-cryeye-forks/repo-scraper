import re
from functools import reduce

from repo_scraper.constants.regex import REGEX_URL, REGEX_PASSWORD, REGEX_PWD, REGEX_IP, REGEX_BASE_64


def multi_matcher(s, *matchers):
    """Receives matchers as parameters and applies all of them"""
    results = [m(s) for m in matchers]
    # Get the flag that indicates where was a match for each matcher
    has_match = [r[0] for r in results]
    # Check if there was at least one match
    at_least_one = reduce(lambda x, y: x or y, has_match)
    # Get list of matches for each matcher, delete Nones
    list_of_lists = [r[1] for r in results if r[1] is not None]
    # Flatten list of matches, ignore None
    matches = [match for single_list in list_of_lists for match in single_list]
    # If the list is empty, return None
    matches = matches or None
    return at_least_one, matches


def base64_matcher(s, remove=False):
    base64images = re.compile(REGEX_BASE_64).findall(s)
    has_base64 = len(base64images) > 0
    return (has_base64, re.sub(REGEX_BASE_64, '""', s)) if remove else has_base64


def password_matcher(s):
    # Case 1: hardcoded passwords assigned to variables (python, r, etc)
    # or values (json, csv, etc)
    # match variable names such as password, PASSWORD, pwd, pass,
    # SOMETHING_PASSWORD assigned to strings (match = and <-)

    # Matches p_w_d='something' and similar
    pwd = re.compile(REGEX_PWD)
    # Matches pass='something' and similar
    pass_ = re.compile(REGEX_PASSWORD)

    # Case 2: URLS (e.g. SQLAlchemy engines)
    # http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html
    # Note that validating URls is really hard...
    # https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python
    urls = re.compile(REGEX_URL)

    # Case 3: Passwords in bash files (bash, psql, etc) bash parameters

    # Case 5: Pg-pass
    # http://www.postgresql.org/docs/9.3/static/libpq-pgpass.html

    # what about case 1 without quotes?

    # passwords assigned to variables whose names are nor similar to pwd
    # but the string seems a password
    regex_list = [pwd, pass_, urls]
    matches = regex_matcher(regex_list, s)
    has_password = len(matches) > 0
    matches = matches if has_password else None
    return has_password, matches


# Checks if a string has ips
# Matching IPs with regex is a thing:
# https://stackoverflow.com/questions/10086572/ip-address-validation-in-python-using-regex
def ip_matcher(s):
    ips = re.findall(REGEX_IP, s)
    # Remove obvious non-dangerous matches
    allowed_ips = ['127.0.0.1', '0.0.0.0']
    ips = [ip for ip in ips if ip not in allowed_ips]
    return (True, ips) if len(ips) else (False, None)


def create_domain_matcher(domain):
    """Returns a function that serves as a matcher for a given domain"""

    def domain_matcher(s):
        regex = r'\S+\.' + domain.replace('.', '\.')
        matches = re.findall(regex, s)
        return (True, matches) if len(matches) else (False, None)

    return domain_matcher


def regex_matcher(regex_list, s):
    """Get a list of regex and return all matches, removes duplicates
    in case more than own regex matches the same pattern (pattern location
    is taken into account to determine where two matches are the same)."""
    # Find matches and position for each regex
    results = [match_with_position(regex, s) for regex in regex_list]
    # Flatten list
    results = reduce(lambda x, y: x + y, results)
    # Convert to set to remove duplicates
    results = set(results)
    # Extract matches only (without position)
    results = [res[1] for res in results]
    return results


def match_with_position(regex, s):
    """Returns a list of tuples (pos, match) for each match."""
    return [(m.start(), m.group()) for m in regex.finditer(s)]
