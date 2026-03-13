import logging

import pandas as pd

from cgm_llm_assistant.constants import GlucoseThresholds
from cgm_llm_assistant.metrics.metrics import (
    average_glucose,
    coefficient_of_variation,
    glucose_std,
    high_events,
    low_events,
    median_glucose,
    time_in_range,
)

logger = logging.getLogger(__name__)


def compute_summary_metrics(
    df: pd.DataFrame, thresholds: GlucoseThresholds = GlucoseThresholds()
) -> dict:
    """
    Compute a dictionary of summary glucose metrics.

    Parameters:
        df: DataFrame with a 'glucose' column.
        thresholds: GlucoseThresholds object with LOW and HIGH values.

    Returns:
        Dictionary containing avg_glucose, median_glucose, std_glucose, cv,
        time_in_range, high_events, and low_events.
    """
    logger.debug("Computing summary metrics")
    result = {
        "avg_glucose": average_glucose(df),
        "median_glucose": median_glucose(df),
        "std_glucose": glucose_std(df),
        "cv": coefficient_of_variation(df),
        "time_in_range": time_in_range(df, thresholds),
        "high_events": high_events(df, thresholds),
        "low_events": low_events(df, thresholds),
    }
    logger.debug(f"Summary metrics: {result}")
    return result


__all__ = ["compute_summary_metrics"]
