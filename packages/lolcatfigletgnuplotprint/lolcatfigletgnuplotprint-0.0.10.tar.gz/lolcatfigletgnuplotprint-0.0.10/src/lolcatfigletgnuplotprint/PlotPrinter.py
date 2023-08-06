from typing import List
import termplotlib as tpl
import datetime
import math

from lolcatfigletgnuplotprint.utils.data_structures import singleton

from .utils.CommandlinePrinter import CommandlinePrinter
from .utils.dates import datetime_to_days_hours_minutes, datetime_to_text, get_datetime_now, parse_past_date_text
from .utils.runtime import get_client_public_ip_address
from .utils.types import PlotPrinterValueGroup, PlotScopeStats, PlotUnit, PlotStat
from .utils.Configuration import Configuration


@singleton
class PlotPrinter:
    def __init__(self):
        datetimeNow = get_datetime_now()
        self.___printer = CommandlinePrinter()
        self.___scopeSeconds = 0
        self.___samplingInterval = 30
        self.___previous_stats = None

        self.___ip_address = None
        if Configuration.plotter.show_ip_address:
            self.___ip_address = get_client_public_ip_address()

        self.___dates = {"app_startup_at": datetimeNow, "now_at": datetimeNow}

    def print(
        self,
        value_groups: List[PlotPrinterValueGroup],
        width=75,
        height=19,
        output_as_return_value: bool = False,
    ) -> str:
        """
        Prints the history data as a nice xy-plot
        """

        # Init
        self.___dates["now_at"] = get_datetime_now()
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
            x = list(range(0, len(group["values"])))  # @TODO: plot timestamps on x-tics
            y = list(map(lambda v: v["value"], group["values"]))

            gnuplot_input = []
            for xx, yy in zip(x, y):
                gnuplot_input.append(f"{xx:e} {yy:e}")

            plot_command_parts.append(f"'-' with linespoints title '{title}'")
            plot_data_parts.append("\n".join(gnuplot_input) + "\ne")
            compinedValues.extend(group["values"])

        # Form the gnuplot command string
        extraArgs = []
        extraArgs.append("unset xtics")  # @TODO: plot timestamps on x-tics
        # extraArgs.append("unset autoscale x")
        extraArgs.append(f"plot {', '.join(plot_command_parts)}")
        extraArgs.extend(plot_data_parts)

        fig.plot([], [], width=width, height=height, extra_gnuplot_arguments=extraArgs, plot_command="", ticks_scale=1)

        # Draw
        plotDump = fig.get_string()

        # Stylify primary plot line
        plotDump = plotDump.replace("*", self.___printer.wrap_text_with_colour(text="-", colour="aqua"))
        plotDump = plotDump.replace("A", self.___printer.wrap_text_with_colour(text="*", colour="aqua"))

        # Stylify secondary plot line
        plotDump = plotDump.replace("#", self.___printer.wrap_text_with_colour(text="-", colour="grey"))
        plotDump = plotDump.replace("B", self.___printer.wrap_text_with_colour(text="x", colour="grey"))

        # add a plot margin-left
        plotDump = plotDump.replace("\n", "\n" + " ")

        self.___printer.print(plotDump)

        # Stats
        stats = self.___get_calculated_plot_stats(compinedValues)

        self.___printFooterStats(stats)
        self.___printAdvFooterStatsLine1(stats)
        self.___printAdvFooterStatsLine2(stats)
        self.___printAdvFooterStatsLine3(stats)
        self.___printAdvFooterStatsLine4(stats)

        return self.___printer.flush_buffer()

    def ___printFooterStats(self, stats: PlotScopeStats):
        """
        Print some stats
        """

        # Line start
        self.___printer.print(Configuration.view.left_margin_fill + " ", end=" ")

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
        self.___printer.print(Configuration.view.left_margin_fill + " ", end=" ")

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

    def ___printAdvFooterStatsLine1(self, stats: PlotScopeStats):
        """
        Line one
        """

        # First line of the footer texts
        footerFirstLineText = Configuration.view.left_margin_fill + "  "

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

    def ___printAdvFooterStatsLine2(self, stats: PlotScopeStats):
        """
        Line two
        """

        if Configuration.plotter.show_scope_extra_info_line:

            # Second line of the footer texts
            footerSecondLineText = Configuration.view.left_margin_fill + "  "

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

    def ___printAdvFooterStatsLine3(self, stats: PlotScopeStats):
        """
        Line three
        """
        # Third line of the footer texts
        footerThirdLineText = Configuration.view.left_margin_fill + "  "

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

    def ___printAdvFooterStatsLine4(self, stats: PlotScopeStats):
        """
        Line four
        """
        if Configuration.plotter.show_ip_address and self.___ip_address is not None:
            # Fourth line of the footer texts
            footerFourthLineText = Configuration.view.left_margin_fill + "  "

            footerFourthLineText += "["  # Container start
            footerFourthLineText += "Client IP: "
            footerFourthLineText += self.___ip_address
            footerFourthLineText += "] "  # Container end

            # Print footer line 4
            self.___printer.print(text=footerFourthLineText, inline=False, colour="grey")

    def ___get_calculated_plot_stats(self, current_values: List[PlotUnit]) -> PlotScopeStats:
        """
        Compiles stats obj
        """

        def calculate_stats(stats_name: str, previous_stats: PlotScopeStats, plot_values: List[PlotUnit]) -> PlotStat:

            # Increase counters
            count = len(plot_values)
            summarum = 0
            average = 0
            minimum = None
            maximum = None
            min_stamp = 0
            max_stamp = 0

            if isinstance(previous_stats, dict) and stats_name in previous_stats:
                minimum = previous_stats[stats_name]["min"]
                maximum = previous_stats[stats_name]["max"]
                min_stamp = previous_stats[stats_name]["min_stamp"]
                max_stamp = previous_stats[stats_name]["max_stamp"]

            # Calc average, min and max
            if count > 0:

                for v in plot_values:
                    value = v["value"]
                    summarum += value
                    if maximum is None or value > maximum:
                        maximum = value
                        max_stamp = v["timestamp"]
                    if minimum is None or value < minimum:
                        minimum = value
                        min_stamp = v["timestamp"]
                average = math.ceil(float(summarum / count))

            return {
                "max": maximum if maximum is not None else 0,
                "min": minimum if minimum is not None else 0,
                "min_stamp": min_stamp,
                "max_stamp": max_stamp,
                "count": count,
                "average": average,
                "sum": summarum,
            }

        stats = {
            "seconds": calculate_stats(
                "seconds",
                self.___previous_stats,
                self.___filter_past_plot_values(current_values, f"{self.___scopeSeconds} secs"),
            ),
            "hour": calculate_stats(
                "hour", self.___previous_stats, self.___filter_past_plot_values(current_values, "1 hour")
            ),
            "day": calculate_stats(
                "day", self.___previous_stats, self.___filter_past_plot_values(current_values, "1 day")
            ),
            "week": calculate_stats(
                "week", self.___previous_stats, self.___filter_past_plot_values(current_values, "1 week")
            ),
            "month": calculate_stats(
                "month", self.___previous_stats, self.___filter_past_plot_values(current_values, "1 month")
            ),
            "year": calculate_stats(
                "year", self.___previous_stats, self.___filter_past_plot_values(current_values, "1 year")
            ),
        }

        self.___previous_stats = stats
        return stats

    def ___filter_past_plot_values(self, values: List[PlotUnit], past_time_text: str) -> List[PlotUnit]:
        return list(
            filter(
                lambda v: v["timestamp"]
                >= datetime.datetime.timestamp(datetime.datetime.fromisoformat(parse_past_date_text(past_time_text))),
                values,
            )
        )
