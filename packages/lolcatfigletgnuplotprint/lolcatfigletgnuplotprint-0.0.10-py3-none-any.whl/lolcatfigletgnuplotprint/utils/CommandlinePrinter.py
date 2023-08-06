import sh
import sys


class CommandlinePrinter:
    ___buffer = ""
    ___output_to_buffer_mode = False

    ___bcolours = {
        "white": "\033[37m",
        "aqua": "\033[36m",
        "magenta": "\033[35m",
        "blue": "\033[34m",
        "yellow": "\033[33m",
        "green": "\033[32m",
        "orange": "\033[33m",
        "red": "\033[31m",
        "grey": "\033[30;1m",
        "black": "\033[30m",
        "default": "\033[39m",
        "unkown": "\033[30;1m",
        "END_COLOUR": "\033[39m",
        "START_BOLD_STYLE": "\033[1m",
        "START_UNDERLINE_STYLE": "\033[4m",
        "END_STYLE": "\033[0m",
    }

    def clear_screen(self, message: str = None):
        self.print(sh.clear())
        if message is not None:
            self.print(message)

    def get_colour(self, colour):
        """
        Get the escape code sequence for a colour
        """
        return self.___bcolours.get(colour, self.___bcolours["END_COLOUR"])

    def wrap_text_with_colour(self, text: str, colour: str):
        return f"{self.get_colour(colour)}{text}{self.get_colour('END_COLOUR')}"

    def get_text_output(self, text, inline=False, colour=None, is_bold=False, is_underlined=False, end="\n") -> str:
        """
        Forms the text output
        """
        if colour is None:
            colour = self.get_colour("END_COLOUR")

        if inline:
            end = ""

        if is_bold:
            text = f"{self.get_colour('START_BOLD_STYLE')}{text}{self.get_colour('END_STYLE')}"

        if is_underlined:
            text = f"{self.get_colour('START_UNDERLINE_STYLE')}{text}{self.get_colour('END_STYLE')}"

        return f"{self.get_colour(colour)}{text}{self.get_colour('END_COLOUR')}{end}"

    def print(self, text, inline=False, colour=None, is_bold=False, is_underlined=False, end="\n"):
        """
        Prints to buffer
        """
        text_output = self.get_text_output(text, inline, colour, is_bold, is_underlined, end)
        self.___write(text_output)

    def print_by_hilighting_char(self, text, character, colour, bgColour="default"):
        bgColour = self.get_colour(bgColour)

        lines = text.split("\n")
        for line in lines:
            lineParts = line.split(character)
            i = 0
            c = len(lineParts)
            for linePart in lineParts:
                i = i + 1
                self.___write(bgColour + linePart + self.get_colour("END_COLOUR"))
                if i < c:
                    self.___write(self.get_colour(colour) + character + self.get_colour("END_COLOUR"))
            self.___write("\n")

    def set_output_to_buffer_mode(self, is_enabled: bool):
        self.___output_to_buffer_mode = is_enabled

    def flush_buffer(self):
        buffer = self.___buffer
        self.___buffer = ""
        return buffer

    def ___write(self, data: str):
        self.___buffer += data

        if not self.___output_to_buffer_mode:
            sys.stdout.write(data)
