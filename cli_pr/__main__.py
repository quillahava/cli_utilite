import requests
import json


def get_json_from_api(branch, arch=None, filename: str = "first_branch.json"):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    params = {}
    if arch is not None:
        params["arch"] = arch

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_response = response.json()
        # save response to file
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


if __name__ == "__main__":
    branch_name = "p10"
    second_branch_name = "sisyphus"
    arch_name = "x86_64"
    second_arch_name = "aarch64"
    try:
        first_response = read_json_from_file("first_branch.json")
        second_response = read_json_from_file("second_branch.json")
        if first_response == None or second_response == None:
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
        packages_first_response = [
            package["name"] for package in first_response["packages"]
        ]
        packages_second_response = [
            package["name"] for package in second_response["packages"]
        ]
        packages_diff = list(
            set(packages_first_response) - set(packages_second_response)
        )
        print(packages_diff)
