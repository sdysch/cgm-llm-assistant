import logging

import pandas as pd

from cgm_llm_assistant.metrics import compute_summary_metrics
from cgm_llm_assistant.aggregates import (
    hourly_profile,
    daily_summary,
    multi_window_resample,
)

logger = logging.getLogger(__name__)


def build_context(df):
    """Prepare structured CGM context for LLM analysis."""

    logger.info("Building context from glucose DataFrame")

    logger.debug("Computing summary metrics")
    summary = compute_summary_metrics(df)

    logger.debug("Computing hourly profile")
    hourly = hourly_profile(df)

    logger.debug("Computing daily summary")
    daily = daily_summary(df)

    logger.debug("Generating multi-window aggregates")
    windows = multi_window_resample(df, windows=(5, 15, 30))

    logger.info("Context built successfully with %d window aggregates", len(windows))

    hourly_dict = {}
    for (date, hour), row in hourly.iterrows():
        date_str = str(date)
        if date_str not in hourly_dict:
            hourly_dict[date_str] = {}
        hourly_dict[date_str][f"hour_{hour}"] = {
            "mean": row["mean"],
            "std": row["std"] if pd.notna(row["std"]) else None,
            "count": int(row["count"]),
        }

    context = {
        "summary_metrics": summary,
        "hourly_profile": hourly_dict,
        "daily_metrics": daily.to_dict(),
        "window_aggregates": {
            f"{minutes}_min": agg.reset_index().to_dict(orient="records")
            for minutes, agg in windows.items()
        },
    }

    logger.debug(f"Returning context: {context}")
    return context
