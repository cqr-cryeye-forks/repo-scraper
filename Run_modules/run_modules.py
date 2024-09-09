import os
import re
import shutil
import subprocess
import zipfile


def copy_zip_to_directory(zip_file_path, target_directory):
    if not os.path.isfile(zip_file_path):
        raise FileNotFoundError(f"Файл {zip_file_path} не найден.")

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    destination = os.path.join(target_directory, os.path.basename(zip_file_path))

    shutil.copy2(zip_file_path, destination)

    return destination


def remove_all_files(directory):
    try:
        command = f'echo 12345678 | sudo -S rm -rf {directory}'
        subprocess.run(command, shell=True, check=True)
        print(f"All files removed from directory: {directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while removing files: {e}")


def get_repo_name(input_string: str) -> str:
    def remove_suffix(name: str) -> str:
        return re.sub(r'\.zip$', '', name)

    if '/' in input_string or '\\' in input_string:
        repo_name = os.path.basename(os.path.normpath(input_string))
    elif 'github.com' in input_string:
        match = re.search(r'github\.com[:/](.*?)(?:\.git|$)', input_string)
        if match:
            repo_name = os.path.basename(match.group(1))
        else:
            raise ValueError("Invalid link to GitHub repository")
    else:
        repo_name = input_string

    repo_name = remove_suffix(repo_name)

    return repo_name


def check_name(repo_url=None, zip_file_name=None):
    if repo_url:
        get_name_from = str(repo_url)
    elif zip_file_name:
        get_name_from = str(zip_file_name)
    else:
        raise 'Use any argument: "--repo-url" [GIT_REPOSITORY] or "--input-zip" [ARCHIVE.ZIP]'

    repo_name = get_repo_name(get_name_from)
    return repo_name


def extract_archives_in(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if zipfile.is_zipfile(item_path):
            print(f"Extracting archive: {item_path}")
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
            os.remove(item_path)


def clone_repo(repo_url, dest_dir, token=None):
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_dir = os.path.join(dest_dir, repo_name)

    if token:
        if repo_url.startswith("https://"):
            repo_url = repo_url.replace("https://", f"https://{token}@")
        else:
            raise ValueError("To use the token, you need the HTTPS URL of the repository.")

    print(f"Cloning repository from URL: {repo_url}")
    try:
        subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)
    except subprocess.CalledProcessError:
        raise RepositoryNotFoundError
    return repo_dir


class RepositoryNotFoundError(ValueError):
    """Invalid link to GitHub repository"""
    pass


def count_dictionaries(nested_list):
    count = 0
    for _, inner_list in nested_list.items():
        count += len(inner_list)  # Считаем количество словарей в каждом вложенном списке
    return count
