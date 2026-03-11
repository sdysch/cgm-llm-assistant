import pandas as pd

# %% Read data and format
df = pd.read_csv(
    'data/example_CGM_data_raw.csv',
    usecols=[
        'Date',
        'Time',
        'BG Reading (mmol/L)',
        'Sensor Glucose (mmol/L)',
    ]
)

df = df.rename(
    columns={
        'BG Reading (mmol/L)': 'bg_mmol',
        'Sensor Glucose (mmol/L)': 'sg_mmol'
    }
)

# Drop NaN SG cols for now
df = df.dropna(subset=['sg_mmol'])

# Format
df['timestamp'] = pd.to_datetime(
    df['Date'] + ' ' + df['Time'],
    format='%Y/%m/%d %H:%M:%S'
)

df = df.sort_values('timestamp').reset_index(drop=True)

df
