import argparse
import re
import sys
from difflib import unified_diff
from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import json5


# Forked from https://github.com/pre-commit/pre-commit-hooks/blob/f48244a8055c1d51955ee6312d8942db325672cf/pre_commit_hooks/check_json.py


def _is_valid_identifier(key: str) -> bool:
    """Check if a key is a valid JavaScript identifier and can be unquoted."""
    if not key:
        return False
    # Must start with letter, underscore, or dollar sign
    if not re.match(r"^[a-zA-Z_$]", key):
        return False
    # Rest can be letters, digits, underscores, or dollar signs
    return re.match(r"^[a-zA-Z_$][a-zA-Z0-9_$]*$", key) is not None


def _format_value(
    value: Any,
    indent_level: int,
    indent_str: str,
    ensure_ascii: bool,
    sort_keys: bool,
    top_keys: Sequence[str],
    is_json5: bool = True,
) -> str:
    """Format a JSON5 value with proper indentation and type handling."""
    if value is None:
        return "null"
    elif value is True:
        return "true"
    elif value is False:
        return "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        # Use JSON5 string formatting which handles escaping
        if ensure_ascii:
            return json5.dumps(value, ensure_ascii=True)
        else:
            return json5.dumps(value, ensure_ascii=False)
    elif isinstance(value, list):
        if not value:
            return "[]"

        items = []
        for item in value:
            formatted_item = _format_value(
                item,
                indent_level + 1,
                indent_str,
                ensure_ascii,
                sort_keys,
                top_keys,
                is_json5,
            )
            items.append(f"{indent_str * (indent_level + 1)}{formatted_item}")

        return "[\n" + ",\n".join(items) + ",\n" + indent_str * indent_level + "]"
    elif isinstance(value, dict):
        if not value:
            return "{}"

        # Sort keys according to preferences
        def pairs_first(items):
            before = [(k, v) for k, v in items if k in top_keys]
            before = sorted(before, key=lambda x: top_keys.index(x[0]))
            after = [(k, v) for k, v in items if k not in top_keys]
            if sort_keys:
                after.sort()
            return before + after

        sorted_items = pairs_first(value.items())

        formatted_items = []
        for key, val in sorted_items:
            formatted_val = _format_value(
                val,
                indent_level + 1,
                indent_str,
                ensure_ascii,
                sort_keys,
                top_keys,
                is_json5,
            )

            # Determine if key needs quotes - for JSON files, always quote keys
            # For JSON5 files, use unquoted keys when possible for valid identifiers
            if is_json5 and _is_valid_identifier(key):
                formatted_key = key
            else:
                formatted_key = json5.dumps(key, ensure_ascii=ensure_ascii)

            formatted_items.append(
                f"{indent_str * (indent_level + 1)}{formatted_key}: {formatted_val}"
            )

        return (
            "{\n"
            + ",\n".join(formatted_items)
            + ",\n"
            + indent_str * indent_level
            + "}"
        )
    else:
        # Fallback to json5 for any other types
        return json5.dumps(value, ensure_ascii=ensure_ascii)


def _preserve_comments(original: str, formatted: str) -> str:
    """Attempt to preserve comments from the original JSON5."""
    # For now, return formatted without comment preservation
    # Comment preservation is complex and would require a full parser
    return formatted


def _get_pretty_format(
    contents: str,
    indent: str,
    ensure_ascii: bool = True,
    sort_keys: bool = True,
    top_keys: Sequence[str] = (),
    is_json5: bool = True,
) -> str:
    # Parse the JSON5 content
    try:
        parsed = json5.loads(contents)
    except Exception as e:
        raise ValueError(f"Invalid JSON5: {e}")

    # Convert indent to string if it's an integer
    if isinstance(indent, int):
        indent_str = " " * indent
    else:
        indent_str = str(indent)

    # Format the content
    formatted = _format_value(
        parsed, 0, indent_str, ensure_ascii, sort_keys, top_keys, is_json5
    )

    # Try to preserve comments
    formatted = _preserve_comments(contents, formatted)

    return f"{formatted}\n"


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

        # Determine if this is a JSON5 file based on extension
        is_json5 = json_file.lower().endswith(".json5")

        try:
            pretty_contents = _get_pretty_format(
                contents,
                args.indent,
                ensure_ascii=args.ensure_ascii,
                sort_keys=not args.no_sort_keys,
                top_keys=args.top_keys,
                is_json5=is_json5,
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
