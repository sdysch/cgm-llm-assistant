from cgm_llm_assistant.processing import load_cgm_csv

df = load_cgm_csv('data/example_CGM_data_raw.csv')
print(df.head())
