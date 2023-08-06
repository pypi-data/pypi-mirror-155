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
    max_stamp: int
    min_stamp: int
    count: int
    average: float


class PlotScopeStats(TypedDict):
    current: PlotStat
    hour: PlotStat
    day: PlotStat
    week: PlotStat
    month: PlotStat
    year: PlotStat


class PlotPrinterValueGroup(TypedDict):
    title: str
    values: List[PlotUnit]
