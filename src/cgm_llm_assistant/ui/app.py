import logging
from pathlib import Path

import streamlit as st

from cgm_llm_assistant.processing import load_cgm_csv
from cgm_llm_assistant.context import build_context
from cgm_llm_assistant.llm import check_model, explain_metrics

logger = logging.getLogger(__name__)


def get_data_files():
    data_dir = Path("data")
    if not data_dir.exists():
        return []
    return [f.name for f in data_dir.glob("*.csv")]


def main(model: str = "phi3:mini"):
    st.set_page_config(page_title="CGM LLM Assistant", page_icon="📊")

    st.title("CGM LLM Assistant")
    st.markdown(
        "Explore your continuous glucose monitor data with AI-powered insights."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Select Data Source")
        data_source = st.radio(
            "Choose data source:",
            ["Use file from data/ folder", "Upload a CSV file"],
            horizontal=True,
        )

    with col2:
        st.subheader("2. Select Model")
        default_model = model if model else "phi3:mini"
        selected_model = st.text_input(
            "Model to use for inference",
            value=default_model,
            help="Ollama model (e.g., phi3:mini, llama2, mistral)",
        )

    df = None

    if data_source == "Use file from data/ folder":
        data_files = get_data_files()
        if data_files:
            selected_file = st.selectbox("Select a CSV file:", data_files)
            if st.button("Load Data"):
                with st.spinner("Loading data..."):
                    try:
                        df = load_cgm_csv(f"data/{selected_file}")
                        st.success(f"Loaded {len(df)} records from {selected_file}")
                    except Exception as e:
                        st.error(f"Error loading file: {e}")
        else:
            st.info("No CSV files found in data/ folder")
    else:
        uploaded_file = st.file_uploader(
            "Upload a CGM CSV file",
            type=["csv"],
            help="Upload a CSV export from Medtronic Guardian 4",
        )
        if uploaded_file is not None:
            with st.spinner("Loading data..."):
                try:
                    import tempfile

                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".csv"
                    ) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name

                    df = load_cgm_csv(tmp_path)
                    st.success(f"Loaded {len(df)} records from uploaded file")
                except Exception as e:
                    st.error(f"Error loading file: {e}")

    if df is not None and len(df) > 0:
        st.divider()
        st.subheader("3. Ask Questions About Your Data")

        model_available = check_model(selected_model)
        if not model_available:
            st.warning(
                f"Model '{selected_model}' not available. "
                f"Please install with: `ollama pull {selected_model}`"
            )
            return

        with st.spinner("Building context..."):
            context = build_context(df)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a question about your CGM data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Getting answer..."):
                    try:
                        answer = explain_metrics(context, prompt, model=selected_model)
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"Error getting explanation: {e}")
                        answer = f"Error: {e}"

            st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.expander("View loaded data summary"):
            st.write(f"Total records: {len(df)}")
            st.write(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
            st.dataframe(df.head(10))

    elif df is not None and len(df) == 0:
        st.warning("No valid CGM records found in the file.")


if __name__ == "__main__":
    import sys

    model = "phi3:mini"
    if len(sys.argv) > 1 and sys.argv[1].startswith("--model="):
        model = sys.argv[1].split("=", 1)[1]
    elif "--model" in sys.argv:
        idx = sys.argv.index("--model")
        if idx + 1 < len(sys.argv):
            model = sys.argv[idx + 1]

    main(model=model)
