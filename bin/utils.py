from bin.arguments import args
from repo_scraper.constants.result import ALERT, WARNING, NOTHING, ERROR


def get_results_level() -> list:
    results_to_print = [ALERT, ERROR]
    if args.warnings:
        results_to_print.append(WARNING)
    elif args.printall:
        results_to_print.extend([WARNING, NOTHING])
    return results_to_print
