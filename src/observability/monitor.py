"""Observability helpers for Week 7.

Week 7 focus:
- Structured metrics with dimensional tags
- Distributed tracing via correlation IDs
- Health check aggregation
- High-resolution performance timing
- Threshold-based severity classification
"""
import time
import uuid
from typing import Optional, Dict



def record_metric(
    name: str,
    value: float,
    unit: str = "count",
    tags: Optional[Dict] = None,
    now: Optional[int] = None,
) -> dict:
    """Record a named metric with optional dimensions.

    Requirements:
    - Return a dict with keys: name, value, unit, tags, timestamp
    - tags should default to {} (not None) in the returned dict
    - timestamp is an epoch int; use now if provided, else time.time()
    """
    if tags is None:
        tags={}
    if now is None:
        now = int(time.time())
    
    metric = {
        "name": name,
        "value": value,
        "unit": unit,
        "tags": tags,
        "timestamp": now,
    }
    return metric



def build_health_response(checks: dict[str, bool]) -> dict:
    """Aggregate component checks into a health response.

    Requirements:
    - Return {"status": "healthy", "checks": checks} when all are True
    - Return {"status": "degraded", "checks": checks} when any are False
    """
    status = "healthy"
    for check_passed in checks.values():
        if not check_passed:
            status = "degraded"
            break
    return {"status": status, "checks": checks}



def elapsed_ms(start_ns: int, end_ns: int) -> float:
    """Compute elapsed time in milliseconds from nanosecond timestamps.

    Use time.time_ns() to capture start/end values.
    Convert: (end_ns - start_ns) / 1_000_000
    """
    return (end_ns - start_ns) / 1_000_000



def check_threshold(value: float, warning: float, critical: float) -> str:
    """Classify a metric value against warning and critical thresholds.

    Return:
    - "ok"       when value < warning
    - "warning"  when warning <= value < critical
    - "critical" when value >= critical
    """

    if value < warning:
        return "ok"

    elif (value >= warning) and (value < critical):
        return "warning"
    
    elif value>= critical:
        return 'critical'
    else:
        return f"Warning value should be less than critical value: warning = {warning}, critical = {critical}"
    
