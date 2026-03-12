from dataclasses import dataclass


GLUCOSE_COL = "sg_mmol"
BG_COL = "bg_mmol"


@dataclass(frozen=True)
class GlucoseThresholds:
    """Default glucose thresholds (mmol/L) for CGM metrics."""

    LOW: float = 3.9
    HIGH: float = 10.0
