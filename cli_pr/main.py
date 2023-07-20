import requests
import json


def get_json_from_api(branch, arch=None):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    params = {}
    if arch is not None:
        params["arch"] = arch

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_response = response.json()
        return json_response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


branch_name = "p10"
second_branch_name = "sisyphus"
arch_name = "x86_64"
second_arch_name = "aarch64"
try:
    first_response = get_json_from_api(branch=branch_name, arch=arch_name)
    second_response = get_json_from_api(
        branch=second_branch_name, arch=second_arch_name
    )
except Exception as e:
    print(e)
# if response_json is not None:
#     print(response_json)
# else:
#     print("Ошибка при выполнении запроса.")
if first_response and second_response:
    packages_first_response = [
        package["name"] for package in first_response["packages"]
    ]
    packages_second_response = [
        package["name"] for package in second_response["packages"]
    ]
    packages_diff = list(set(packages_first_response) - set(packages_second_response))
    print(packages_diff)
