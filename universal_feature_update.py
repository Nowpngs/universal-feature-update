import subprocess
import os
from color_text import ColorText

try:
    from openpyxl.reader.excel import load_workbook
    from openpyxl.styles import PatternFill
except ImportError:
    raise SystemExit(
        "Process terminated: openpyxl module not found. Please make sure it is installed."
    )


class UniversalUpdateFeature:
    destination_project_path = ""
    ssh_key_path = ""
    feature_name = ""
    work_book = None
    remote_repo_name = set()

    def __init__(self, destination_project_path, ssh_key_path, feature_name):
        self.destination_project_path = destination_project_path
        self.ssh_key_path = ssh_key_path
        self.feature_name = feature_name

    def process(self):
        self.load_feature_excel()
        self.check_path()
        self.fetch_destination_origin()
        self.get_remote_repo_name()
        self.fetch_source_origin()
        self.create_new_branch_destination()
        self.process_cherry_pick()
        self.remove_remote_source()
        ColorText.print_ok_info(f"Perfect! Operation Completed!")

    def load_feature_excel(self):
        # load feature excel
        ColorText.print_ok_info(f"Loading Feature {self.feature_name}")
        try:
            self.work_book = load_workbook(
                filename=f"feature_xlsx/{self.feature_name}/{self.feature_name}.xlsx"
            )
        except FileNotFoundError:
            raise SystemExit(ColorText.color_error("Feature excel file not found."))

    def check_path(self):
        ColorText.print_ok_info(
            f"Cheking Destination Path {self.destination_project_path}"
        )
        # check if the path to folder exists
        if not os.path.exists(self.destination_project_path):
            raise SystemExit(ColorText.color_error("Path does not exist"))

        ColorText.print_ok_info(f"Cheking SSH Key Path {self.ssh_key_path}")
        # check if the path to ssh key exists
        if not os.path.exists(self.ssh_key_path):
            raise SystemExit(ColorText.color_error("Path does not exist"))

    def fetch_destination_origin(self):
        ColorText.print_ok_info(f"Fetch Destination Origin")
        # fetch and create new branch on destination project
        try:
            subprocess.run(
                ["ssh-add", self.ssh_key_path],
                check=True,
                cwd=self.destination_project_path,
            )
            subprocess.run(
                ["git", "fetch", "--all"], check=True, cwd=self.destination_project_path
            )
            subprocess.run(
                ["git", "restore", "."], check=True, cwd=self.destination_project_path
            )
            subprocess.run(
                ["git", "branch", "-a"], check=True, cwd=self.destination_project_path
            )

            selected_branch = input("Input Select Branch (Enter for origin/main):")
            if not selected_branch:
                selected_branch = "origin/main"

            subprocess.run(
                ["git", "checkout", selected_branch],
                check=True,
                cwd=self.destination_project_path,
            )
        except subprocess.CalledProcessError:
            raise SystemExit(ColorText.color_error("Fetch and Create branch failed"))

    def get_remote_repo_name(self):
        ColorText.print_ok_info(f"Get Remote Repo From {self.feature_name}.xlsx")
        # get remote repo name
        for row in self.work_book["Sheet1"]["B"]:
            if row.row == 1:
                continue
            self.remote_repo_name.add(row.value)

        if len(self.remote_repo_name) == 0:
            raise SystemExit(
                ColorText.color_error(
                    f"No remote repo name found in {self.feature_name}.xlsx"
                )
            )

    def fetch_source_origin(self):
        ColorText.print_ok_info(f"Fetch Remote Repo")
        # fetch and add remote for the source project
        for index, repo_name in enumerate(self.remote_repo_name):
            try:
                subprocess.run(
                    [
                        "git",
                        "remote",
                        "add",
                        f"source_project_{index}",
                        repo_name,
                    ],
                    check=True,
                    cwd=self.destination_project_path,
                )
                subprocess.run(
                    ["git", "fetch", f"source_project_{index}"],
                    check=True,
                    cwd=self.destination_project_path,
                )
            except subprocess.CalledProcessError:
                self.remove_remote_source()
                raise SystemExit(
                    ColorText.color_error(
                        f"Fetch failed, Repo name: {repo_name} Not Exist"
                    )
                )

    def create_new_branch_destination(self):
        ColorText.print_ok_info(f"Create New Branch {self.feature_name}")
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
                cwd=self.destination_project_path,
            )
        except subprocess.CalledProcessError:
            self.remove_remote_source()
            raise SystemExit(ColorText.color_error("Create branch failed"))

    def process_cherry_pick(self):
        for row in self.work_book["Sheet1"]["C"]:
            print(row.value)

    def remove_remote_source(self):
        # remove remote source
        remote_repo = subprocess.run(
            ["git", "remote"],
            check=True,
            cwd=self.destination_project_path,
            capture_output=True,
            text=True,
        )
        existing_remotes = remote_repo.stdout.strip().split("\n")
        for remote_name in existing_remotes:
            if remote_name != "origin":
                try:
                    ColorText.print_ok_info(f"Remove Remote Source {remote_name}")
                    subprocess.run(
                        [
                            "git",
                            "remote",
                            "remove",
                            remote_name,
                        ],
                        check=True,
                        cwd=self.destination_project_path,
                    )
                except subprocess.CalledProcessError:
                    raise SystemExit(
                        ColorText.color_error(f"Remove remote {remote_name} failed")
                    )
