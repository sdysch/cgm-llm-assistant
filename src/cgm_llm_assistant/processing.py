import logging

import pandas as pd
from pathlib import Path

from cgm_llm_assistant.constants import GLUCOSE_COL, BG_COL

logger = logging.getLogger(__name__)


def load_cgm_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a CGM CSV export and return a cleaned DataFrame with:
    - timestamp
    - bg_mmol
    - glucose (sensor glucose)

    Drops rows with missing sensor glucose.
    """
    logger.info(f"Loading CGM CSV from {path}")
    df = pd.read_csv(
        path,
        usecols=[
            "Date",
            "Time",
            "BG Reading (mmol/L)",
            "Sensor Glucose (mmol/L)",
        ],
    )
    logger.debug(f"Loaded {len(df)} rows from CSV")

    # Rename columns
    df = df.rename(
        columns={"BG Reading (mmol/L)": BG_COL, "Sensor Glucose (mmol/L)": GLUCOSE_COL}
    )

    # Drop rows where glucose is NaN
    df = df.dropna(subset=[GLUCOSE_COL])
    logger.debug(f"Dropped rows with missing glucose, remaining: {len(df)}")

    # Combine date and time into datetime
    df["timestamp"] = pd.to_datetime(
        df["Date"] + " " + df["Time"], format="%Y/%m/%d %H:%M:%S"
    )

    # Sort chronologically
    df = df.sort_values("timestamp").reset_index(drop=True)
    logger.debug("Sorted by timestamp")

    # Keep only relevant columns
    result = df[["timestamp", BG_COL, GLUCOSE_COL]]
    logger.info(f"Loaded {len(result)} CGM records")
    return result
