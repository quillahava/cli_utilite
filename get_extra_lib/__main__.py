import requests
import json
import re
from packaging import version


def get_json_from_api(branch, arch=None, filename: str | None = None):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    params = {}
    if arch is not None:
        params["arch"] = arch

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_response = response.json()
        # save response to file
        if filename:
            with open(filename, "w") as file:
                json.dump(json_response, file, indent=4)

        return json_response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


# read from file
def read_json_from_file(filename: str):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def get_package_diff(response1, response2):
    packages_first_response = [package["name"] for package in response1["packages"]]
    packages_second_response = [package["name"] for package in response2["packages"]]
    packages_diff = list(set(packages_first_response) - set(packages_second_response))
    return packages_diff


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


def compare_version(response1, response2):
    packages_diff = {}
    packages1 = response1["packages"]
    packages2 = response2["packages"]

    version_release_dict1 = {
        package["name"]: version.Version(
            remove_letters_from_version(package["version"])
        )
        for package in packages1
    }

    for package in packages2:
        package_name = package["name"]
        version_release = version.Version(
            remove_letters_from_version(package["version"])
        )

        if (
            package_name in version_release_dict1
            and version_release_dict1[package_name] < version_release
        ):
            packages_diff[package_name] = version_release_dict1[package_name]

    return packages_diff


if __name__ == "__main__":
    branch_name = "p10"
    second_branch_name = "p9"
    arch_name = "x86_64"
    second_arch_name = "aarch64"
    first_response = read_json_from_file("first_branch.json")
    second_response = read_json_from_file("second_branch.json")
    if first_response == None or second_response == None:
        try:
            first_response = get_json_from_api(
                branch=branch_name, arch=arch_name, filename="first_branch.json"
            )
            second_response = get_json_from_api(
                branch=second_branch_name,
                arch=second_arch_name,
                filename="second_branch.json",
            )
        except Exception as e:
            print(e)
    if first_response and second_response:
        # packages_diff = get_package_diff(first_response, second_response)
        # # output all diff packages
        # packages_diff_2 = get_package_diff(second_response, first_response)
        packages_diff = compare_version(first_response, second_response)
        # for index, name in enumerate(packages_diff, start=1):
        #     print(f"{index}: {name}")
        for index, (package_name, version_release) in enumerate(
            packages_diff.items(), start=1
        ):
            print(f"{index}. {package_name}: {version_release}")
