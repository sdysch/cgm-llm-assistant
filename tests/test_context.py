import pandas as pd
import pytest
from datetime import datetime, timedelta

from cgm_llm_assistant.context import build_context
from cgm_llm_assistant.constants import GLUCOSE_COL, TIMESTAMP_COL


@pytest.fixture
def sample_df():
    """Return a small DataFrame with timestamp and glucose for testing."""
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    timestamps = [base_time + timedelta(minutes=i * 5) for i in range(24)]
    glucose_values = [
        5.0,
        5.5,
        6.0,
        6.5,
        7.0,
        7.5,
        8.0,
        8.5,
        9.0,
        8.5,
        8.0,
        7.5,
        7.0,
        6.5,
        6.0,
        5.5,
        5.0,
        4.5,
        4.0,
        4.5,
        5.0,
        5.5,
        6.0,
        6.5,
    ]
    return pd.DataFrame({TIMESTAMP_COL: timestamps, GLUCOSE_COL: glucose_values})


def test_build_context_returns_dict(sample_df):
    result = build_context(sample_df)
    assert isinstance(result, dict)


def test_build_context_contains_summary_metrics(sample_df):
    result = build_context(sample_df)
    assert "summary_metrics" in result


def test_build_context_contains_hourly_profile(sample_df):
    result = build_context(sample_df)
    assert "hourly_profile" in result


def test_build_context_contains_daily_metrics(sample_df):
    result = build_context(sample_df)
    assert "daily_metrics" in result


def test_build_context_contains_window_aggregates(sample_df):
    result = build_context(sample_df)
    assert "window_aggregates" in result


def test_build_context_window_aggregates_keys(sample_df):
    result = build_context(sample_df)
    assert "5_min" in result["window_aggregates"]
    assert "15_min" in result["window_aggregates"]
    assert "30_min" in result["window_aggregates"]


def test_build_context_summary_metrics_values(sample_df):
    result = build_context(sample_df)
    summary = result["summary_metrics"]
    assert "avg_glucose" in summary
    assert "median_glucose" in summary
    assert "time_in_range" in summary


def test_build_context_hourly_profile_is_dict(sample_df):
    result = build_context(sample_df)
    assert isinstance(result["hourly_profile"], dict)


def test_build_context_daily_metrics_is_dict(sample_df):
    result = build_context(sample_df)
    assert isinstance(result["daily_metrics"], dict)
