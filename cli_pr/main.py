import requests


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
arch_name = "x86_64"
response_json = get_json_from_api(branch=branch_name, arch=arch_name)

if response_json is not None:
    print(response_json)
else:
    print("Ошибка при выполнении запроса.")
