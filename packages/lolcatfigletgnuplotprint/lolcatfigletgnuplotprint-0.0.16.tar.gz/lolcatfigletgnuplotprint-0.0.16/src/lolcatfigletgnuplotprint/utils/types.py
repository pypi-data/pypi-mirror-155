from typing import List, Optional, TypedDict


class PrinterAttachment(TypedDict):
    isPriority: Optional[bool]
    message: str
    senderName: Optional[str]


class PlotUnit(TypedDict):
    value: float
    timestamp: int


class PlotStat(TypedDict):
    max: float
    min: float
    count: int
    average: float
    sum: float
    max_stamp: int
    min_stamp: int
    newest_stamp: int
    oldest_stamp: int
    has_older_values: bool


class PlotScopeStats(TypedDict):
    scope: PlotStat
    hour: PlotStat
    three_hours: PlotStat
    six_hours: PlotStat
    twelve_hours: PlotStat
    day: PlotStat
    week: PlotStat
    # month: PlotStat
    # year: PlotStat


class PlotPrinterValueGroup(TypedDict):
    title: str
    values: List[PlotUnit]
