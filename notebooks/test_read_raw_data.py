from cgm_llm_assistant.processing import load_cgm_csv
from cgm_llm_assistant.context import build_context

df = load_cgm_csv("data/example_CGM_data_raw.csv")

context = build_context(df)
context.keys()
