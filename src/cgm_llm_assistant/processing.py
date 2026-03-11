import pandas as pd
from pathlib import Path

def load_cgm_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a CGM CSV export and return a cleaned DataFrame with:
    - timestamp
    - bg_mmol
    - glucose (sensor glucose)
    
    Drops rows with missing sensor glucose.
    """
    df = pd.read_csv(
        path,
        usecols=[
            'Date',
            'Time',
            'BG Reading (mmol/L)',
            'Sensor Glucose (mmol/L)',
        ]
    )

    # Rename columns
    df = df.rename(
        columns={
            'BG Reading (mmol/L)': 'bg_mmol',
            'Sensor Glucose (mmol/L)': 'glucose'
        }
    )

    # Drop rows where glucose is NaN
    df = df.dropna(subset=['glucose'])

    # Combine date and time into datetime
    df['timestamp'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'],
        format='%Y/%m/%d %H:%M:%S'
    )

    # Sort chronologically
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Keep only relevant columns
    return df[['timestamp', 'bg_mmol', 'glucose']]
