import os

from bin.arguments import args
from repo_scraper import matchers as m, filetype
from repo_scraper.Result import *
from repo_scraper.constants.git_diff import MAX_DIFF_ADDITIONS_CHARACTERS


class FileChecker:
    def __init__(self, path, allowed_extensions, max_file_size_bytes=MAX_DIFF_ADDITIONS_CHARACTERS):
        self.path = path
        self.max_file_size_bytes = max_file_size_bytes
        self.allowed_extensions = allowed_extensions

    def check(self):
        comments = []

        if not os.path.exists(self.path):
            return Result(self.path, MISSED_FILE)
        f_size = os.stat(self.path).st_size
        if f_size > self.max_file_size_bytes:
            return Result(self.path, BIG_FILE)

        if filetype.get_extension(self.path) not in self.allowed_extensions and not args.all_files:
            return Result(self.path, FILETYPE_NOT_ALLOWED)

        matches = []
        with open(self.path, 'r', encoding='utf8') as f:
            try:
                for i, line in enumerate(f, 1):
                    match, detected = m.multi_matcher(line.strip(),
                                                      m.multi_matcher,
                    m.base64_matcher,
                    m.url_matcher,
                    m.git_token_matcher,
                    m.ssh_key_matcher,
                    m.strong_password_matcher,
                    m.ip_matcher,
                    m.password_matcher,
                    m.pwd_matcher,
                    m.secret_key_matcher,
                    m.api_key_matcher
                    )

                    if match:
                        matches.append([i, line.strip()])
            except UnicodeDecodeError:
                return Result(self.path, FILETYPE_NOT_ALLOWED)

        if matches:
            return Result(self.path, MATCH, matches=matches, comments=comments)
        else:
            return Result(self.path, NOT_MATCH, comments=comments)
