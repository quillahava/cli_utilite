#!/usr/bin/env python

import argparse
import json
from get_extra_lib import (
    get_json_from_api,
    get_package_diff,
    compare_version,
    generate_comparison_json,
)


def main():
    parser = argparse.ArgumentParser(
        description="CLI utility for comparing lists of binary packages"
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
                json.dump(comparison_json, file, indent=4)
        else:
            print("Couldn't get data for comparison.")
    except Exception as e:
        print(f"Error {e}")


if __name__ == "__main__":
    main()
