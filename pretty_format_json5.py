import argparse
import sys
from difflib import unified_diff
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import json5


# Forked from https://github.com/pre-commit/pre-commit-hooks/blob/f48244a8055c1d51955ee6312d8942db325672cf/pre_commit_hooks/check_json.py


def _get_pretty_format(
    contents: str,
    indent: str,
    ensure_ascii: bool = True,
    sort_keys: bool = True,
    top_keys: Sequence[str] = (),
) -> str:
    def pairs_first(pairs: Sequence[Tuple[str, str]]) -> Mapping[str, str]:
        before = [pair for pair in pairs if pair[0] in top_keys]
        before = sorted(before, key=lambda x: top_keys.index(x[0]))
        after = [pair for pair in pairs if pair[0] not in top_keys]
        if sort_keys:
            after.sort()
        return dict(before + after)

    json_pretty = json5.dumps(
        json5.loads(contents, object_pairs_hook=pairs_first),
        indent=indent,
        ensure_ascii=ensure_ascii,
    )
    return f"{json_pretty}\n"


def _autofix(filename: str, new_contents: str) -> None:
    print(f"Fixing file {filename}")
    with open(filename, "w", encoding="UTF-8") as f:
        f.write(new_contents)


def parse_num_to_int(s: str) -> Union[int, str]:
    """Convert string numbers to int, leaving strings as is."""
    try:
        return int(s)
    except ValueError:
        return s


def parse_topkeys(s: str) -> List[str]:
    return s.split(",")


def get_diff(source: str, target: str, file: str) -> str:
    source_lines = source.splitlines(True)
    target_lines = target.splitlines(True)
    diff = unified_diff(source_lines, target_lines, fromfile=file, tofile=file)
    return "".join(diff)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-autofix",
        action="store_true",
        dest="no_autofix",
        default=False,
        help="Don't automatically fixes encountered not-pretty-formatted files",
    )
    parser.add_argument(
        "--indent",
        type=parse_num_to_int,
        default="2",
        help=(
            "The number of indent spaces or a string to be used as delimiter"
            ' for indentation level e.g. 4 or "\t" (Default: 2)'
        ),
    )
    parser.add_argument(
        "--ensure-ascii",
        action="store_true",
        dest="ensure_ascii",
        default=False,
        help=("Convert non-ASCII characters to Unicode escape sequences " "(\\uXXXX)"),
    )
    parser.add_argument(
        "--no-sort-keys",
        action="store_true",
        dest="no_sort_keys",
        default=False,
        help="Keep JSON nodes in the same order",
    )
    parser.add_argument(
        "--top-keys",
        type=parse_topkeys,
        dest="top_keys",
        default=[],
        help="Ordered list of keys to keep at the top of JSON hashes",
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    status = 0

    for json_file in args.filenames:
        with open(json_file, encoding="UTF-8") as f:
            contents = f.read()

        try:
            pretty_contents = _get_pretty_format(
                contents,
                args.indent,
                ensure_ascii=args.ensure_ascii,
                sort_keys=not args.no_sort_keys,
                top_keys=args.top_keys,
            )
        except ValueError:
            print(
                f"Input File {json_file} is not a valid JSON, consider using "
                f"check-json",
            )
            return 1

        if contents != pretty_contents:
            if not args.no_autofix:
                _autofix(json_file, pretty_contents)
            else:
                diff_output = get_diff(contents, pretty_contents, json_file)
                sys.stdout.buffer.write(diff_output.encode())

            status = 1

    return status


if __name__ == "__main__":
    sys.exit(main())
