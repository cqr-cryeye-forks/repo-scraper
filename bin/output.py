import json

from repo_scraper.Result import Result, Results


def save_result(output: str, result: list[Result], as_json: bool = True):
    print(f"Saving results to {output}...")
    try:
        with open(output, 'w') as file:
            if as_json:
                data = Results.parse_obj({'results': result}).dict()
                json.dump(data, file, indent=2)
            else:
                result_str = 'Result:\n'.join("\n".join(
                    f"`{name}={getattr(res, name)}`"
                    for name in dir(res) if not name.startswith("__")) for res in result)
                file.writelines(result_str)
        print(f"Saving results to {output} success")
    except Exception as err:
        print(f"Saving results to {output} error: {err}")
