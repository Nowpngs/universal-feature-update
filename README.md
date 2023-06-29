# Universal Feature Update

Universal Feature Update is a tool that allows you to easily cherry-pick features from your own repository or other GitHub repositories for seamless deployment. This tool simplifies the process by leveraging the Openpxyl library to manipulate Excel files and using the provided variables in the `process.py` script.

## Table of Contents

- Installation
- Usage
- Notes
- License
- Credit

## Installation

To use Universal Feature Update, follow the steps below:

1. Clone the repository to your local machine:

```sh
git@github.com:Nowpngs/universal-feature-update.git
```

2. Install [Python](https://www.python.org/downloads/)
3. Install openpyxl via [pip](https://pip.pypa.io/en/stable/installation/):

```sh
pip install openpyxl
```

## Usage

1. Create the folder name `feature_xlsx` in the destination project directory
2. in the `feature_xlsx` folder create the feature name directory and stored the feature.xlsx inside (must be same)
3. Open the `process.py` file in a text editor.
4. Set the following variables in the `process.py` script according to your needs:

   - `destination_project_path`: The input path of the destination project where you want to deploy the feature. Provide the absolute path to the project directory
   - `ssh_key_path`: The input path of the SSH key for the destination project. Provide the absolute path to the SSH key file.
   - `feature_name`: The name of the feature file you want to cherry-pick. This file should be located under `feature_xlsx` folder in destination project.

5. Save the process.py file.
6. Open a terminal and navigate to the root directory of the cloned repository.
7. Run the following command to execute the `process.py` script:

```sh
python3 process.py
```

This will initiate the process of cherry-picking the specified feature and deploying it to the destination project.

Please ensure that you have the necessary permissions and access rights to both the source repository and the destination project before running this tool.

## Notes

- Make sure to provide accurate and valid paths for the `destination_project_path` and `ssh_key_path` variables to ensure successful deployment.
- The `feature_name` should match the name of the feature file located in the `feature_xlsx` in the destination project folder.
- Make sure the excel file and directory folder is the same name as `feature_name`

## License

This project is licensed under the MIT License.
## CreditThis tool was inspired by Jirayu Phongrattananan.