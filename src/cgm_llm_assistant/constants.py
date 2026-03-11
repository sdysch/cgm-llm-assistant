from dataclasses import dataclass


@dataclass(frozen=True)
class GlucoseThresholds:
    """Default glucose thresholds (mmol/L) for CGM metrics."""

    LOW: float = 3.9
    HIGH: float = 10.0
