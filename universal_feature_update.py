import subprocess
import os

try:
    from openpyxl.reader.excel import load_workbook
except ImportError:
    raise SystemExit(
        "Process terminated: openpyxl module not found. Please make sure it is installed."
    )


class UniversalUpdateFeature:
    project_path = ""  # unput path of project in your laptop (shinsan or stk)
    ssh_key_path = ""  # input path of ssh key (codium gitlab)
    feature_name = ""  # input feature name from the update_feature folder

    work_book = None

    def __init__(self):
        self.load_feature_excel()
        self.check_path()
        self.fetch_origin()
        self.create_new_branch()

    def load_feature_excel(self):
        # load feature excel
        try:
            self.work_book = load_workbook(
                filename=f"{self.feature_name}/{self.feature_name}.xlsx"
            )
        except FileNotFoundError:
            raise SystemExit("Process terminated: Feature excel file not found.")

    def check_path(self):
        # check if the path to folder exists
        if not os.path.exists(self.project_path):
            raise SystemExit("Process terminated: Path does not exist")

        # check if the path to ssh key exists
        if not os.path.exists(self.ssh_key_path):
            raise SystemExit("Process terminated: Path does not exist")

    def fetch_origin(self):
        # fetch and create new branch
        try:
            subprocess.run(
                ["ssh-add", self.ssh_key_path], check=True, cwd=self.project_path
            )
            subprocess.run(["git", "fetch", "--all"], check=True, cwd=self.project_path)
            subprocess.run(
                ["git", "checkout", "origin/main"], check=True, cwd=self.project_path
            )
            subprocess.run(["git", "restore", "."], check=True, cwd=self.project_path)
        except subprocess.CalledProcessError:
            raise SystemExit("Process terminated: Fetch and Create branch failed")

    def create_new_branch(self):
        # create new branch
        try:
            subprocess.run(
                [
                    "git",
                    "switch",
                    "-c",
                    self.feature_name,
                ],
                check=True,
                cwd=self.project_path,
            )
        except subprocess.CalledProcessError:
            raise SystemExit("Process terminated: Create branch failed")


# Run the program
UniversalUpdateFeature()
