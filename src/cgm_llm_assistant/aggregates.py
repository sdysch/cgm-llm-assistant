import logging
from typing import Iterable

import pandas as pd

from cgm_llm_assistant.constants import GLUCOSE_COL, TIMESTAMP_COL
from cgm_llm_assistant.metrics import compute_summary_metrics

logger = logging.getLogger(__name__)


def resample_glucose(
    df: pd.DataFrame,
    minutes: int = 15,
) -> pd.DataFrame:
    """
    Resample glucose readings into N-minute bins.

    Parameters
    ----------
    df
        DataFrame containing 'timestamp' and 'sg_mmol'
    minutes
        Window size in minutes (e.g. 5, 15, 60)

    Returns
    -------
    DataFrame
        Aggregated glucose statistics per interval
    """

    logger.info("Resampling glucose data into %s-minute bins", minutes)

    g = df.set_index(TIMESTAMP_COL)[GLUCOSE_COL]

    freq = f"{minutes}min"

    agg = g.resample(freq).agg(
        mean="mean",
        median="median",
        std="std",
        min="min",
        max="max",
    )

    logger.debug("Generated %s aggregated rows", len(agg))

    return agg


def multi_window_resample(
    df: pd.DataFrame,
    windows: Iterable[int] = (5, 15, 60),
) -> dict[int, pd.DataFrame]:
    """
    Generate aggregates for multiple window sizes.
    """

    logger.info("Generating multi-window aggregates")

    results: dict[int, pd.DataFrame] = {}

    for w in windows:
        logger.debug("Processing %s minute window", w)
        results[w] = resample_glucose(df, minutes=w)

    return results


def hourly_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Average glucose by hour of day.
    """

    logger.info("Computing hourly glucose profile")

    profile = (
        df.assign(hour=df[TIMESTAMP_COL].dt.hour)
        .groupby("hour")[GLUCOSE_COL]
        .agg(
            mean="mean",
            std="std",
            count="count",
        )
    )

    return profile


def weekday_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Average glucose by weekday.
    """

    logger.info("Computing weekday glucose profile")

    profile = (
        df.assign(weekday=df[TIMESTAMP_COL].dt.day_name())
        .groupby("weekday")[GLUCOSE_COL]
        .agg(
            mean="mean",
            std="std",
            count="count",
        )
    )

    return profile


def daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute full metrics for each day.
    """

    logger.info("Computing daily summary metrics")

    results = []

    grouped = df.groupby(df[TIMESTAMP_COL].dt.date)

    for date, g in grouped:
        logger.debug("Processing %s", date)

        metrics = compute_summary_metrics(g)

        metrics["date"] = date

        results.append(metrics)

    return pd.DataFrame(results).set_index("date")


def glucose_rate_of_change(df: pd.DataFrame) -> pd.Series:
    """
    Compute glucose rate of change (mmol/L per minute).
    """

    logger.info("Computing glucose rate of change")

    g = df.set_index(TIMESTAMP_COL)[GLUCOSE_COL]

    dt = g.index.to_series().diff().dt.total_seconds() / 60

    roc = g.diff() / dt

    return roc


def rolling_glucose_stats(
    df: pd.DataFrame,
    window_minutes: int = 30,
) -> pd.DataFrame:
    """
    Rolling statistics for smoothing and trend detection.
    """

    logger.info("Computing rolling glucose statistics")

    g = df.set_index(TIMESTAMP_COL)[GLUCOSE_COL]

    window = f"{window_minutes}min"

    return pd.DataFrame(
        {
            "rolling_mean": g.rolling(window).mean(),
            "rolling_std": g.rolling(window).std(),
        }
    )
