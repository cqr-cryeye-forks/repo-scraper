import re

from repo_scraper.constants.regex import REGEX_EXTENSION


def get_extension(filename):
    try:
        extensions = re.compile(REGEX_EXTENSION).findall(filename)
        if not extensions:
            return None
        return extensions[0].lower()
    except Exception as err:
        print(f'Get extension error: {err}')
        return None
