from typing import List
import termplotlib as tpl
import datetime
import math

from lolcatfigletgnuplotprint.utils.data_structures import singleton
from lolcatfigletgnuplotprint.utils.transformations import chunk_list

from .utils.CommandlinePrinter import CommandlinePrinter
from .utils.dates import (
    datetime_to_days_hours_minutes,
    datetime_to_text,
    get_datetime_now,
    get_timestamp_ago,
)
from .utils.runtime import get_client_public_ip_address
from .utils.types import PlotPrinterValueGroup, PlotScopeStats, PlotUnit, PlotStat
from .utils.Configuration import Configuration


@singleton
class PlotPrinter:
    ___max_scope_points: int  # How many plot points plots

    def __init__(self):
        datetimeNow = get_datetime_now()
        self.___printer = CommandlinePrinter()
        self.___ip_address = None
        if Configuration.plotter.show_ip_address:
            self.___ip_address = get_client_public_ip_address()

        self.___dates = {"app_startup_at": datetimeNow, "now_at": datetimeNow}

    def print(
        self,
        value_groups: List[PlotPrinterValueGroup],
        width=75,
        height=19,
        output_only_as_return_value: bool = False,
        max_scope_points: int = 30,
    ) -> str:
        """
        Prints the history data as a nice xy-plot
        """

        # Init
        self.___dates["now_at"] = get_datetime_now()
        self.___printer.set_output_to_buffer_mode(output_only_as_return_value)
        self.___max_scope_points = max_scope_points
        compinedValues = []

        # Plot
        plot_command_parts = []
        plot_data_parts = []
        fig = tpl.figure(padding=1)

        for group in value_groups:
            # Grap actual all input values for stats
            compinedValues.extend(group["values"])

            # Limit scope size
            targeted_plot_values = group["values"][-self.___max_scope_points :]

            # Make axis
            x = list(range(0, len(targeted_plot_values)))  # @TODO: plot timestamps on x-tics
            y = list(map(lambda v: v["value"], targeted_plot_values))

            gnuplot_input = []
            for xx, yy in zip(x, y):
                gnuplot_input.append(f"{xx:e} {yy:e}")

            plot_command_parts.append(f"'-' with linespoints title '{group['title']}'")
            plot_data_parts.append("\n".join(gnuplot_input) + "\ne")

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

        #
        # Stats
        #
        stats = self.___get_calculated_plot_stats(compinedValues)

        # Print stats
        had_output = self.___print_scope_history_stats(stats)
        self.___print_scope_stats(stats, colour="grey" if had_output else "aqua")

        # Extra info
        self.___print_adv_footer_stats_line1(stats)
        self.___print_adv_footer_stats_line2(stats)
        self.___print_adv_footer_stats_line3(stats)

        return self.___printer.flush_buffer()

    def ___print_scope_history_stats(self, stats: PlotScopeStats) -> bool:
        """
        Print some stats
        """

        def get_stat_container(stat_name: str, stats: PlotScopeStats = None) -> str:

            stat = stats[stat_name] if stats is not None else {"min": 0, "max": 0, "average": 0}
            label_colour = "aqua" if stats is not None else "gray"

            stat_line = ""
            stat_line += self.___printer.print("[", end="", output_only_as_return_value=True)  # Container start
            stat_line += self.___printer.print(
                text=f"{stat_name.replace('_', ' ').capitalize()}:",
                inline=True,
                colour=label_colour,
                output_only_as_return_value=True,
            )
            stat_line += self.___printer.print("Min:" + str(stat["min"]), end=" ", output_only_as_return_value=True)
            stat_line += self.___printer.print("Max:" + str(stat["max"]), end=" ", output_only_as_return_value=True)
            stat_line += self.___printer.print(
                "Avg:" + "%.0f" % stat["average"], end="", output_only_as_return_value=True
            )
            stat_line += self.___printer.print("]", end=" ", output_only_as_return_value=True)  # Container end
            return stat_line

        stat_lines = []
        scope_groups = [
            ("hour", "three_hours"),
            ("six_hours", "twelve_hours"),
            ("day", "week"),
        ]

        for scope_group in scope_groups:
            scopeA, scopeB = scope_group
            if stats[scopeA]["has_older_values"]:
                stat_lines.append(get_stat_container(scopeA, stats))
                if stats[scopeB]["has_older_values"]:
                    stat_lines.append(get_stat_container(scopeB, stats))
                else:
                    stat_lines.append(get_stat_container(scopeB))

        line_groups = chunk_list(stat_lines, 2)

        for line_group in line_groups:
            self.___printer.print(Configuration.view.left_margin_fill + " ", end=" ")
            self.___printer.print(" ".join(line_group))

        return len(line_groups) > 0

    def ___print_scope_stats(self, stats: PlotScopeStats, colour: str):
        """
        Line one
        """

        # First line of the footer texts
        footerFirstLineText = Configuration.view.left_margin_fill + "  "

        # Scope stats
        footerFirstLineText += "["  # Container start

        footerFirstLineText += "Scope: "
        footerFirstLineText += "Min:" + str(stats["scope"]["min"]) + " "
        footerFirstLineText += "Max:" + str(stats["scope"]["max"]) + " "
        footerFirstLineText += "Avg:" + str(stats["scope"]["average"])

        footerFirstLineText += "] "  # Container end

        # Scope of the plot
        scopeSeconds = self.___get_scope_seconds(stats)
        scopeMinutes = scopeSeconds / 60
        if scopeSeconds < 60:
            scopeTimeTotal = str(scopeSeconds) + "s"
        else:
            scopeTimeTotal = "%.0f" % (scopeMinutes) + "min"

        # Scope range
        footerFirstLineText += "["  # Container start
        footerFirstLineText += datetime_to_text(self.___dates["now_at"])
        if scopeSeconds >= 60:
            dateTimeScopeStart = self.___dates["now_at"] - datetime.timedelta(seconds=scopeSeconds)
            footerFirstLineText += " " + dateTimeScopeStart.strftime("%H:%M")
            footerFirstLineText += "→" + self.___dates["now_at"].strftime("%M")
        else:
            footerFirstLineText += " " + self.___dates["now_at"].strftime("%H:%M")

        footerFirstLineText += " (" + scopeTimeTotal + ")"
        footerFirstLineText += "] "  # Container end

        # Print footer line 1
        self.___printer.print(text=footerFirstLineText, inline=False, colour=colour)

    def ___print_adv_footer_stats_line1(self, stats: PlotScopeStats):
        """
        Line two
        """

        if Configuration.plotter.show_scope_extra_info_line:

            # Second line of the footer texts
            footerSecondLineText = Configuration.view.left_margin_fill + "  "

            # Sample rate
            footerSecondLineText += "["  # Container start
            footerSecondLineText += "Sample rate:" + str(self.___max_scope_points) + "p"
            footerSecondLineText += "] "  # Container end

            # Users per second
            scopeSeconds = self.___get_scope_seconds(stats)
            footerSecondLineText += "["  # Container start
            if scopeSeconds > 0:
                meanPerSec = stats["seconds"]["sum"] / scopeSeconds
            else:
                meanPerSec = 0

            footerSecondLineText += "Speed:" + "%.2f" % meanPerSec + " u/s"
            footerSecondLineText += "] "  # Container end

            # History peak time
            if stats["month"]["max_at_stamp"] > 0:
                footerSecondLineText += "["  # Container start
                footerSecondLineText += "HPT: " + datetime_to_text(
                    datetime.datetime.fromtimestamp(stats["month"]["max_at_stamp"])
                )
                footerSecondLineText += "] "  # Container end

            # Print footer line 2
            self.___printer.print(text=footerSecondLineText, inline=False, colour="grey")

    def ___print_adv_footer_stats_line2(self, stats: PlotScopeStats):
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

    def ___print_adv_footer_stats_line3(self, stats: PlotScopeStats):
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

        def calculate_stats(filtered_plot_values: List[PlotUnit], all_values: List[PlotUnit]) -> PlotStat:

            # Increase counters
            count = len(filtered_plot_values)
            summarum = 0
            average = 0
            minimum = None
            maximum = None
            min_at_stamp = 0
            max_at_stamp = 0
            newest_stamp = 0
            oldest_stamp = 0

            # Calc average, min and max
            if count > 0:
                for v in filtered_plot_values:
                    value = v["value"]
                    summarum += value
                    if maximum is None or value > maximum:
                        maximum = value
                        max_at_stamp = v["timestamp"]
                    if minimum is None or value < minimum:
                        minimum = value
                        min_at_stamp = v["timestamp"]

                    if newest_stamp == 0 or newest_stamp <= v["timestamp"]:
                        newest_stamp = v["timestamp"]
                    if oldest_stamp == 0 or oldest_stamp >= v["timestamp"]:
                        oldest_stamp = v["timestamp"]
                average = math.ceil(float(summarum / count))

            return {
                "max": maximum if maximum is not None else 0,
                "min": minimum if minimum is not None else 0,
                "min_at_stamp": min_at_stamp,
                "max_at_stamp": max_at_stamp,
                "count": count,
                "average": average,
                "sum": summarum,
                "newest_stamp": newest_stamp,
                "oldest_stamp": oldest_stamp,
                "has_older_values": count < len(all_values),
            }

        scope_values = current_values[-self.___max_scope_points :]
        week_values = self.___filter_past_plot_values(current_values, days=7)
        day_values = self.___filter_past_plot_values(week_values, days=1)
        twelve_hours_values = self.___filter_past_plot_values(day_values, hours=12)
        six_hours_values = self.___filter_past_plot_values(twelve_hours_values, hours=6)
        three_hours_values = self.___filter_past_plot_values(six_hours_values, hours=3)
        hour_values = self.___filter_past_plot_values(three_hours_values, hours=1)

        return {
            "scope": calculate_stats(scope_values, current_values),
            "week": calculate_stats(week_values, current_values),
            "day": calculate_stats(day_values, current_values),
            "twelve_hours": calculate_stats(twelve_hours_values, current_values),
            "six_hours": calculate_stats(six_hours_values, current_values),
            "three_hours": calculate_stats(three_hours_values, current_values),
            "hour": calculate_stats(hour_values, current_values),
        }

    def ___filter_past_plot_values(
        self, values: List[PlotUnit], days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0
    ) -> List[PlotUnit]:
        return list(
            filter(
                lambda v: v["timestamp"] >= get_timestamp_ago(days, hours, minutes, seconds),
                values,
            )
        )

    def ___get_scope_seconds(self, stats: PlotScopeStats) -> int:
        return int(stats["scope"]["newest_stamp"]) - int(stats["scope"]["oldest_stamp"])
