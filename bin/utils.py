from bin.arguments import args
from repo_scraper.constants.result import ALERT, WARNING, NOTHING


def get_results_level() -> list:
    results_to_print = [ALERT]
    if args.warnings:
        results_to_print += [WARNING]
    elif args.printall:
        results_to_print += [WARNING, NOTHING]
    return results_to_print
