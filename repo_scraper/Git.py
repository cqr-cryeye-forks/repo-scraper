import re
import subprocess
from functools import reduce

from repo_scraper.constants.git_diff import *
from repo_scraper.constants.regex import REGEX_FILE_NAME
from repo_scraper.constants.result import *


class Git:
    def __init__(self, git_dir):
        self.git_dir = git_dir

    def list_commits(self):
        """Returns a list with all commit hashes"""
        p = subprocess.Popen(['git', '-C', self.git_dir, 'log', '--pretty=format:%H'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        # See comments on the function definition for details
        self.check_stderr(err)
        # Split by break line to get a list and reverse the order
        # so the first commit comes first
        return str(out).replace('"', '').split('\n')[::-1]

    def diff_for_commit_to_commit(self, commit1_hash, commit2_hash):
        """Retrieves diff for a specific commit and parses it
           to get file name and additions"""
        # Pass the -M flag to detect modified files and avoid redundancy
        p = subprocess.Popen(['git', '-C', self.git_dir, 'diff', '-M', commit1_hash, commit2_hash],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        # See comments on the function definition for details
        self.check_stderr(err)

        return self.parse_diff(out)

    def parse_diff(self, diff):
        """Parse a diff output"""
        files = diff.split('diff --git ')[1:]
        files = [self.parse_file_diff(f) for f in files]
        return files

    @staticmethod
    def parse_file_diff(diff):
        """
        Parse a diff output

        https://stackoverflow.com/questions/2529441/how-to-read-the-output-from-git-diff
        """
        lines = diff.split('\n')
        # File line is the first line here, with the following format:
        # a/file.txt b/file2.txt where file and file2 are different
        # only if the file was renamed, in which case the current name is file2
        # print 'L is %s matches %s' % (lines[0], re.compile('\s{1}.{1}/{1}(.*)').findall(lines[0]))
        # note, if the filename has unusual characters, it's going to appear with quotes
        filename = re.compile(REGEX_FILE_NAME).findall(lines[0])[0]

        # If there are many lines in the diff file, the filter for additions
        # is going to break, check how many lines there are
        # print 'lines for content %s' % len(lines[1:])
        if len(lines[1:]) > MAX_DIFF_LINES:
            return {'filename': filename, 'content': None, 'error': BIG_FILE}

        # Filter only the additions (lines that start with +)
        content = filter(lambda x: x.startswith('+'), lines[1:])
        # Remove the leading + sign on each line
        content = [line.strip('+') for line in content]
        # Join the lines again
        content = reduce(lambda x, y: x + '\n' + y, content) if len(content) else ''
        # Threshold for the number of characters
        # print 'len is: %d' % len(content)
        if len(content) > MAX_DIFF_ADDITIONS_CHARACTERS:
            return {'filename': filename, 'content': None, 'error': BIG_FILE}
        else:
            return {'filename': filename, 'content': content, 'error': None}

    def checkout(self, commit_id):
        p = subprocess.Popen(['git', '-C', self.git_dir, 'checkout', commit_id], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        # See comments on the function definition for details
        self.check_stderr(err)

    # git likes to abuse standard error:
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=447395
    # I wrote this function to check for actual errors instead of
    # what git likes to send sometimes, actually the only error
    # I'm looking for right now is when the git command is ran
    # in a folder with no repository
    @staticmethod
    def check_stderr(err):
        if str(err).startswith('fatal'):
            raise NotImplementedError(err)
