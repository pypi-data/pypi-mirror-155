from typing import List
import sh
import random
from shutil import which

from lolcatfigletgnuplotprint.utils.data_structures import singleton

from .utils.CommandlinePrinter import CommandlinePrinter
from .utils.strings import chunk_string_by_length
from .utils.types import PrinterAttachment
from .utils.Configuration import Configuration


@singleton
class LolcatFigletPrinter:
    def __init__(self):
        self.___shell_apps = self.___initiailize_shell_apps()
        self.___printer = CommandlinePrinter()

    def print(
        self,
        message: str = None,
        heading_text: str = None,
        description_text: str = None,
        attachements: List[PrinterAttachment] = [],
        priority: int = None,
        output_as_return_value: bool = False,
    ) -> str:

        # Init
        self.___printer.set_output_to_buffer_mode(output_as_return_value)

        #
        # Clear previous view
        #
        self.___printer.clear_screen()

        #
        # Print heading text
        #
        self.___print_heading_text(heading_text=heading_text, priority=priority)

        #
        # Print description text
        #
        self.___print_description_text(description_text=description_text)
        #
        # Print attachments
        #
        self.___print_attachments(attachements=attachements)

        #
        # Print the message
        #
        if message is not None:
            self.___printer.print(message)

        # Print some new lines for end margin
        self.___printer.print("\n" * 2)

        return self.___printer.flush_buffer()

    def ___print_heading_text(self, heading_text: str = None, priority: int = None):
        """Large heading text"""
        if heading_text is not None:

            # Print some new lines for top margin
            self.___printer.print("\n" * 4)

            if "figlet" in self.___shell_apps:
                heading_output = sh.figlet("-ctf", "slant", heading_text)
            else:
                heading_output = str(heading_text).center(50)

            if "lolcat" in self.___shell_apps:
                heading_output = sh.lolcat(heading_output)

            #
            # Print the lolcat figlet message
            #
            if "lolcat" not in self.___shell_apps:
                output_text = str(heading_output)
                if priority is None or priority > 0:
                    figlet_colours = ["aqua", "green", "magenta", "yellow"]
                    figlet_colour = random.choice(figlet_colours)
                else:
                    figlet_colour = "grey"
                self.___printer.print(text=output_text, inline=False, colour=figlet_colour)
            else:
                self.___printer.print(heading_output)

    def ___print_description_text(self, description_text: str = None):
        """Small centered description text"""
        if description_text is not None:
            desc_rows = description_text.split("\n")
            desc_rows_margined = ("\n" + Configuration.view.left_margin_fill).join(desc_rows)
            description_output = (f"{Configuration.view.left_margin_fill}{desc_rows_margined}").center(50)
            self.___printer.print(text=description_output, inline=True, colour="white")
            self.___printer.print("\n")  # 2x new line

    def ___print_attachments(self, attachements: List[PrinterAttachment] = []):
        """list of items, colourfied"""
        if isinstance(attachements, list) and len(attachements) > 0:

            # The first and new messages colour
            firstMessageColour = "green"
            priorityMessageColour = "magenta"
            # The colours of later on messages
            colours = ["yellow", "white", "grey"]

            coloursLength = len(colours) - 1
            colourIndex = 0
            indent = f"{Configuration.view.left_margin_fill}	"

            for responseIndex, responseMessage in enumerate(attachements):
                text_is_bold = False
                text_is_underlined = False

                # Set message block colour
                if "isPriority" in responseMessage and responseMessage["isPriority"]:
                    messageColour = priorityMessageColour
                    text_is_bold = True
                    text_is_underlined = True
                elif responseIndex == 0:
                    messageColour = firstMessageColour
                else:
                    messageColour = colours[colourIndex]
                    if colourIndex < coloursLength:
                        colourIndex = colourIndex + 1

                # Print message parts in chunks divided by length
                messageChunks = chunk_string_by_length(message=responseMessage["message"], length=53)
                for messageChunkIndex, messagePart in enumerate(messageChunks):

                    if messageChunkIndex == 0:
                        # Print sender
                        # .. some indent
                        self.___printer.print(indent, end=" ")
                        # Coloured message part
                        if "senderName" in responseMessage:
                            self.___printer.print(text=responseMessage["senderName"] + " ", inline=True, colour="aqua")
                        # Coloured message part
                        self.___printer.print(
                            text=messagePart,
                            inline=False,
                            colour=messageColour,
                            is_bold=text_is_bold,
                            is_underlined=text_is_underlined,
                        )
                    else:
                        # Coloured message part
                        self.___printer.print(text=indent + " " + messagePart, inline=False, colour=messageColour)

                # 1x new line
                self.___printer.print("")

    def ___initiailize_shell_apps(self):
        shell_apps = []
        for app_name in ["lolcat", "figlet"]:
            app_path = which(app_name)
            if app_path is not None:
                shell_apps.append(app_name)
        return shell_apps
