# This file contains utility functions for working with the filesystem
import os
from functools import reduce

import glob2 as glob


def list_files_in(directory, ignore_git_folder, ignore_file):
    """Receives a path to a directory and returns
    paths to all files along with each mimetype"""
    file_list = []
    for root, dirs, files in os.walk(directory):
        file_list.extend(os.path.join(root, file) for file in files)
    file_list = set(file_list)

    glob_rules = []

    if ignore_git_folder:
        glob_rules.append('.git/**')

    # Check if ignore file was provided
    if ignore_file is not None:
        glob_rules += parse_ignore_file(ignore_file)

    if len(glob_rules):
        glob_matches = match_glob_rules_in_directory(glob_rules, directory)
        # Remove files in file_list that matched any glob rule
        file_list = file_list - glob_matches

    return file_list


def match_glob_rules_in_directory(glob_rules, directory):
    # Append directory to each glob_rule
    glob_rules = [os.path.join(directory, rule) for rule in glob_rules]
    glob_matches = [glob.glob(rule) for rule in glob_rules]
    # Flatten matches
    glob_matches = reduce(lambda x, y: x + y, glob_matches)
    # Convert to a set to remove duplicates
    return set(glob_matches)


def parse_ignore_file(ignore_file):
    # Open file
    with open(ignore_file, 'r') as f:
        lines = f.read().splitlines()
    # Filter lines starting with #
    lines = filter(lambda line: not line.startswith('#'), lines)
    # Remove empty lines
    lines = filter(lambda line: len(line) > 0, lines)
    return lines
