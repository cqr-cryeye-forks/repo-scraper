from repo_scraper import matchers as m, filetype
from repo_scraper.Result import *


class DiffChecker:
    def __init__(self, commit_hashes, filename, content, error, allowed_extensions):
        self.commit_hashes = commit_hashes
        self.filename = filename
        self.content = content
        self.error = error
        self.allowed_extensions = allowed_extensions

    def check(self):
        # Build the identifier using the filename and commit hashes
        identifier = f'{self.filename} ({self.commit_hashes[1]})'

        # The comments variable is a list to keep track of useful information
        # encountered when checking, right now, its only being used
        # to annotate when base64 code was removed
        comments = []

        # Check the number of additions, if there are too many
        # send a warning and skip, this may be due to a big data file addition
        if self.error:
            return Result(self.filename, self.error)

        # Check if extension/mimetype is allowed
        if filetype.get_extension(self.filename) not in self.allowed_extensions:
            return Result(identifier, FILETYPE_NOT_ALLOWED)

        # Start applying rules...
        # First check if additions contain base64, if there is remove it
        has_base64, self.content = m.base64_matcher(self.content, remove=True)
        if has_base64:
            comments.append('BASE64_REMOVED')

        # Create matcher for amazonaws.com
        amazon_aws_matcher = m.create_domain_matcher('amazonaws.com')
        # Apply matchers: password, ips and aws
        match, matches = m.multi_matcher(self.content, m.password_matcher, m.ip_matcher, amazon_aws_matcher)

        if match:
            return Result(identifier, MATCH, matches=matches, comments=comments)
        else:
            return Result(identifier, NOT_MATCH, comments=comments)
