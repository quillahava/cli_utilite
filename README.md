# Altbrains

Altbrains stands for "Alt Linux Branches Inspector," a command-line utility and shared library that allows you to compare lists of binary packages from different branches of the Alt Linux distribution repository. . It retrieves package lists from the specified branches, performs a comparison, and generates a JSON report containing three sections:

1. 'packages_only_in_source_branch': A list of packages that exist in the first branch but not in the second branch.
2. 'packages_only_in_target_branch': A list of packages that exist in the second branch but not in the first branch.
3. 'packages_with_higher_version_in_source_branch': A dictionary of packages and their respective versions from the first branch that have higher versions than those in the second branch.

The generated 'response.json' file will be placed in the current working directory. The comparison is based on the package names and their version numbers (after removing letters and special characters). Note that this utility requires an active internet connection to access the Alt Linux repository API.

# Installation Guide for altbrains

This guide will walk you through the installation process for the `altbrains` utility. Before proceeding, please make sure you have the following dependencies installed on your system:

1. **Python**: Ensure that Python 3.6 or higher is installed on your system. If you don't have Python installed, you can download it from the official website: [Python Downloads](https://www.python.org/downloads/).

2. **Poetry**: Install `poetry` by following the instructions on the official website: [Poetry Installation](https://python-poetry.org/docs/#installation).

Once you have Python and Poetry installed, you can proceed with the installation of `altbrains` using the `make` command.

## Step 1: Clone the Repository

Begin by cloning the `altbrains` repository to your local machine:

```bash
git clone git@github.com:quillahava/cli_utilite.git
```

## Step 2: Navigate to the Project Directory

Change your working directory to the root of the cloned repository:

```bash
cd cli_utilite
```

**Note:** `altbrains` can be run directly with the command `python altbrains` from root directory of project.

## Step 3: Create Virtual Environment and Install Dependencies

Run the following `make` command to create a virtual environment and install the necessary dependencies for `altbrains`:

```bash
make shell
```

The above command will create a virtual environment (using `poetry`) and install the required dependencies.

Alternatively, you can create a virtual environment with `pip`:

```bash
python -m venv venv
source venv/bin/activate   # On Windows, use 'venv\Scripts\activate'
pip install -r requirements.txt
```

## Step 4: Install `altbrains`

Next, run the following `make` command to install `altbrains` into the virtual environment:

```bash
make install
```

Alternatively, if you manually created a virtual environment, you can install `altbrains` using `python`:

```bash
python setup.py build
python setup.py install
```

## Step 5: Verify Installation

To confirm that the installation was successful, you can use the following command to get help and see the available options for `altbrains`:

```bash
altbrains -h
```

If the installation was successful, you will see the utility's help information.

## Step 6: Usage

Run the `altbrains` with the desired branch names:

```bash
altbrains sisyphus p10
```

This command will compare the lists of binary packages between the `sisyphus` and `p10` branches, and it will generate the `response.json` file in the current directory.

## Sample Output

After running the command, the `response.json` file will be created with the following structure:
**Warning:** The utility's execution may take several minutes. To reduce waiting time, use the `--arch` flag with the package architecture, e.g., `--arch x86_64`.

```json
{
  "source_branch": "sisyphus",
  "target_branch": "p10",
  "source_packages_count": 1000,
  "target_packages_count": 900,
  "packages_only_in_source_branch": {
    "count": 1,
    "packages": [
      {
        "name": "package1",
        "version": "1.0.0",
        "release": "1"
      }
    ]
  },
  "packages_only_in_target_branch": {
    "count": 1,
    "packages": [
      {
        "name": "package2",
        "version": "2.0.1",
        "release": "2"
      }
    ]
  },
  "packages_with_higher_version_in_source_branch": {
    "count": 1,
    "packages": [
      {
        "name": "package3",
        "version": "2.5.0",
        "release": "3"
      }
    ]
  }
}
```

## Uninstalling `altbrains`

If, for any reason, you want to uninstall `altbrains` from the virtual environment, you can use the following `make` command:

```bash
make uninstall
```

Alternatively, if you manually created a virtual environment, you can uninstall `altbrains` using `pip`:

```bash
pip uninstall altbrains
```

Happy using `altbrains`! 🚀
