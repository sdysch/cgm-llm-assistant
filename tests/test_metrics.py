import pandas as pd
import pytest

from cgm_llm_assistant.metrics import (
    average_glucose,
    time_in_range,
    high_events,
    low_events,
    coefficient_of_variation,
)
from cgm_llm_assistant.constants import GlucoseThresholds


@pytest.fixture
def sample_df():
    """Return a small DataFrame of glucose readings for testing."""
    return pd.DataFrame({"glucose": [3.5, 4.2, 5.5, 9.8, 10.5, 7.0]})


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
    expected_cv = sample_df["glucose"].std() / avg
    result = coefficient_of_variation(sample_df)
    assert abs(result - expected_cv) < 1e-6
