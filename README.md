# Repo Scraper

Check your projects for possible password (or other sensitive data) leaks.

The library exposes three commands:
* `repo-scraper` - Auto detect target and check dir or repository
* `check_dir` - Performs checks on a folder and subdirectories
* `check_repo` - Performs a check in a git repository

All scripts work the same from the user point of view, enter any command with `--help` for more details.

## Example

### Folder
Check your project:
```bash
repo-scraper --path path/to/project
```

### Git
```bash
repo-scraper --git-path path/to/project
```
You can add `--branch NAME` to specify git branch
#### Output:
```bash
Alert! - Match in C:\Users\nicko\Documents\GitHub\repo-scraper\dummy-project\python_file_with_password.py
1. password = 'qwerty'

Alert! - Match in C:\Users\nicko\Documents\GitHub\repo-scraper\dummy-project\dangerous_file.json
1. "password": "super-secret-password"
```

## How does it work?

Briefly speaking, `check_dir` lists all files below a folder and applies regular expressions to look for passwords/IPs. Given that a blind search would never end (for example, if the repo constants a 50MB csv file), some filters are applied before the regular expressions are matched:

* **File size** - If file is bigger than 1MB, ignore it but print a warning
* **Extension** - If extension is not allowed, ignore file but print a warning. (See [NOTES](NOTES.md) to know why extension is used instead of mimetype)
* **Base64** - If file contains Base64 data, remove it. Many plain-text formats (such as Jupyter notebooks embed data in Base64 format. Applying regex to such files is never going to end)

`check_repo` works in a slightly different way, one obvious way to check git history is to check out each commit and apply `check_dir`. That approach would be really slow since the script would be checking the same files many times. Instead, `check_repo` checks out the first commit, runs `check_dir` there and then, moves up one commit at a time and uses `git diff` to get only the difference between each consecutive pair of commits.

As in `check_dir`, the script applies some filters before applying regular expressions to prevent getting stuck on big files, note that in this case we are not dealing with files, but with the `git diff` output, and that prevents us to check for file size directly:

* **Number of lines** - 
* **Number of characters** - 
* **Extension** - If extension is not allowed, ignore file but print a warning. (See [NOTES](NOTES.md) to know why extension is used instead of mimetype)
* **Base64** - Remove Base64 code.

The project has some limitations see [NOTES](NOTES.md) file for information regarding the design of the project and how that limits what the library is able to detect.

## Installation

```bash
    pip install git+git://github.com/zeinlol/repo-scraper.git -r requirements.txt
```

## Dependencies

* glob2
* nose (optional, for running tests)

## Tested with
* Python 3.9.10
* Git 2.31.1

## Usage

```bash
    cd path/to/your/project
    check_dir
```

See help for more options available:

```bash
    repo-scraper --help
```

### Using a IGNORE file while checking directory

Just as with git, you can specify a file to make the program ignore some files/folders. This is specially useful when you have folder with many log files that you are sure do not have sensitive data. The library assumes one glob rule per line.

Adding a IGNORE file will make execution faster, since many regular expressions are matched against all files that have certain characteristics.

**Important**: Even though the format is very similar, you cannot use the same rules as in your [.gitignore](https://git-scm.com/docs/gitignore) file. For more details, see [this](https://en.wikipedia.org/wiki/Glob_(programming)).

## What's done

* Passwords (using regex). See [`test_password_check.py`](tests/test_password_check.py)
* IPs
* URLs on amazonaws.com (it's simple to add more domains if needed)

## What's missing

* URLs

# TODO
* Come up with a cool name
