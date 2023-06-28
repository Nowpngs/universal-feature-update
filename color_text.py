class ColorText:
    GREEN = "\033[0;32m"
    END = "\033[0m"

    @staticmethod
    def print_ok_info(text):
        print(f"{ColorText.GREEN}-----{text}-----{ColorText.END}")
