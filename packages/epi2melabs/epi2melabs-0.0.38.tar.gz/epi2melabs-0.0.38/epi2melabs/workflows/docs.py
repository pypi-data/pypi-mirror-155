#!/usr/bin/env python
"""Combine documentation files and write them out."""

import argparse
from collections import OrderedDict
import json
import os
import sys
from typing import Dict, Sequence, Tuple


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Combine documentation files and write them out.",
        usage=(
            "write_docs -p docs -s intro usage "
            "-oj nextflow_config.json -ot README.md"
        )
    )

    parser.add_argument(
        '-p',
        '--paths',
        required=True,
        nargs="+",
        help='Locations (files or dirs) in which to find doc files.'
    )

    parser.add_argument(
        '-s',
        '--sections',
        required=True,
        nargs="+",
        help='Names of required documentation sections.'
    )

    parser.add_argument(
        '-e',
        '--extensions',
        nargs="+",
        required=True,
        default=['.rst', '.txt', '.md'],
        help='List of allowed extensions.'
    )

    parser.add_argument(
        '-oj',
        '--output_json',
        help='Path at which to output JSON.'
    )

    parser.add_argument(
        '-ot',
        '--output_text',
        help='Path at which to output JSON.'
    )

    args = parser.parse_args(sys.argv[1:])
    return args


def load_file(
    name: str,
    path: str
) -> Dict[str, str]:
    """Load documentation from file."""
    with open(path) as read_in:
        contents = "".join(read_in.readlines())
        return {name: contents}


def check_path(
    path: str,
    required: Sequence[str],
    extensions: Sequence[str]
) -> Tuple[bool, str]:
    """Check if a path exists and has the right extension."""
    basename = os.path.basename(path)
    nameroot, nameext = os.path.splitext(basename)
    if (
        os.path.isfile(path)
        and nameroot in required
        and nameext in extensions
    ):
        return True, nameroot
    return False, nameroot


def load(
    paths: Sequence[str],
    required: Sequence[str],
    extensions: Sequence[str]
) -> Dict[str, str]:
    """Load documentation from paths."""
    sections = {}
    for item in paths:
        check, name = check_path(
            item, required, extensions)
        if check:
            sections.update(load_file(name, item))
            continue
        if os.path.isdir(item):
            for subitem in os.listdir(item):
                subitem_path = f"{item}/{subitem}"
                subcheck, subname = check_path(
                    subitem_path, required, extensions)
                if not subcheck:
                    continue
                sections.update(
                    load_file(subname, subitem_path))
    return sections


def check(
    found: Dict[str, str], required: Sequence[str]
) -> None:
    """Check documentation is in order."""
    notfound_reqs = []
    for req in required:
        if not found.get(req):
            notfound_reqs.append(req)

    if notfound_reqs:
        notfound = ", ".join(notfound_reqs)
        print(
            "Error: Not all expected sections "
            f"were found: {notfound}")
        sys.exit(1)

    return OrderedDict(
        [(req, found[req]) for req in required])


def write_json(
    sections: Dict[str, str], path: str, key: str = 'docs'
) -> None:
    """Write documentation to json."""
    data = {}
    if os.path.exists(path):
        with open(path, "r") as existing_file:
            try:
                data.update(json.load(existing_file))
            except json.decoder.JSONDecodeError:
                raise RuntimeError(
                    "Error: Output JSON file exists but cannot "
                    f"be loaded, it may be corrupt: {path}")
    data.update({key: sections})
    with open(path, "w") as out_file:
        json.dump(data, out_file, indent=4)


def write_text(
    sections: Dict[str, str], path: str
) -> None:
    """Write documentation to file."""
    joined_sections = ''.join(list(sections.values()))
    with open(path, "w") as new_file:
        new_file.write(joined_sections)


def main() -> None:
    """Parse arguments and launch a workflow."""
    args = parse_args()
    sections = load(args.paths, args.sections, args.extensions)
    ordered = check(sections, args.sections)
    if args.output_json:
        write_json(ordered, args.output_json)
    if args.output_text:
        write_text(ordered, args.output_text)
    if not (args.output_json or args.output_text):
        print(ordered)


if __name__ == '__main__':
    main()
