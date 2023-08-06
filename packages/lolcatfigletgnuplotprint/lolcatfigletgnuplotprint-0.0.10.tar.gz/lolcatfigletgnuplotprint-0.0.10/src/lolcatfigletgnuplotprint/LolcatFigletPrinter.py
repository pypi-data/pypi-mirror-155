from typing import List
import sh
import random

from lolcatfigletgnuplotprint.utils.data_structures import singleton
from lolcatfigletgnuplotprint.utils.runtime import check_shell_apps_installed

from .utils.CommandlinePrinter import CommandlinePrinter
from .utils.strings import chunk_string_by_length
from .utils.types import PrinterAttachment
from .utils.Configuration import Configuration


@singleton
class LolcatFigletPrinter:
    def __init__(self):
        self.___shell_apps_installed = check_shell_apps_installed(["lolcat", "figlet"])
        self.___printer = CommandlinePrinter()

    def print(
        self,
        message: str = None,
        heading_text: str = None,
        description_text: str = None,
        attachements: List[PrinterAttachment] = [],
        priority: int = None,
        output_as_return_value: bool = False,
        print_vertical_margins: bool = True,
    ) -> str:
        """The out-putter, swinger"""
        # Init
        self.___printer.set_output_to_buffer_mode(output_as_return_value)

        #
        # Clear previous view
        #
        self.___printer.clear_screen()

        #
        # Print heading text
        #
        heading = self.___form_heading_text(heading_text=heading_text, priority=priority)
        if heading is not None:
            if print_vertical_margins:
                # Print some new lines for top margin
                self.___printer.print("\n" * 4)
            self.___printer.print(heading)
        #
        # Print description text
        #
        description = self.___form_description_text(description_text=description_text)
        if description is not None:
            self.___printer.print(description)
            if print_vertical_margins:
                self.___printer.print("\n")  # 2x new line

        #
        # Print attachments
        #
        attachments_text = self.___form_attachments_text(attachements=attachements)
        if attachments_text is not None:
            self.___printer.print(attachments_text)

        #
        # Print the message
        #
        if message is not None:
            self.___printer.print(message)

        if print_vertical_margins:
            # Print some new lines for end margin
            self.___printer.print("\n" * 2)

        return self.___printer.flush_buffer()

    def ___form_heading_text(self, heading_text: str = None, priority: int = None) -> str:
        """Large heading text"""
        text_output = None
        if heading_text is not None:
            if "figlet" in self.___shell_apps_installed:
                heading_output = sh.figlet("-ctf", "slant", heading_text)
            else:
                heading_output = str(heading_text).center(50)

            if "lolcat" in self.___shell_apps_installed:
                heading_output = sh.lolcat(heading_output)

            #
            # Print the lolcat figlet message
            #
            if "lolcat" not in self.___shell_apps_installed:
                output_text = str(heading_output)
                if priority is None or priority > 0:
                    figlet_colours = ["aqua", "green", "magenta", "yellow"]
                    figlet_colour = random.choice(figlet_colours)
                else:
                    figlet_colour = "grey"
                text_output = self.___printer.get_text_output(text=output_text, inline=False, colour=figlet_colour)
            else:
                text_output = self.___printer.get_text_output(heading_output)

        return text_output

    def ___form_description_text(self, description_text: str = None) -> str:
        """Small centered description text"""
        text_output = None
        if description_text is not None:
            desc_rows = description_text.split("\n")
            desc_rows_margined = ("\n" + Configuration.view.left_margin_fill).join(desc_rows)
            description_output = (f"{Configuration.view.left_margin_fill}{desc_rows_margined}").center(50)
            text_output = self.___printer.get_text_output(text=description_output, inline=True, colour="white")
        return text_output

    def ___form_attachments_text(self, attachements: List[PrinterAttachment] = []) -> str:
        text_output = None

        """list of items, colourfied"""
        if isinstance(attachements, list) and len(attachements) > 0:
            text_output = ""

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
                        text_output += self.___printer.get_text_output(indent, end=" ")
                        # Coloured message part
                        if "senderName" in responseMessage:
                            text_output += self.___printer.get_text_output(
                                text=responseMessage["senderName"] + " ", inline=True, colour="aqua"
                            )
                        # Coloured message part
                        text_output += self.___printer.get_text_output(
                            text=messagePart,
                            inline=False,
                            colour=messageColour,
                            is_bold=text_is_bold,
                            is_underlined=text_is_underlined,
                        )
                    else:
                        # Coloured message part
                        text_output += self.___printer.get_text_output(
                            text=indent + " " + messagePart, inline=False, colour=messageColour
                        )

                # 1x new line
                text_output += self.___printer.get_text_output("")

        return text_output
