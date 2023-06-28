import subprocess
import os

try:
    from openpyxl.reader.excel import load_workbook
except ImportError:
    raise SystemExit(
        "Process terminated: openpyxl module not found. Please make sure it is installed."
    )


class UniversalUpdateFeature:
    destination_project_path = ""  # input path of the destination project
    source_project_path = ""  # input path of the source project
    ssh_key_path = ""  # input path of ssh key (codium gitlab)
    feature_name = "" # input feature name from the update_feature folder

    work_book = None
    remote_repo_name = set()

    def __init__(self):
        self.load_feature_excel()
        self.check_path()
        self.fetch_destination_origin()
        self.get_remote_repo_name()
        self.create_new_branch_destination()
        self.fetch_source_origin()
        self.process_cherry_pick()
        self.remove_remote_source()

    def load_feature_excel(self):
        # load feature excel
        try:
            self.work_book = load_workbook(
                filename=f"{self.feature_name}/{self.feature_name}.xlsx"
            )
        except FileNotFoundError:
            raise SystemExit("Process terminated: Feature excel file not found.")

    def get_remote_repo_name(self):
        # get remote repo name
        for row in self.work_book["Sheet1"]["B"]:
            self.remote_repo_name.add(row.value)

        if len(self.remote_repo_name) == 0:
            raise SystemExit("Process terminated: Remote repo name not found.")

    def check_path(self):
        # check if the path to folder exists
        if not os.path.exists(self.destination_project_path):
            raise SystemExit("Process terminated: Path does not exist")

        # check if the path to ssh key exists
        if not os.path.exists(self.ssh_key_path):
            raise SystemExit("Process terminated: Path does not exist")

    def fetch_destination_origin(self):
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
                ["git", "checkout", "origin/main"],
                check=True,
                cwd=self.destination_project_path,
            )
            subprocess.run(
                ["git", "restore", "."], check=True, cwd=self.destination_project_path
            )
        except subprocess.CalledProcessError:
            raise SystemExit("Process terminated: Fetch and Create branch failed")

    def fetch_source_origin(self):
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
                    f"Process terminated: Fetch failed, Repo name: {repo_name} Not Exist"
                )

    def create_new_branch_destination(self):
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
            raise SystemExit("Process terminated: Create branch failed")

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
                        f"Process terminated: Remove remote {remote_name} failed"
                    )


# Run the program
UniversalUpdateFeature()
