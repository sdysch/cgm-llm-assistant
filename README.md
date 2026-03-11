# CGM LLM Assistant
A small project for exploring continuous glucose monitor (CGM) data and generating natural language explanations of glucose trends using large language models.

This project is intended to be used with my Medtronic Guardian 4 CGM data, using the raw export from the website.
Compatibility with other CGM sources is not intended, but could be hacked.

Example dataframe:
```python
           Date      Time  bg_mmol  sg_mmol
526  2026/02/23  22:00:32      NaN      9.2
527  2026/02/23  21:55:32      NaN      9.0
528  2026/02/23  21:50:32      NaN      8.9
529  2026/02/23  21:45:32      NaN      8.7
530  2026/02/23  21:40:32      NaN      8.5
```

The goal is to make it easy to answer questions like:

* When do my glucose spikes happen most often?
* How stable is my overnight glucose?
* What patterns appear across days or weeks?
* The project processes CGM exports, computes common glucose metrics, and produces summaries that can be interpreted by an LLM.

## Features (planned / in progress)

* Load CGM data from CSV exports
* Compute common CGM metrics
* Detect glucose spikes and lows
* Generate trend summaries
* Explain glucose patterns using an LLM
* Interactive dashboard for exploration
* Integrate bolus wizard, autobolus info

## Example Questions

The assistant aims to answer questions such as:
* Why did my glucose spike yesterday?
* What time of day has the most variability?
* Are my overnight readings stable?
* Which days had the best time-in-range?

## Setup

This project uses `uv` for dependency and environment management.

Install dependencies:
```bash
uv sync
```

Activate the environment:

```bash
source .venv/bin/activate
```

## Development

Install development dependencies:

```bash
uv sync --group dev
```

Run tests:

```bash
uv run pytest
```

Lint code:

```bash
uv run ruff check
```

## Disclaimer
This project is for data exploration and educational purposes only.
It is not medical advice and should not be used for clinical decisions.
