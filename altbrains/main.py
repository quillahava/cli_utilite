#!/usr/bin/env python

import argparse
import json
from get_extra_lib import (
    generate_comparison_json,
)
from get_extra_lib import PackageEncoder


def main():
    parser = argparse.ArgumentParser(
        description="Altbrains allows you to compare package lists from two Alt Linux branches, generating a JSON report."
    )
    parser.add_argument("source_branch", help="Name of first branch")
    parser.add_argument("target_branch", help="Name of second branch")
    parser.add_argument("--arch", help="Arch of packages", default=None)
    args = parser.parse_args()
    print("Wait please")
    try:
        comparison_json = generate_comparison_json(
            args.source_branch, args.target_branch, args.arch
        )

        if comparison_json:
            # Writing the JSON response to the response.json file
            with open("response.json", "w") as file:
                json.dump(comparison_json, file, indent=4, cls=PackageEncoder)
        else:
            print("Couldn't get data for comparison.")
    except Exception as e:
        print(f"Error {e}")
    print('Great. The file with name "response.json" was created in current directory.')


if __name__ == "__main__":
    main()
