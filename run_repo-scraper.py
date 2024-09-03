import argparse
import pathlib
import subprocess
import time
from pathlib import Path
from typing import Final

from Run_modules.run_modules import check_name, clone_repo, RepositoryNotFoundError, copy_zip_to_directory, \
    remove_all_files, extract_archives_in, save_results_to_json


def analyze_file_with_repo_scraper(file_path: Path):
    command = ['python3', 'repo-scraper', '--path', str(file_path), "--force"]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode()
    except Exception as e:
        return f"Error running repo-scraper: {str(e)}"


def scan_files(directory):
    vulnerabilities = []
    result = analyze_file_with_repo_scraper(directory)
    if result:
        vulnerabilities.append(result)
    return vulnerabilities


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

    vulnerabilities = scan_files(directory)

    remove_all_files(directory)

    if not vulnerabilities:
        vulnerabilities = {"Empty": "No sensitive data or issues found"}

    return vulnerabilities


def main(repo_url=None, zip_file_name=None, json_file=None):
    directory = prepare_repository(repo_url=repo_url, zip_file_name=zip_file_name)
    if directory:
        vulnerabilities = process_repository(directory)
    else:
        vulnerabilities = {"Error": "Invalid link to GitHub repository, try to use git token with Registry"}
    save_results_to_json(vulnerabilities, json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan repository or directory for files.')
    parser.add_argument('--repo-url', type=str, help='URL of the git repository.')
    # parser.add_argument('--token', type=str, help='GitHub Personal Access Token for private repositories.')
    parser.add_argument('--input-zip', type=pathlib.Path, help='Path to the input zip.')
    parser.add_argument('--output', type=pathlib.Path, help='Path to save the analysis results in JSON format.')
    parser.add_argument('--suffix', default='all',
                        help="Use suffix for only this file type, choose any (1-10)"
                             '["py", "ipynb", "json", "sql", "sh", "txt", "r", "md", "log", "yaml", "php"]'
                        )

    args = parser.parse_args()
    MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent
    JSON_FILE: Final[pathlib.Path] = MAIN_DIR / args.output
    FILE_SUFFIX_CHECKER = args.suffix
    if args.suffix == 'all':
        FILE_SUFFIX_CHECKER = [".py", ".ipynb", ".json", ".sql", ".sh", ".txt", ".r", ".md", ".log", ".yaml", ".php"]

    time_start = time.time()
    main(repo_url=args.repo_url, zip_file_name=args.input_zip, json_file=JSON_FILE)
    print(time.time() - time_start)
