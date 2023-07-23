from setuptools import setup, find_packages

setup(
    name="cli_utilite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "packaging", "argparse", "pydantic"],
    entry_points={
        "console_scripts": [
            "cli_utilite = cli_utilite.__main__:main",
        ],
    },
    author="quillahava",
    author_email="voyt.to.work@yandex.ru",
    description="CLI utility for comparing lists of binary packages",
    url="https://github.com/quillahava/cli_utilite",
)
