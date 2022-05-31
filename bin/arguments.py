import argparse
import os

from repo_scraper.constants.extensions import DEFAULT_EXTENSIONS_FORMAT, DEFAULT_EXTENSIONS

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, default=os.getcwd(),
                    help="Directory or Git repository location, if this is not provided, "
                         f"the script will run on the working directory (now: {os.getcwd()})")
parser.add_argument("-e", "--extensions", default=DEFAULT_EXTENSIONS,
                    help=f"Comma-separated extensions, files that don't match any of these will raise a warning. "
                         f"If empty, uses default list: {DEFAULT_EXTENSIONS_FORMAT}")
parser.add_argument("-gp", "--git-path", type=str,
                    help="Git repository location, if this is not provided, the script will run on the "
                         "working directory")
parser.add_argument("-i", "--ignore", type=str, help="Optional ignore file")
parser.add_argument("-b", "--branch", type=str, default='master', help="Choose branch. Default is master")
parser.add_argument("-o", "--output", type=str, help="Output file for results")
parser.add_argument("-j", "--json", action="store_true", help="Save results as json")
parser.add_argument("-w", "--warnings", action="store_true", help="Print warnings (and alerts)")
parser.add_argument("-a", "--printall", action="store_true",
                    help="Print everything (alerts, warnings and non-matches)")
parser.add_argument("-f", "--force", action="store_true",
                    help="Force execution, prevents confirmation prompt form appearing")
parser.add_argument("-g", "--include-git", action="store_true",
                    help="Includes .git/ folder in the search scope, disabled by default")

args = parser.parse_args()
