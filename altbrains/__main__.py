#!/usr/bin/env python

import argparse
from get_extra_lib import write_to_file


def main():
    parser = argparse.ArgumentParser(
        description="Altbrains allows you to compare package lists from two Alt Linux branches, generating a JSON report."
    )
    parser.add_argument("source_branch", help="Name of first branch")
    parser.add_argument("target_branch", help="Name of second branch")
    parser.add_argument("-f", "--filename", help="Output file", default="response")
    parser.add_argument("--arch", help="Arch of packages", default=None)
    args = parser.parse_args()
    print("Wait please")
    write_to_file(
        first_branch=args.source_branch,
        second_branch=args.target_branch,
        filename=args.filename,
        arch=args.arch,
    )
    print(
        f'Great. The file with name "{args.filename}.json" was created in current directory.'
    )


if __name__ == "__main__":
    main()
