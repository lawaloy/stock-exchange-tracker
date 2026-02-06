"""
Alert rule evaluators.
"""

from typing import Dict, List


def _compare(value: float, operator: str, threshold: float) -> bool:
    if operator == "less_than":
        return value < threshold
    if operator == "less_or_equal":
        return value <= threshold
    if operator == "greater_than":
        return value > threshold
    if operator == "greater_or_equal":
        return value >= threshold
    if operator == "equal":
        return value == threshold
    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_price_threshold(condition: Dict, stock: Dict) -> bool:
    """
    Evaluate a price threshold condition against a single stock record.
    """
    operator = condition.get("operator", "less_than")
    threshold = float(condition.get("value", 0))
    price = float(stock.get("close", 0))
    return _compare(price, operator, threshold)


def evaluate_screening_match(condition: Dict, stock: Dict) -> bool:
    """
    Evaluate a screening condition using simple numeric thresholds.
    Supported keys: volume_threshold, min_daily_change_pct, price_min, price_max.
    """
    filters = condition.get("filters", {})
    volume_threshold = filters.get("volume_threshold")
    min_daily_change_pct = filters.get("min_daily_change_pct")
    price_min = filters.get("price_min")
    price_max = filters.get("price_max")

    if volume_threshold is not None and float(stock.get("volume", 0)) < float(volume_threshold):
        return False
    if min_daily_change_pct is not None and abs(float(stock.get("change_percent", 0))) < float(min_daily_change_pct):
        return False
    if price_min is not None and float(stock.get("close", 0)) < float(price_min):
        return False
    if price_max is not None and float(stock.get("close", 0)) > float(price_max):
        return False

    return True
