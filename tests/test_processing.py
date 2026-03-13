import pandas as pd
from pathlib import Path

from cgm_llm_assistant.processing import load_cgm_csv


def test_load_example_csv():
    """Test loading the example.csv data file."""
    data_path = Path(__file__).parent.parent / "data" / "example.csv"
    df = load_cgm_csv(data_path)

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "timestamp" in df.columns
    assert "bg_mmol" in df.columns
    assert "sg_mmol" in df.columns
