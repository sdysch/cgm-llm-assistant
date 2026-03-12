import pandas as pd
import pytest
from datetime import datetime, timedelta

from cgm_llm_assistant.aggregates import (
    resample_glucose,
    multi_window_resample,
    hourly_profile,
    weekday_profile,
    glucose_rate_of_change,
    rolling_glucose_stats,
)
from cgm_llm_assistant.constants import GLUCOSE_COL, TIMESTAMP_COL


@pytest.fixture
def sample_df():
    """Return a small DataFrame with timestamp and glucose for testing."""
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    timestamps = [base_time + timedelta(minutes=i * 5) for i in range(12)]
    glucose_values = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 7.5, 7.0, 6.5, 6.0, 5.5]
    return pd.DataFrame({TIMESTAMP_COL: timestamps, GLUCOSE_COL: glucose_values})


def test_resample_glucose(sample_df):
    result = resample_glucose(sample_df, minutes=15)
    assert isinstance(result, pd.DataFrame)
    assert "mean" in result.columns
    assert len(result) > 0


def test_multi_window_resample(sample_df):
    result = multi_window_resample(sample_df, windows=[5, 15])
    assert isinstance(result, dict)
    assert 5 in result
    assert 15 in result


def test_hourly_profile(sample_df):
    result = hourly_profile(sample_df)
    assert isinstance(result, pd.DataFrame)
    assert "mean" in result.columns


def test_weekday_profile(sample_df):
    result = weekday_profile(sample_df)
    assert isinstance(result, pd.DataFrame)
    assert "mean" in result.columns


def test_glucose_rate_of_change(sample_df):
    result = glucose_rate_of_change(sample_df)
    assert isinstance(result, pd.Series)
    assert len(result) == len(sample_df)


def test_rolling_glucose_stats(sample_df):
    result = rolling_glucose_stats(sample_df, window_minutes=15)
    assert isinstance(result, pd.DataFrame)
    assert "rolling_mean" in result.columns
    assert "rolling_std" in result.columns
