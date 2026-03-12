import pandas as pd
import pytest

from cgm_llm_assistant.metrics import (
    average_glucose,
    time_in_range,
    high_events,
    low_events,
    coefficient_of_variation,
    median_glucose,
    glucose_std,
    compute_summary_metrics,
)
from cgm_llm_assistant.constants import GLUCOSE_COL, GlucoseThresholds


@pytest.fixture
def sample_df():
    """Return a small DataFrame of glucose readings for testing."""
    return pd.DataFrame({GLUCOSE_COL: [3.5, 4.2, 5.5, 9.8, 10.5, 7.0]})


def test_average_glucose(sample_df):
    result = average_glucose(sample_df)
    expected = sum([3.5, 4.2, 5.5, 9.8, 10.5, 7.0]) / 6
    assert abs(result - expected) < 1e-6


def test_time_in_range_default(sample_df):
    thresholds = GlucoseThresholds()
    result = time_in_range(sample_df, thresholds)
    # readings in range: 4.2, 5.5, 7.0, 9.8 → 4/6
    assert abs(result - (4 / 6)) < 1e-6


def test_high_events(sample_df):
    thresholds = GlucoseThresholds()
    result = high_events(sample_df, thresholds)
    # high > 10 → 10.5 → 1 event
    assert result == 1


def test_low_events(sample_df):
    thresholds = GlucoseThresholds()
    result = low_events(sample_df, thresholds)
    # low < 3.9 → 3.5 → 1 event
    assert result == 1


def test_coefficient_of_variation(sample_df):
    avg = average_glucose(sample_df)
    expected_cv = sample_df[GLUCOSE_COL].std() / avg
    result = coefficient_of_variation(sample_df)
    assert abs(result - expected_cv) < 1e-6


def test_median_glucose(sample_df):
    result = median_glucose(sample_df)
    expected = sample_df[GLUCOSE_COL].median()
    assert abs(result - expected) < 1e-6


def test_glucose_std(sample_df):
    result = glucose_std(sample_df)
    expected = sample_df[GLUCOSE_COL].std()
    assert abs(result - expected) < 1e-6


def test_compute_summary_metrics(sample_df):
    thresholds = GlucoseThresholds()
    result = compute_summary_metrics(sample_df, thresholds)

    assert "avg_glucose" in result
    assert "median_glucose" in result
    assert "std_glucose" in result
    assert "cv" in result
    assert "time_in_range" in result
    assert "high_events" in result
    assert "low_events" in result

    assert abs(result["avg_glucose"] - average_glucose(sample_df)) < 1e-6
    assert abs(result["median_glucose"] - median_glucose(sample_df)) < 1e-6
    assert abs(result["std_glucose"] - glucose_std(sample_df)) < 1e-6
    assert abs(result["cv"] - coefficient_of_variation(sample_df)) < 1e-6
    assert abs(result["time_in_range"] - time_in_range(sample_df, thresholds)) < 1e-6
    assert result["high_events"] == high_events(sample_df, thresholds)
    assert result["low_events"] == low_events(sample_df, thresholds)
