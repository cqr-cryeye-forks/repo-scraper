import argparse
import os
import pathlib
import subprocess
import time
from pathlib import Path
from typing import List, Final

from run_modules import check_name, clone_repo, RepositoryNotFoundError, copy_zip_to_directory, \
    remove_all_files, extract_archives_in, load_gitignore, save_results_to_json


def should_ignore(file_path: Path, ignore_patterns, use_gitignore=False):
    if use_gitignore:
        for pattern in ignore_patterns:
            if file_path.match(pattern):
                return False

    if file_path.suffix not in FILE_SUFFIX_CHECKER:
        return False

    return True


def analyze_file_with_repo_scraper(file_path: Path):
    file_suffix = file_path.suffix.lower()

    if file_suffix in FILE_SUFFIX_CHECKER:
        command = ['repo-scraper', '--path', str(file_path)]
    else:
        return None

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode()
    except Exception as e:
        return f"Error running repo-scraper: {str(e)}"


def scan_files(directory, ignore_patterns: List[str], use_gitignore=False):
    vulnerabilities = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ['.git', '.idea', '__pycache__']]
        for file in files:
            file_path = pathlib.Path(os.path.join(root, file))

            if should_ignore(file_path, ignore_patterns, use_gitignore):
                print(f"Scanning file: {file_path}")
                result = analyze_file_with_repo_scraper(file_path)
                vulnerabilities.append(result)


def prepare_repository(repo_url=None, zip_file_name=None, token=None):
    repo_name = check_name(repo_url=repo_url, zip_file_name=zip_file_name)
    directory: Final[pathlib.Path] = MAIN_DIR / repo_name
    directory.mkdir(parents=True, exist_ok=True)

    if repo_url:
        print(f"Directory {directory} is empty. Cloning repository...")
        try:
            clone_repo(repo_url, directory, token)
        except RepositoryNotFoundError:
            remove_all_files(directory)
            return
    elif zip_file_name:
        zip_file_path = directory / zip_file_name
        copy_zip_to_directory(zip_file_path, directory)
    else:
        print(f"Directory {directory} is empty.")

    return directory


def process_repository(directory, use_gitignore=False):
    extract_archives_in(directory)

    ignore_patterns = []
    if use_gitignore:
        ignore_patterns = load_gitignore(directory)

    vulnerabilities = scan_files(directory, ignore_patterns, use_gitignore)

    remove_all_files(directory)

    if not vulnerabilities:
        vulnerabilities = {"Empty": "No vulnerable patterns found"}

    return vulnerabilities


def main(repo_url=None, zip_file_name=None, json_file=None, use_gitignore=None):
    directory = prepare_repository(repo_url=repo_url, zip_file_name=zip_file_name)
    if directory:
        vulnerabilities = process_repository(directory, use_gitignore=use_gitignore)
    else:
        vulnerabilities = {"Error": "Invalid link to GitHub repository, try to use git token with Registry"}
    save_results_to_json(vulnerabilities, json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan repository or directory for files.')
    parser.add_argument('--repo-url', type=str, help='URL of the git repository.')
    # parser.add_argument('--token', type=str, help='GitHub Personal Access Token for private repositories.')
    parser.add_argument('--input-zip', type=pathlib.Path, help='Path to the input zip.')
    parser.add_argument('--output', type=pathlib.Path, help='Path to save the analysis results in JSON format.')
    parser.add_argument('--git-ignore', action='store_true', help='Use .gitignore to skip files and directories.')
    parser.add_argument('--suffix', default='all',
                        help="Use suffix for only this file type, choose any (1-10)"
                             "['.py','.js','.ts','.yaml','.yml','.json','.cfg','.ini','.md','.txt',]"
                        )

    args = parser.parse_args()
    MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent
    JSON_FILE: Final[pathlib.Path] = MAIN_DIR / args.output
    FILE_SUFFIX_CHECKER = args.suffix
    if args.suffix == 'all':
        FILE_SUFFIX_CHECKER = [
            '.py',
            '.js',
            '.ts',
            '.yaml',
            '.yml',
            '.json',
            '.cfg',
            '.ini',
            '.md',
            '.txt',
        ]
    time_start = time.time()
    main(repo_url=args.repo_url, zip_file_name=args.input_zip, json_file=JSON_FILE, use_gitignore=args.git_ignore)
    print(time.time() - time_start)
