from typing import List

from .utils.types import PlotPrinterValueGroup, PlotScopeStats, PrinterAttachment
from .utils.dates import get_datetime_now


def print_example():

    heading_text = "Heading text"
    description_text = "Description text"
    attachements = [
        {"message": "attachment one"},
        {"message": "attachment two"},
        {"message": "attachment three, a priority message", "isPriority": True},
        {"message": "attachment four"},
        {"message": "attachment five"},
        {"message": "attachment six"},
    ]

    timestampNow = get_datetime_now().timestamp()

    message = plot_print(
        value_groups=[
            {
                "title": "Data 1",
                "values": [
                    {"value": 1, "timestamp": timestampNow},
                    {"value": 5, "timestamp": timestampNow + 5},
                    {"value": 2, "timestamp": timestampNow + 15},
                ],
            },
            {
                "title": "Data 2",
                "values": [
                    {"value": 7, "timestamp": timestampNow},
                    {"value": 3, "timestamp": timestampNow + 5},
                    {"value": 5, "timestamp": timestampNow + 15},
                ],
            },
        ],
        output_only_as_return_value=True,
    )

    lolcat_figlet_print(
        message=message,
        heading_text=heading_text,
        description_text=description_text,
        attachements=attachements,
    )


def plot_print(
    value_groups: List[PlotPrinterValueGroup],
    width=75,
    height=17,
    output_only_as_return_value: bool = False,
    sample_interval_secs: int = 60,
) -> str:
    from .PlotPrinter import PlotPrinter

    """
    Prints xy-plot
    """
    return PlotPrinter().print(
        value_groups=value_groups,
        width=width,
        height=height,
        output_only_as_return_value=output_only_as_return_value,
        sample_interval_secs=sample_interval_secs,
    )


def lolcat_figlet_print(
    message: str = None,
    heading_text: str = None,
    description_text: str = None,
    attachements: List[PrinterAttachment] = [],
    priority: int = None,
    output_only_as_return_value: bool = False,
    print_vertical_margins: bool = True,
) -> str:
    from .LolcatFigletPrinter import LolcatFigletPrinter

    """
    Prints texts with a fancy look
    """
    return LolcatFigletPrinter().print(
        message=message,
        heading_text=heading_text,
        description_text=description_text,
        attachements=attachements,
        priority=priority,
        output_only_as_return_value=output_only_as_return_value,
        print_vertical_margins=print_vertical_margins,
    )


def clear_screen(message: str = None):
    from .utils.CommandlinePrinter import CommandlinePrinter

    """
    Clears terminal screen
    """
    CommandlinePrinter().clear_screen(message)
