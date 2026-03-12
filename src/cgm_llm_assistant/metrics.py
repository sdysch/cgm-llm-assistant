import logging
import pandas as pd
from cgm_llm_assistant.constants import GLUCOSE_COL, GlucoseThresholds

logger = logging.getLogger(__name__)


def average_glucose(df: pd.DataFrame) -> float:
    """
    Compute the mean glucose value.

    Parameters:
        df: DataFrame with a 'glucose' column.

    Returns:
        Average glucose as a float.
    """
    mean = df[GLUCOSE_COL].mean()
    logger.debug(f"Returning {mean}")
    return mean


def time_in_range(
    df: pd.DataFrame, thresholds: GlucoseThresholds = GlucoseThresholds()
) -> float:
    """
    Compute the proportion of readings within the target glucose range.

    Parameters:
        df: DataFrame with a 'glucose' column.
        thresholds: GlucoseThresholds object with LOW and HIGH values.

    Returns:
        Time-in-range as a float between 0 and 1.
    """
    tir = (
        (df[GLUCOSE_COL] >= thresholds.LOW) & (df[GLUCOSE_COL] <= thresholds.HIGH)
    ).mean()
    logger.debug(f"Returning {tir}")
    return tir


def high_events(
    df: pd.DataFrame, thresholds: GlucoseThresholds = GlucoseThresholds()
) -> int:
    """
    Count the number of glucose readings above the HIGH threshold.

    Parameters:
        df: DataFrame with a 'glucose' column.
        thresholds: GlucoseThresholds object.

    Returns:
        Number of high events as an integer.
    """
    high = (df[GLUCOSE_COL] > thresholds.HIGH).sum()
    logger.debug(f"Returning {high}")
    return high


def low_events(
    df: pd.DataFrame, thresholds: GlucoseThresholds = GlucoseThresholds()
) -> int:
    """
    Count the number of glucose readings below the LOW threshold.

    Parameters:
        df: DataFrame with a 'glucose' column.
        thresholds: GlucoseThresholds object.

    Returns:
        Number of low events as an integer.
    """
    low = (df[GLUCOSE_COL] < thresholds.LOW).sum()
    logger.debug(f"Returning {low}")
    return low


def coefficient_of_variation(df: pd.DataFrame) -> float:
    """
    Compute glucose variability (standard deviation / mean).

    Parameters:
        df: DataFrame with a 'glucose' column.

    Returns:
        Coefficient of variation as a float.
    """
    avg = average_glucose(df)
    cv = df[GLUCOSE_COL].std() / avg if avg else 0.0
    logger.debug(f"Returning {cv}")
    return cv
