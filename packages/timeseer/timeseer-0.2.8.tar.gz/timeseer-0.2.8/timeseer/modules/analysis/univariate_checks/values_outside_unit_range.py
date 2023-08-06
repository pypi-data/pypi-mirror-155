"""For certain units (e.g. pH) there is a limited range values can take.

<p>This check validates whether for a specific set of units, the historical values are
within the expected deterministic range.</p>
<p class="scoring-explanation">The score for this check is based on the amount
of time values are outside of the unit range.</p>
<div class="ts-check-impact">
<p>Mismatches between unit range and measured values are data quality issues.
</p>
</div>
"""

from enum import Enum, auto
from datetime import datetime

import numpy as np
import pandas as pd

from pandas.api.types import is_string_dtype

from pint import UndefinedUnitError

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    get_unit_registry,
    event_frames_from_dataframe,
    merge_intervals_and_open_event_frames,
    process_open_intervals,
)
from timeseer.metadata import fields

_CHECK_NAME = "Values outside unit range"
_EVENT_FRAME_NAME = "Values outside unit range"


META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


class LimitType(Enum):
    """Choose whether to use physical or functional limits."""

    PHYSICAL = auto()
    FUNCTIONAL = auto()


def _make_units_dir():
    ureg = get_unit_registry()
    units_zero_min = [
        "meter",
        "second",
        "ampere",
        "candela",
        "gram",
        "mole",
        "kelvin",
        "unit",
        "pH",
        "m2",
        "liter",
        "hertz",
        "kph",
        "galileo",
        "newton",
        "joule",
        "watt",
        "water",
        "pascal",
        "foot_pound",
        "poise",
        "stokes",
        "rhe",
        "particle",
        "molar",
        "katal",
        "clausius",
        "entropy_unit",
        "curie",
        "langley",
        "nit",
        "lumen",
        "lux",
        "a_u_intensity",
        "volt",
        "ohm",
        "siemens",
        "henry",
        "weber",
        "tesla",
        "bohr_magneton",
    ]
    dimensions_zero_min = []
    for unit in units_zero_min:
        dimension = ureg.get_dimensionality(unit)
        dimensions_zero_min.append(dimension)
    return dimensions_zero_min


def _get_intervals(outliers, df, event_type):
    outliers = pd.Series(data=outliers, index=df.index).fillna(False)
    outlier_grp = (outliers != outliers.shift().bfill()).cumsum()
    outlier_intervals = (
        df.assign(outlier_grp=outlier_grp)[outliers]
        .reset_index()
        .groupby(["outlier_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    outlier_intervals["type"] = event_type
    return outlier_intervals


def _get_active_points(df: pd.DataFrame, min_value: float, max_value: float):
    return (df["value"] < min_value) | (df["value"] > max_value)


def _handle_open_intervals(df, intervals):
    intervals["open"] = intervals["end_date"] == df.index[-1]
    return intervals


def _get_dimensionality(unit):
    ureg = get_unit_registry()
    try:
        return ureg.get_dimensionality(unit)
    except (UndefinedUnitError, AttributeError, ValueError, KeyError):
        return "Unknown"


def _unit_dir(unit):
    input_dimension = _get_dimensionality(unit)
    return input_dimension


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_values_outside_unit_range_check(
    unit, analysis_input: AnalysisInput, open_event_frames: list[EventFrame]
) -> tuple[list[EventFrame], datetime]:
    df = analysis_input.data
    df = _clean_dataframe(df)

    analysis_start = df.index[0]
    if analysis_input.analysis_start is not None:
        analysis_start = analysis_input.analysis_start

    min_value = 0
    max_value = np.inf
    if _unit_dir(unit) == _get_dimensionality("pH"):
        max_value = 14

    active_points = _get_active_points(df, min_value, max_value)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    intervals = _handle_open_intervals(df, intervals)

    intervals = merge_intervals_and_open_event_frames(
        analysis_start, intervals, open_event_frames
    )

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = df.index[-1]

    return list(frames), last_analyzed_point


def _is_relevant_open_event_frame(event_frame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
    )


def _get_open_event_frames(
    analysis_input: AnalysisInput,
) -> list[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _is_valid_input(
    analysis_input: AnalysisInput, median_archival_step: list[float], unit: str
) -> tuple[str, bool]:
    if median_archival_step is None or len(median_archival_step) == 0:
        return "No median archival step", False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No data", False
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    if unit is None:
        return "No unit", False
    dimensions_zero_min = _make_units_dir()
    if _unit_dir(unit) not in dimensions_zero_min:
        return "Unit not in dimensions", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    unit = analysis_input.metadata.get_field(fields.Unit)
    median_archival_step = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == "Archival time median"
    ]

    message, is_ok = _is_valid_input(analysis_input, median_archival_step, unit)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    open_event_frames = _get_open_event_frames(analysis_input)

    frames, last_analyzed_point = _run_values_outside_unit_range_check(
        unit, analysis_input, open_event_frames
    )
    return AnalysisResult(
        event_frames=frames,
        last_analyzed_point=last_analyzed_point,
    )
