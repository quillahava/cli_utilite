# Get info about binary packages from an Alt Linux repository

CLI utility for comparing lists of binary packages. This utility allows you to compare two branches of binary packages from an Alt Linux repository. It retrieves package lists from the specified branches, performs a comparison, and generates a JSON report containing three sections:
1. 'packages_in_branch1': A list of package names that exist in the first branch but not in the second branch.\n\n2. 'packages_in_branch2': A list of package names that exist in the second branch but not in the first branch.
3. 'packages_with_higher_version_in_branch1': A dictionary of package names and their respective versions from the first branch that have higher versions than those in the second branch. 
The generated 'response.json' file will be placed in the current working directory. The comparison is based on the package names and their version numbers (after removing letters and special characters) to ensure accurate results. Note that this utility requires an active internet connection to access the Alt Linux repository API.

# Installation Guide for cli_utilite

This guide will walk you through the installation process for the `cli_utilite` utility. Before proceeding, please make sure you have the following dependencies installed on your system:

1. **Python**: Ensure that Python 3.6 or higher is installed on your system. If you don't have Python installed, you can download it from the official website: [Python Downloads](https://www.python.org/downloads/).

2. **Poetry**: Install `poetry` by following the instructions on the official website: [Poetry Installation](https://python-poetry.org/docs/#installation).

Once you have Python and Poetry installed, you can proceed with the installation of `cli_utilite` using the `make` command.

## Step 1: Clone the Repository

Begin by cloning the `cli_utilite` repository to your local machine:

```bash
git clone git@github.com:quillahava/cli_utilite.git
```

## Step 2: Navigate to the Project Directory

Change your working directory to the root of the cloned repository:

```bash
cd cli_utilite
```

## Step 3: Create Virtual Environment and Install Dependencies

Run the following `make` command to create a virtual environment and install the necessary dependencies for `cli_utilite`:

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

## Step 4: Install `cli_utilite`

Next, run the following `make` command to install `cli_utilite` into the virtual environment:

```bash
make install
```

Alternatively, if you manually created a virtual environment, you can install `cli_utilite` using `python`:

```bash
python setup.py build
python setup.py install
```

## Step 5: Verify Installation

To confirm that the installation was successful, you can use the following command to get help and see the available options for `cli_utilite`:

```bash
cli_utilite -h
```

If the installation was successful, you will see the utility's help information.

## Step 6: Usage

Run the `cli_utilite` with the desired branch names:

```bash
cli_utilite sisyphus p10
```

This command will compare the lists of binary packages between the `sisyphus` and `p10` branches, and it will generate the `response.json` file in the current directory.

## Sample Output

After running the command, the `response.json` file will be created with the following structure:

```json
{
  "packages_in_branch1": ["package1", "package2", "package4"],
  "packages_in_branch2": ["package3", "package5", "package6"],
  "packages_with_higher_version_in_branch1": {
    "package1": "1.2.0",
    "package2": "2.0.1"
  }
}
```

- `packages_in_branch1`: Lists the packages present in the first branch (`sisyphus`).
- `packages_in_branch2`: Lists the packages present in the second branch (`p10`).
- `packages_with_higher_version_in_branch1`: Contains packages that have higher version-release in the first branch (`sisyphus`) compared to the second branch (`p10`).

## Uninstalling `cli_utilite`

If, for any reason, you want to uninstall `cli_utilite` from the virtual environment, you can use the following `make` command:

```bash
make uninstall
```

Alternatively, if you manually created a virtual environment, you can uninstall `cli_utilite` using `pip`:

```bash
pip uninstall cli_utilite
```

That's it! You have successfully installed and verified `cli_utilite`. You can now use the utility to perform the desired tasks. If you encounter any issues during the installation or usage, feel free to reach out for support.

Happy using `cli_utilite`! 🚀
Sure! Below is an example of how to use the `cli_utilite` to compare lists of binary packages from two branches and generate the `response.json` file.
