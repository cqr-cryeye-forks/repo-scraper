#!/usr/bin/env python3
import re
import sys

from bin.arguments import args
from bin.output import save_result
from bin.utils import get_results_level
from repo_scraper.GitChecker import GitChecker


def check_repo(results_to_print: list = None):
    if not results_to_print:
        results_to_print = get_results_level()

    if not args.force:
        continue_ = "y"
        if continue_.lower() != 'y':
            sys.exit('Aborted by the user')

    allowed_extensions = args.extensions
    if type(args.extensions) != list:
        allowed_extensions = re.compile(',\s*\.?').split(allowed_extensions.lower())

    # Default path is working directory, change if user
    # specified a different one
    path = '.' if args.git_path is None else args.git_path

    # Create an instance of git checker_parser.add_argument("-v", "--verbose", action="store_true",
    # help="prints all results, including no matches and warnings")
    gc = GitChecker(allowed_extensions=allowed_extensions, git_dir=path, git_branch=args.branch)

    # Get the generator that will turn one resul per file modified in each commit
    file_traverser = gc.file_traverser()
    results_as_list = list(file_traverser)
    shown_results = []
    for result in results_as_list:
        if result.result_type in results_to_print:
            shown_results.append(result)
            print(result)
    if args.output:
        save_result(output=args.output, result=shown_results, as_json=args.json)


if __name__ == '__main___':
    check_repo()
