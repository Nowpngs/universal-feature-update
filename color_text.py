class ColorText:
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    END = "\033[0m"

    @staticmethod
    def print_ok_info(text):
        print(f"{ColorText.GREEN}INFO:{ColorText.END} {text}\n")

    @staticmethod
    def color_error(text):
        return f"{ColorText.RED}ERROR:{ColorText.END} {text}\n"
