from setuptools import setup, find_packages

setup(
    name="altbrains",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
    ],
    entry_points={
        "console_scripts": [
            "altbrains=altbrains.main:main",
        ],
    },
)
