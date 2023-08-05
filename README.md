# Altbrains

Altbrains stands for "Alt Linux Branches Inspector," a command-line utility and shared library that allows you to compare lists of binary packages from different branches of the Alt Linux distribution repository. . It retrieves package lists from the specified branches, performs a comparison, and generates a JSON report containing three sections:

1. 'packages_only_in_source_branch': A list of packages that exist in the first branch but not in the second branch.
2. 'packages_only_in_target_branch': A list of packages that exist in the second branch but not in the first branch.
3. 'packages_with_higher_version_in_source_branch': A dictionary of packages and their respective versions from the first branch that have higher versions than those in the second branch.

The generated 'response.json' file will be placed in the current working directory. The comparison is based on the package names and their version numbers (after removing letters and special characters). Note that this utility requires an active internet connection to access the Alt Linux repository API.

## Installation Guide for altbrains

This guide will walk you through the installation process for the `altbrains` utility. Before proceeding, please make sure you have the following dependencies installed on your system:

1. **python3**
2. **make** 


## Step 1: Clone the Repository

Begin by cloning the `altbrains` repository to your local machine:

```bash
git clone https://github.com/quillahava/cli_utilite.git
```

## Step 2: Navigate to the Project Directory

Change your working directory to the root of the cloned repository:

```bash
cd cli_utilite
```

**Note:** `altbrains` can be run directly with the command `python altbrains` from the root directory of the project.

## Step 3: Install `altbrains`

Run the following `make` command to install `altbrains` (administrative privileges may be required):

```bash
sudo make install
```

This will install `altbrains` into your system.

## Step 4: Verify Installation

To confirm that the installation was successful, you can use the following command to get help and see the available options for `altbrains`:

```bash
altbrains -h
```

If the installation was successful, you will see the utility's help information.
## Step 5: Usage

Run the `altbrains` with the desired branch names:

```bash
altbrains sisyphus p10 --arch x86_64
```

This command will compare the lists of binary packages between the `sisyphus` and `p10` branches with `x86_64` architecture, and it will generate the `response.json` file in the current directory.

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

If, you want to uninstall `altbrains`, you can use the following `make` command:

```bash
make uninstall
```

Now you have `altbrains` installed and ready to use. You can run it with desired branch names to compare lists of binary packages between different branches of the Alt Linux distribution repository.


If you encounter any issues or have further questions, feel free to reach out. Happy using `altbrains`! 🚀appy using `altbrains`! 🚀
