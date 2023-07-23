#!/usr/bin/env python

import argparse
import json
from get_extra_lib import (
    generate_comparison_json,
)
from get_extra_lib import PackageEncoder


def main():
    parser = argparse.ArgumentParser(
        description="CLI utility for comparing lists of binary packages. This utility allows you to compare two branches of binary packages from an Alt Linux repository. It retrieves package lists from the specified branches, performs a comparison, and generates a JSON report containing three sections:\n\n1. 'packages_in_branch1': A list of package names that exist in the first branch but not in the second branch.\n\n2. 'packages_in_branch2': A list of package names that exist in the second branch but not in the first branch.\n\n3. 'packages_with_higher_version_in_branch1': A dictionary of package names and their respective versions from the first branch that have higher versions than those in the second branch.\n\nThe generated 'response.json' file will be placed in the current working directory. The comparison is based on the package names and their version numbers (after removing letters and special characters) to ensure accurate results. Note that this utility requires an active internet connection to access the Alt Linux repository API."
    )
    parser.add_argument("branch1", help="Name of first branch")
    parser.add_argument("branch2", help="Name of second branch")
    parser.add_argument("--arch", help="Arch of packages", default=None)
    args = parser.parse_args()

    try:
        comparison_json = generate_comparison_json(
            args.branch1, args.branch2, args.arch
        )

        if comparison_json:
            # Writing the JSON response to the response.json file
            with open("response.json", "w") as file:
                json.dump(comparison_json, file, indent=4, cls=PackageEncoder)
        else:
            print("Couldn't get data for comparison.")
    except Exception as e:
        print(f"Error {e}")


if __name__ == "__main__":
    main()
