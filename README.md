# CGM LLM Assistant

![CI](https://github.com/sdysch/cgm-llm-assistant/actions/workflows/ci.yml/badge.svg)

A project for exploring continuous glucose monitor (CGM) data and generating natural language explanations of glucose trends using large language models.

> **Note**: This project is designed for Medtronic Guardian 4 CGM data exported from the website. Other CGM sources may require adaptation.

## Example Output

```python
           Date      Time  bg_mmol  sg_mmol
526  2026/02/23  22:00:32      NaN      9.2
527  2026/02/23  21:55:32      NaN      9.0
```

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for dependency management
- [ollama](https://ollama.com/) (optional, for local LLM inference)

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Pull an LLM model 
ollama pull phi3:mini

# 3. Run the assistant
uv run cgm-assistant data/example_CGM_data_raw.csv
```

## Installation

### 1. Install uv

If you don't have `uv` installed, follow the [official guide](https://docs.astral.sh/uv/#installation) or use:

### 2. Install dependencies

```bash
uv sync
```

This creates a virtual environment and installs all dependencies automatically.

### 3. Activate the environment (optional)

```bash
source .venv/bin/activate
```

Alternatively, use `uv run` to execute commands in the environment without activating it.

## Development

### Install dev dependencies

```bash
uv sync --group dev
```

### Run tests

```bash
uv run pytest
```

### Lint code

```bash
uv run ruff check
```

## Usage

### CLI

Process a CGM export file:

```bash
uv run cgm-assistant data/example_CGM_data_raw.csv
```

Specify a different model (must be installed first):

```bash
uv run cgm-assistant data/example_CGM_data_raw.csv --model my_model
```

### Interactive Dashboard (TODO)

```bash
uv run streamlit run src/cgm_llm_assistant/dashboard.py
```

### Setting up Ollama

For local LLM inference, install and run [ollama](https://ollama.com/):

```bash
# Start ollama server
ollama serve

# Pull a model
ollama pull phi3:mini
```

## Features

- Load CGM data from CSV exports
- Compute common CGM metrics (time-in-range, etc.)
- Explain glucose patterns using an LLM (in progress)
- Detect glucose spikes and lows (todo)
- Generate trend summaries (todo)
- Interactive dashboard for exploration (todo)

## Disclaimer

This project is for data exploration and educational purposes only.
It is not medical advice and should not be used for clinical decisions.
