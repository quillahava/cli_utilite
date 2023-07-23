import requests
import json
import re
from packaging import version
from .models import JsonResponse, Package, PackageEncoder
from typing import List, Dict, Union


# Makes a request to the API and returns a json response
def get_json_from_api(branch, arch=None, filename: str | None = None):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    params = {}
    if arch is not None:
        params["arch"] = arch

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_response = JsonResponse(**response.json())
        # save response to file
        if filename:
            with open(filename, "w") as file:
                json.dump(json_response, file, indent=4)

        return json_response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


# Read from file
def read_json_from_file(filename: str):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


# Returns a list of packages that are in the first branch and not in the second
def get_package_diff(
    response_source: JsonResponse, response_target: JsonResponse
) -> List[Package]:
    packages_first_response = {
        package.name: package for package in response_source.packages
    }
    packages_second_response = {
        package.name: package for package in response_target.packages
    }

    packages_diff = []
    for package_name in packages_first_response:
        if package_name not in packages_second_response:
            package = packages_first_response[package_name]
            packages_diff.append(package)

    return packages_diff


# Returns the string 'version' to the comparative form
def remove_letters_from_version(version):
    # Используем регулярное выражение для удаления букв и знаков из начала и конца строки
    version = re.sub(r"^[a-zA-Z.]+", "", version)
    version = re.sub(r"[a-zA-Z.]+$", "", version)
    # Используем регулярное выражение для удаления некорректных символов между числами
    version = re.sub(r"[^\d.]+", "", version)
    # Заменяем рядом стоящие точки на одну точку
    version = re.sub(r"\.\.+", ".", version)
    # Заменяем все буквы на пустую строку, оставляя только цифры и точки
    result = "".join(char for char in version if char.isdigit() or char == ".")

    return result


# Compares package versions in two branches
def compare_version(response1: JsonResponse, response2: JsonResponse):
    packages_diff = []
    packages1 = response1.packages
    packages2 = response2.packages

    version_release_dict1 = {}
    for package in packages1:
        version_str = package.version
        processed_version = remove_letters_from_version(version_str)
        if processed_version:
            version_release_dict1[package.name] = {
                "processed_version": version.Version(processed_version),
                "original_version": version_str,
            }

    for package in packages2:
        package_name = package.name
        version_str = package.version
        processed_version = remove_letters_from_version(version_str)

        if processed_version:
            version_release = version.Version(processed_version)

            if (
                package_name in version_release_dict1
                and version_release_dict1[package_name]["processed_version"]
                < version_release
            ):
                original_version = version_release_dict1[package_name][
                    "original_version"
                ]
                package_to_response = Package(
                    name=package_name, version=original_version, release=package.release
                )
                packages_diff.append(package_to_response)

    return packages_diff


# Generates a response in json format
def generate_comparison_json(
    source_branch: str, target_branch: str, arch: str | None = None
):
    response1: JsonResponse | None = get_json_from_api(source_branch, arch)
    response2: JsonResponse | None = get_json_from_api(target_branch, arch)

    if not response1 or not response2:
        return None

    packages_in_source_branch = response1.length
    packages_in_target_branch = response2.length

    packages_diff_source = get_package_diff(response1, response2)
    packages_diff_target = get_package_diff(response2, response1)
    packages_with_higher_version = compare_version(response1, response2)

    comparison_json = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "source_packages_count": packages_in_source_branch,
        "target_packages_count": packages_in_target_branch,
        "packages_only_in_source_branch": {
            "count": len(packages_diff_source),
            "packages": packages_diff_source,
        },
        "packages_only_in_target_branch": {
            "count": len(packages_diff_target),
            "packages": packages_diff_target,
        },
        "packages_with_higher_version_in_source_branch": {
            "count": len(packages_with_higher_version),
            "packages": packages_with_higher_version,
        },
    }

    return comparison_json


if __name__ == "__main__":
    branch_name = "p10"
    second_branch_name = "p9"
    arch_name = "x86_64"
    with open("response.json", "w") as file:
        json.dump(
            generate_comparison_json(branch_name, second_branch_name, arch=arch_name),
            file,
            indent=4,
        )
