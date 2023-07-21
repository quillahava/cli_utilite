#!/usr/bin/env python

import argparse
from get_extra_lib import get_json_from_api, get_package_diff, compare_version


def main():
    parser = argparse.ArgumentParser(
        description="CLI утилита для сравнения списков бинарных пакетов"
    )
    parser.add_argument("branch1", help="Имя первой ветки")
    parser.add_argument("branch2", help="Имя второй ветки")
    parser.add_argument("--arch", help="Архитектура пакетов", default="x86_64")
    args = parser.parse_args()

    branch1 = args.branch1
    branch2 = args.branch2
    arch = args.arch

    try:
        first_response = get_json_from_api(branch1, arch)
        second_response = get_json_from_api(branch2, arch)
        if first_response and second_response:
            compare_versions = compare_version(first_response, second_response)
            print("Пакеты, которые есть в 1-й, но нет во 2-й:")
            for package_name in get_package_diff(first_response, second_response):
                print(package_name)
            print("\nПакеты, которые есть во 2-й, но нет в 1-й:")
            for package_name in get_package_diff(second_response, first_response):
                print(package_name)
            print("\nПакеты, version которых больше в 1-й, чем во 2-й:")
            for package_name, version_release in compare_versions.items():
                print(f"{package_name}: {version_release}")
        else:
            print("Не удалось получить данные для сравнения.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
