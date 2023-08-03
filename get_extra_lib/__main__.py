import requests
import json
import re
from packaging import version
from models import JsonResponse, Package, PackageEncoder
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
# def remove_letters_from_version(version):
#     # Используем регулярное выражение для удаления букв и знаков из начала и конца строки
#     version = re.sub(r"^[a-zA-Z.]+", "", version)
#     version = re.sub(r"[a-zA-Z.]+$", "", version)
#     # Используем регулярное выражение для удаления некорректных символов между числами
#     version = re.sub(r"[^\d.]+", "", version)
#     # Заменяем рядом стоящие точки на одну точку
#     version = re.sub(r"\.\.+", ".", version)
#     # Заменяем все буквы на пустую строку, оставляя только цифры и точки
#     result = "".join(char for char in version if char.isdigit() or char == ".")
#
#     return result
def parse_version(version_str):
    pattern = r"(\d+|[a-zA-Z]+)"
    version_components = re.findall(pattern, version_str)
    parsed_version = []

    for component in version_components:
        if component.isdigit():
            parsed_version.append(int(component))
        else:
            parsed_version.append(component)

    return parsed_version


def compare_parsed_versions(str_version_1, str_version_2):
    parsed_version_1 = parse_version(str_version_1)
    parsed_version_2 = parse_version(str_version_2)
    len1, len2 = len(parsed_version_1), len(parsed_version_2)

    # Дополняем версии нулями до одинаковой длины
    if len1 < len2:
        parsed_version_1 += [0] * (len2 - len1)
    elif len2 < len1:
        parsed_version_2 += [0] * (len1 - len2)
    for component1, component2 in zip(parsed_version_1, parsed_version_2):
        if isinstance(component1, int) and isinstance(component2, int):
            if component1 < component2:
                return str_version_2
            elif component1 > component2:
                return str_version_1
        else:
            if isinstance(component1, int):
                return str_version_1
            elif isinstance(component2, int):
                return str_version_2
            else:
                if component1 < component2:
                    return str_version_2
                elif component1 > component2:
                    return str_version_1

    return str_version_1  # If we reach this point, the versions are equal


def compare_parsed_versions_bool(str_version_1, str_version_2):
    return compare_parsed_versions(str_version_1, str_version_2) == str_version_1


# Compares package versions in two branches
# Функция для сравнения версий пакетов в разных списках
def compare_packages_versions(packages1, packages2):
    version_dict = {}

    # Заполняем словарь информацией о версиях пакетов из первого списка
    for pkg in packages2:
        key = pkg.name
        version_dict[key] = pkg.version

    # Сравниваем версии пакетов из второго списка и добавляем в результат только те, которые выше
    result = []
    for pkg in packages1:
        key = pkg.name
        if key in version_dict:
            if compare_parsed_versions_bool(pkg.version, version_dict[key]):
                result.append(pkg)

    return result


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
    packages_with_higher_version = compare_packages_versions(
        response1.packages, response2.packages
    )

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
    # version1 = "1.3.3.0.81.37d1"
    # version2 = "1.3.3.0.80.37e1"
    # print(f"version 1: {version1}")
    # print(f"version 2: {version2}")
    # print(f"highest version: {compare_parsed_versions(version1, version2)}")
    # print(f"highest version: {compare_parsed_versions(version1, version2)}")
    with open("response.json", "w") as file:
        json.dump(
            generate_comparison_json(branch_name, second_branch_name, arch=arch_name),
            file,
            indent=4,
            cls=PackageEncoder,
        )
    print(generate_comparison_json(branch_name, second_branch_name, arch_name))
    # with open("response_2.json", "w") as file:
    #     json.dump(
    #         compare_version(
    #             get_json_from_api(branch=branch_name, arch=arch_name),
    #             get_json_from_api(branch=second_branch_name, arch=arch_name),
    #         ),
    #         file,
    #         indent=4,
    #         cls=PackageEncoder,
    #     )
    # print(
    #     compare_version(
    #         get_json_from_api(branch=branch_name, arch=arch_name),
    #         get_json_from_api(branch=second_branch_name, arch=arch_name),
    #     )
    # )
