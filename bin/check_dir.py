#!/usr/bin/env python3
import re
import sys

from bin.arguments import args
from bin.output import save_result
from bin.utils import get_results_level
from repo_scraper.FolderChecker import FolderChecker


def check_dir(results_to_print: list[str] = None):
    if not results_to_print:
        results_to_print = get_results_level()
    if not args.force:
        sys.exit('Aborted by the user')

    folder_path = '.' if args.path is None else args.path
    ignore_path = args.ignore

    allowed_extensions = args.extensions
    if type(args.extensions) != list:
        allowed_extensions = re.compile(r',\s*\.?').split(allowed_extensions.lower())

    # Create an instance of folder checker,
    # this class will list files in all subdirectories,
    # then apply ignoring file rules. It provides a generator
    # to check each file
    ignore_git = not args.include_git
    fc = FolderChecker(folder_path, allowed_extensions=allowed_extensions,
                       ignore_git_folder=ignore_git,
                       ignore_path=ignore_path)
    # Get the generator to traverse the folder structure
    file_traverser = fc.file_traverser()
    results_as_list = list(file_traverser)
    shown_results = []
    for result in results_as_list:
        if result.result_type in results_to_print:
            shown_results.append(result)
            print(result)
    if args.output:
        save_result(output=args.output, result=shown_results, as_json=args.json)


if __name__ == '__main__':
    check_dir()
