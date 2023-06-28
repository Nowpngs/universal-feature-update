import subprocess


class UniversalUpdateFeature:
    project_path = ""

    def __init__(self):
        self.input_path()

    def input_path(self):
        self.project_path = input("Input path of project in you laptop (shinsan or stk):")
        # check if the path to folder existing
        try:
            command = f"cd {self.project_path}"
            subprocess.run([command], check=True)
        except subprocess.CalledProcessError as e:
            raise SystemExit("Process terminated: Path does not exist")

# run the program
UniversalUpdateFeature()