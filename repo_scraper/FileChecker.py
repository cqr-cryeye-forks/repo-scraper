import os

from bin.arguments import args
from repo_scraper import filetype, matchers as m
from repo_scraper.Result import *
from repo_scraper.constants.git_diff import MAX_DIFF_ADDITIONS_CHARACTERS


class FileChecker:
    def __init__(self, path, allowed_extensions, max_file_size_bytes=MAX_DIFF_ADDITIONS_CHARACTERS):
        self.path = path
        self.max_file_size_bytes = max_file_size_bytes
        self.allowed_extensions = allowed_extensions

    def check(self):
        # print(f'Testing file {self.path}')
        # The comments variable is a list to keep track of useful information
        # encountered when checking, right now, its only being used
        # to annotate when base64 code was removed
        comments = []

        # Check file size if it's more than max_file_size_bytes (default is 10MB)
        # send just a warning and do not open the file,
        # since pattern matching is going to be really slow
        if not os.path.exists(self.path):
            return Result(self.path, MISSED_FILE)
        f_size = os.stat(self.path).st_size
        if f_size > self.max_file_size_bytes:
            return Result(self.path, BIG_FILE)

        # Check if extension is allowed
        if filetype.get_extension(self.path) not in self.allowed_extensions and not args.all_files:
            return Result(self.path, FILETYPE_NOT_ALLOWED)

        # At this point you only have files with allowed extensions and
        # smaller than max_file_size_bytes
        # open the file and then apply all rules
        with open(self.path, 'r', encoding='utf8') as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                return Result(self.path, FILETYPE_NOT_ALLOWED)

        # Last check: search for potential base64 strings and remove them, send a warning
        has_base64, content = m.base64_matcher(content, remove=True)
        if has_base64:
            comments.append('BASE64_REMOVED')

        # Create matcher for amazonaws.com
        amazon_aws_matcher = m.create_domain_matcher('amazonaws.com')
        # Apply matchers: password, ips and aws
        match, matches = m.multi_matcher(content, m.password_matcher, m.ip_matcher, amazon_aws_matcher)

        if match:
            return Result(self.path, MATCH, matches=matches, comments=comments)
        else:
            return Result(self.path, NOT_MATCH, comments=comments)
