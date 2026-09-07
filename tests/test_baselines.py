"""Tests for transparent forecasting baselines."""

import numpy as np
import pandas as pd
import pytest

from src.baselines import (
    add_baseline_forecasts,
    calculate_forecast_metrics
)


def make_monthly_data(prices):
    """Create one calendar-aligned test series."""

    return pd.DataFrame({
        "series": "Test series",
        "month": pd.date_range(
            "2024-01-01",
            periods=len(prices),
            freq="MS"
        ),
        "price": prices
    })


def test_baseline_values_are_correct():
    prices = list(range(100, 113))
    data = make_monthly_data(prices)

    result = add_baseline_forecasts(data)

    assert np.isnan(
        result.loc[0, "last_value_forecast"]
    )

    assert (
        result.loc[1, "last_value_forecast"]
        == 100
    )

    assert (
        result.loc[3, "rolling_median_3_forecast"]
        == 101
    )

    assert (
        result.loc[12, "seasonal_naive_forecast"]
        == 100
    )


def test_missing_prices_are_not_filled():
    data = make_monthly_data(
        [100, np.nan, 120, 130]
    )

    result = add_baseline_forecasts(data)

    assert np.isnan(
        result.loc[2, "last_value_forecast"]
    )

    assert np.isnan(
        result.loc[
            3,
            "rolling_median_3_forecast"
        ]
    )


def test_series_do_not_leak_into_each_other():
    data = pd.DataFrame({
        "series": ["A", "A", "B", "B"],
        "month": pd.to_datetime([
            "2024-01-01",
            "2024-02-01",
            "2024-01-01",
            "2024-02-01"
        ]),
        "price": [100, 110, 1000, 1100]
    })

    result = add_baseline_forecasts(data)

    series_b = result[
        result["series"] == "B"
    ].reset_index(drop=True)

    assert np.isnan(
        series_b.loc[0, "last_value_forecast"]
    )

    assert (
        series_b.loc[1, "last_value_forecast"]
        == 1000
    )


def test_non_aligned_calendar_is_rejected():
    data = pd.DataFrame({
        "series": ["A", "A"],
        "month": pd.to_datetime([
            "2024-01-01",
            "2024-03-01"
        ]),
        "price": [100, 120]
    })

    with pytest.raises(
        ValueError,
        match="not calendar-aligned"
    ):
        add_baseline_forecasts(data)


def test_duplicate_month_is_rejected():
    data = pd.DataFrame({
        "series": ["A", "A"],
        "month": pd.to_datetime([
            "2024-01-01",
            "2024-01-01"
        ]),
        "price": [100, 110]
    })

    with pytest.raises(
        ValueError,
        match="Duplicate"
    ):
        add_baseline_forecasts(data)


def test_empty_dataframe_is_rejected():
    data = pd.DataFrame(
        columns=["series", "month", "price"]
    )

    with pytest.raises(
        ValueError,
        match="empty"
    ):
        add_baseline_forecasts(data)


def test_metric_values_are_correct():
    data = pd.DataFrame({
        "actual": [100, 200],
        "forecast": [110, 180]
    })

    metrics = calculate_forecast_metrics(
        data,
        actual_column="actual",
        forecast_column="forecast"
    )

    assert metrics["observed_targets"] == 2
    assert metrics["predictions"] == 2
    assert metrics["coverage_pct"] == pytest.approx(100)
    assert metrics["mae_ngn"] == pytest.approx(15)
    assert metrics["wape_pct"] == pytest.approx(10)
    assert metrics["bias_ngn"] == pytest.approx(-5)

    assert metrics["bias_pct"] == pytest.approx(
        -10 / 300 * 100
    )


def test_missing_forecast_reduces_coverage():
    data = pd.DataFrame({
        "actual": [100, 200, 300],
        "forecast": [110, np.nan, 330]
    })

    metrics = calculate_forecast_metrics(
        data,
        actual_column="actual",
        forecast_column="forecast"
    )

    assert metrics["observed_targets"] == 3
    assert metrics["predictions"] == 2

    assert metrics["coverage_pct"] == pytest.approx(
        2 / 3 * 100
    )