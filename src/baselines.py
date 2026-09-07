"""Transparent forecasting baselines and evaluation metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_BASELINE_COLUMNS = {
    "series",
    "month",
    "price"
}


def _require_columns(
    data: pd.DataFrame,
    required_columns: set[str]
) -> None:
    """Raise an error when required columns are unavailable."""

    missing_columns = (
        required_columns
        - set(data.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )


def _validate_monthly_calendar(
    data: pd.DataFrame
) -> None:
    """Confirm that every series has one row per calendar month."""

    duplicate_months = data.duplicated(
        subset=["series", "month"],
        keep=False
    )

    if duplicate_months.any():
        raise ValueError(
            "Duplicate series-month observations detected."
        )

    for series_name, series in data.groupby(
        "series",
        sort=False
    ):
        months = pd.DatetimeIndex(
            series["month"].sort_values()
        )

        expected_months = pd.date_range(
            months.min(),
            months.max(),
            freq="MS"
        )

        calendar_is_complete = (
            len(months) == len(expected_months)
            and np.array_equal(
                months.to_numpy(),
                expected_months.to_numpy()
            )
        )

        if not calendar_is_complete:
            raise ValueError(
                f"{series_name} is not calendar-aligned. "
                "Represent missing months as rows with NaN prices."
            )


def add_baseline_forecasts(
    data: pd.DataFrame
) -> pd.DataFrame:
    """Add last-value, rolling-median and seasonal forecasts."""

    _require_columns(
        data,
        REQUIRED_BASELINE_COLUMNS
    )

    if data.empty:
        raise ValueError(
            "Cannot forecast an empty DataFrame."
        )

    result = data.copy()

    result["month"] = (
        pd.to_datetime(
            result["month"],
            errors="raise"
        )
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    result["price"] = pd.to_numeric(
        result["price"],
        errors="raise"
    )

    result = (
        result
        .sort_values(["series", "month"])
        .reset_index(drop=True)
    )

    _validate_monthly_calendar(result)

    result["last_value_forecast"] = (
        result
        .groupby("series")["price"]
        .shift(1)
    )

    result["rolling_median_3_forecast"] = (
        result
        .groupby("series")["price"]
        .transform(
            lambda prices: (
                prices
                .shift(1)
                .rolling(
                    window=3,
                    min_periods=3
                )
                .median()
            )
        )
    )

    result["seasonal_naive_forecast"] = (
        result
        .groupby("series")["price"]
        .shift(12)
    )

    return result


def calculate_forecast_metrics(
    data: pd.DataFrame,
    actual_column: str,
    forecast_column: str
) -> dict[str, float | int]:
    """Calculate coverage, MAE, WAPE and forecast bias."""

    _require_columns(
        data,
        {
            actual_column,
            forecast_column
        }
    )

    actual_values = pd.to_numeric(
        data[actual_column],
        errors="raise"
    )

    forecast_values = pd.to_numeric(
        data[forecast_column],
        errors="raise"
    )

    observed_targets = actual_values.notna().sum()

    valid_pairs = pd.DataFrame({
        "actual": actual_values,
        "forecast": forecast_values
    }).dropna()

    prediction_count = len(valid_pairs)

    if prediction_count == 0:
        return {
            "observed_targets": int(observed_targets),
            "predictions": 0,
            "coverage_pct": np.nan,
            "mae_ngn": np.nan,
            "wape_pct": np.nan,
            "bias_ngn": np.nan,
            "bias_pct": np.nan
        }

    signed_error = (
        valid_pairs["forecast"]
        - valid_pairs["actual"]
    )

    absolute_error = signed_error.abs()
    actual_total = valid_pairs["actual"].abs().sum()

    coverage = (
        prediction_count
        / observed_targets
        * 100
        if observed_targets > 0
        else np.nan
    )

    wape = (
        absolute_error.sum()
        / actual_total
        * 100
        if actual_total > 0
        else np.nan
    )

    bias_percentage = (
        signed_error.sum()
        / actual_total
        * 100
        if actual_total > 0
        else np.nan
    )

    return {
        "observed_targets": int(observed_targets),
        "predictions": prediction_count,
        "coverage_pct": float(coverage),
        "mae_ngn": float(absolute_error.mean()),
        "wape_pct": float(wape),
        "bias_ngn": float(signed_error.mean()),
        "bias_pct": float(bias_percentage)
    }