import logging

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

    context = {
        "summary_metrics": summary,
        "hourly_profile": hourly.to_dict(),
        "daily_metrics": daily.to_dict(),
        # Time-window aggregates
        "window_aggregates": {
            f"{minutes}_min": agg.reset_index().to_dict(orient="records")
            for minutes, agg in windows.items()
        },
    }

    logger.debug(f"Returning context: {context}")
    return context
