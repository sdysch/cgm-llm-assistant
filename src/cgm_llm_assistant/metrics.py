import pandas as pd
from cgm_llm_assistant.constants import GLUCOSE_COL, GlucoseThresholds


def average_glucose(df: pd.DataFrame) -> float:
    """
    Compute the mean glucose value.

    Parameters:
        df: DataFrame with a 'glucose' column.

    Returns:
        Average glucose as a float.
    """
    return df[GLUCOSE_COL].mean()


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
    return (
        (df[GLUCOSE_COL] >= thresholds.LOW) & (df[GLUCOSE_COL] <= thresholds.HIGH)
    ).mean()


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
    return (df[GLUCOSE_COL] > thresholds.HIGH).sum()


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
    return (df[GLUCOSE_COL] < thresholds.LOW).sum()


def coefficient_of_variation(df: pd.DataFrame) -> float:
    """
    Compute glucose variability (standard deviation / mean).

    Parameters:
        df: DataFrame with a 'glucose' column.

    Returns:
        Coefficient of variation as a float.
    """
    avg = average_glucose(df)
    return df[GLUCOSE_COL].std() / avg if avg else 0.0
