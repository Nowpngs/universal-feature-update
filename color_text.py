class ColorText:
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    YELLOW = "\033[0;33m"
    END = "\033[0m"

    @staticmethod
    def print_ok_info(text):
        print(f"\n{ColorText.GREEN}INFO:{ColorText.END} {text}")

    @staticmethod
    def print_warning_info(text):
        print(f"\n{ColorText.YELLOW}WARNING:{ColorText.END} {text}")

    @staticmethod
    def color_error(text):
        return f"\n{ColorText.RED}ERROR:{ColorText.END} {text}"

    @staticmethod
    def color_warning(text):
        return f"\n{ColorText.YELLOW}WARNING:{ColorText.END} {text}"
