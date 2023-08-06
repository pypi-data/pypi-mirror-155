from typing import List
import termplotlib as tpl
import datetime
import math

from .utils.CommandlinePrinter import CommandlinePrinter
from .utils.dates import datetime_to_days_hours_minutes, datetime_to_text, get_datetime_now, parse_past_date_text
from .utils.runtime import get_client_public_ip_address
from .utils.types import PlotPrinterValueGroup, PlotScopeStats, PlotUnit, PlotStat


class PlotPrinter:
    def __init__(self):
        datetimeNow = get_datetime_now()
        self.___printer = CommandlinePrinter()
        self.___scopeSeconds = 0
        self.___samplingInterval = 30
        self.___ip_address = get_client_public_ip_address()
        self.___dates = {"app_startup_at": datetimeNow, "now_at": datetimeNow}
        self.___prepend_text_left = "    "

    def print(
        self, value_groups: List[PlotPrinterValueGroup], width=75, height=17, output_as_return_value: bool = False
    ) -> str:
        """
        Prints the history data as a nice xy-plot
        """

        # Init
        self.___printer.set_output_to_buffer_mode(output_as_return_value)
        compinedValues = []

        # Set scope length
        maxValuesLen = 0
        for group in value_groups:
            if len(group["values"]) > maxValuesLen:
                maxValuesLen = len(group["values"])
        self.___scopeSeconds = max((maxValuesLen * self.___samplingInterval) - self.___samplingInterval, 0)

        # Plot
        plot_command_parts = []
        plot_data_parts = []
        fig = tpl.figure(padding=1)

        for group in value_groups:
            title = group["title"]
            x = list(range(0, len(group["values"])))  # @TODO: plot timestamps
            y = list(map(lambda v: v["value"], group["values"]))

            gnuplot_input = []
            for xx, yy in zip(x, y):
                gnuplot_input.append(f"{xx:e} {yy:e}")

            plot_command_parts.append(f"'-' with linespoints title '{title}'")
            plot_data_parts.append("\n".join(gnuplot_input) + "\ne")
            compinedValues.extend(group["values"])

        # Form the gnuplot command string
        extraArgs = []
        extraArgs.append(f"plot {', '.join(plot_command_parts)}")
        extraArgs.extend(plot_data_parts)

        fig.plot(
            [],
            [],
            width=width,
            height=height,
            extra_gnuplot_arguments=extraArgs,
            plot_command="",
        )

        # Draw
        plotDump = fig.get_string()
        plotDump = plotDump.replace("*", "-").replace("A", "*")
        plotDump = plotDump.replace("\n", "\n" + " ")
        self.___printer.print_by_hilighting_char(plotDump, "*", "aqua", "grey")

        # Stats
        stats = self.___get_calculated_plot_stats(compinedValues)
        self.___printFooterStats(stats)
        self.___printAdvFooterStatsLine1(stats)
        self.___printAdvFooterStatsLine2(stats)
        self.___printAdvFooterStatsLine3(stats)
        self.___printAdvFooterStatsLine4(stats)

        return self.___printer.flush_buffer()

    """
	Print some stats
	"""

    def ___printFooterStats(self, stats: PlotScopeStats):

        # Line start
        self.___printer.print(self.___prepend_text_left + " ", end=" ")

        # Hour stats
        self.___printer.print("[", end="")  # Container start
        self.___printer.print(text="Hour:", inline=True, colour="aqua")
        self.___printer.print("Min:" + str(stats["hour"]["min"]), end=" ")
        self.___printer.print("Max:" + str(stats["hour"]["max"]), end=" ")
        self.___printer.print("Avg:" + "%.0f" % stats["hour"]["average"], end="")
        self.___printer.print("]", end=" ")  # Container end

        # Week stats
        self.___printer.print("[", end="")  # Container start
        self.___printer.print(text="Day:", inline=True, colour="aqua")
        self.___printer.print("Min:" + str(stats["day"]["min"]), end=" ")
        self.___printer.print("Max:" + str(stats["day"]["max"]), end=" ")
        self.___printer.print("Avg:" + "%.0f" % stats["day"]["average"], end="")
        self.___printer.print("]", end=" ")  # Container end

        # line break
        self.___printer.print(" ")
        # Line start
        self.___printer.print(self.___prepend_text_left + " ", end=" ")

        # Month stats
        self.___printer.print("[", end="")  # Container start
        self.___printer.print(text="Week:", inline=True, colour="aqua")
        self.___printer.print("Min:" + str(stats["week"]["min"]), end=" ")
        self.___printer.print("Max:" + str(stats["week"]["max"]), end=" ")
        self.___printer.print("Avg:" + "%.0f" % stats["week"]["average"], end="")
        self.___printer.print("]", end=" ")  # Container end

        # Year stats
        self.___printer.print("[", end="")  # Container start
        self.___printer.print(text="Month:", inline=True, colour="aqua")
        self.___printer.print("Min:" + str(stats["month"]["min"]), end=" ")
        self.___printer.print("Max:" + str(stats["month"]["max"]), end=" ")
        self.___printer.print("Avg:" + "%.0f" % stats["month"]["average"], end="")
        self.___printer.print("]", end=" ")  # Container end

        # line break
        self.___printer.print(" ")

    """
	Line one
	"""

    def ___printAdvFooterStatsLine1(self, stats: PlotScopeStats):

        # First line of the footer texts
        footerFirstLineText = self.___prepend_text_left + "  "

        # Scope stats
        footerFirstLineText += "["  # Container start

        footerFirstLineText += "Scope: "
        footerFirstLineText += "Min:" + str(stats["seconds"]["min"]) + " "
        footerFirstLineText += "Max:" + str(stats["seconds"]["max"]) + " "
        footerFirstLineText += "Avg:" + str(stats["seconds"]["average"])

        footerFirstLineText += "] "  # Container end

        # Scope of the plot
        scopeMinutes = self.___scopeSeconds / 60
        if self.___scopeSeconds < 60:
            scopeTimeTotal = str(self.___scopeSeconds) + "s"
        else:
            scopeTimeTotal = "%.0f" % (scopeMinutes) + "min"

        # Scope range
        footerFirstLineText += "["  # Container start
        footerFirstLineText += datetime_to_text(self.___dates["now_at"])
        if self.___scopeSeconds >= 60:
            dateTimeScopeStart = self.___dates["now_at"] - datetime.timedelta(seconds=self.___scopeSeconds)
            footerFirstLineText += " " + dateTimeScopeStart.strftime("%H:%M")
            footerFirstLineText += "→" + self.___dates["now_at"].strftime("%M")
        else:
            footerFirstLineText += " " + self.___dates["now_at"].strftime("%H:%M")

        footerFirstLineText += " (" + scopeTimeTotal + ")"
        footerFirstLineText += "] "  # Container end

        # Print footer line 1
        self.___printer.print(text=footerFirstLineText, inline=False, colour="grey")

    """
	Line two
	"""

    def ___printAdvFooterStatsLine2(self, stats: PlotScopeStats):

        # Second line of the footer texts
        footerSecondLineText = self.___prepend_text_left + "  "

        # Sample rate
        footerSecondLineText += "["  # Container start
        footerSecondLineText += "Sample rate:" + str(self.___samplingInterval) + "s"
        footerSecondLineText += "] "  # Container end

        # Users per second
        footerSecondLineText += "["  # Container start
        if self.___scopeSeconds > 0:
            meanPerSec = stats["seconds"]["sum"] / self.___scopeSeconds
        else:
            meanPerSec = 0

        footerSecondLineText += "Speed:" + "%.2f" % meanPerSec + " u/s"
        footerSecondLineText += "] "  # Container end

        # History peak time
        if stats["month"]["max_stamp"] > 0:
            footerSecondLineText += "["  # Container start
            footerSecondLineText += "HPT: " + datetime_to_text(
                datetime.datetime.fromtimestamp(stats["month"]["max_stamp"])
            )
            footerSecondLineText += "] "  # Container end

        # Print footer line 2
        self.___printer.print(text=footerSecondLineText, inline=False, colour="grey")

    """
	Line three
	"""

    def ___printAdvFooterStatsLine3(self, stats: PlotScopeStats):
        # Third line of the footer texts
        footerThirdLineText = self.___prepend_text_left + "  "

        footerThirdLineText += "["  # Container start
        footerThirdLineText += "Tracker start time: "
        footerThirdLineText += datetime_to_text(self.___dates["app_startup_at"]) + " "

        # the time the app has been running
        runtimeDelta = self.___dates["now_at"] - self.___dates["app_startup_at"]
        days, hours, minutes = datetime_to_days_hours_minutes(runtimeDelta)
        footerThirdLineText += "("
        footerThirdLineText += str(days) + "d, "
        footerThirdLineText += str(hours) + "h, "
        footerThirdLineText += str(minutes) + "m"
        footerThirdLineText += ")"

        footerThirdLineText += "] "  # Container end

        # Print footer line 3
        self.___printer.print(text=footerThirdLineText, inline=False, colour="grey")

    """
	Line four
	"""

    def ___printAdvFooterStatsLine4(self, stats: PlotScopeStats):
        if self.___ip_address is not None:
            # Fourth line of the footer texts
            footerFourthLineText = self.___prepend_text_left + "  "

            footerFourthLineText += "["  # Container start
            footerFourthLineText += "Client IP: "
            footerFourthLineText += self.___ip_address
            footerFourthLineText += "] "  # Container end

            # Print footer line 4
            self.___printer.print(text=footerFourthLineText, inline=False, colour="grey")

    def ___get_calculated_plot_stats(self, values: List[PlotUnit]) -> PlotScopeStats:
        """
        Compiles stats obj
        """

        def calculate_stats(plot_values: List[PlotUnit]) -> PlotStat:

            # Increase counters
            count = len(plot_values)
            summarum = 0
            average = 0
            minimum = 0
            maximum = 0
            min_stamp = 0
            max_stamp = 0

            # Calc average, min and max
            if count > 0:

                for v in plot_values:
                    value = v["value"]
                    summarum += value
                    if value > maximum:
                        maximum = value
                        max_stamp = v["timestamp"]
                    if value < minimum:
                        minimum = value
                        min_stamp = v["timestamp"]
                average = math.ceil(float(summarum / count))

            return {
                "max": maximum,
                "min": minimum,
                "min_stamp": min_stamp,
                "max_stamp": max_stamp,
                "count": count,
                "average": average,
                "sum": summarum,
            }

        return {
            "seconds": calculate_stats(self.___filter_past_plot_values(values, f"{self.___scopeSeconds} secs")),
            "hour": calculate_stats(self.___filter_past_plot_values(values, "1 hour")),
            "day": calculate_stats(self.___filter_past_plot_values(values, "1 day")),
            "week": calculate_stats(self.___filter_past_plot_values(values, "1 week")),
            "month": calculate_stats(self.___filter_past_plot_values(values, "1 month")),
            "year": calculate_stats(self.___filter_past_plot_values(values, "1 year")),
        }

    def ___filter_past_plot_values(self, values: List[PlotUnit], past_time_text: str) -> List[PlotUnit]:
        return list(
            filter(
                lambda v: v["timestamp"]
                >= datetime.datetime.timestamp(datetime.datetime.fromisoformat(parse_past_date_text(past_time_text))),
                values,
            )
        )
