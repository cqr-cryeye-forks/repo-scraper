import json
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

    def check_json_for_secrets(self, json_content):
        matches = []
        for key, value in json_content.items():
            if isinstance(value, str):
                # Применяем регулярные выражения для проверки значений
                match, _ = m.multi_matcher(value.strip(),
                                           m.password_matcher,
                                           m.git_token_matcher,
                                           m.ssh_key_matcher,
                                           m.strong_password_matcher)
                if match:
                    matches.append([None, f"{key}: {value.strip()}"])  # Номера строки нет, так как это JSON
            elif isinstance(value, dict):
                # Рекурсивно проверяем вложенные словари
                matches.extend(self.check_json_for_secrets(value))
        return matches

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
        if self.path.endswith('.json'):
            with open(self.path, 'r', encoding='utf-8') as f:
                try:
                    json_content = json.load(f)
                    matches.extend(self.check_json_for_secrets(json_content))
                except json.JSONDecodeError:
                    pass  # Пропускаем файлы с ошибками в JSON
        else:
            with open(self.path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    match, _ = m.multi_matcher(line.strip(),
                                               m.password_matcher,
                                               m.git_token_matcher,
                                               m.ssh_key_matcher,
                                               m.strong_password_matcher)
                    if match:
                        matches.append([i, line.strip()])

        if matches:
            return Result(self.path, MATCH, matches=matches, comments=comments)
        else:
            return Result(self.path, NOT_MATCH, comments=comments)
