"""Validate the public WFP Nigeria food-price dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "wfp_food_prices_nga.csv"
DEFAULT_REPORT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "validation_report.json"
)

REQUIRED_COLUMNS = [
    "date",
    "admin1",
    "admin2",
    "market",
    "market_id",
    "latitude",
    "longitude",
    "category",
    "commodity",
    "commodity_id",
    "unit",
    "priceflag",
    "pricetype",
    "currency",
    "price",
    "usdprice",
]

OBSERVATION_KEY = [
    "date",
    "market_id",
    "commodity_id",
    "unit",
    "pricetype",
    "currency",
]

BROAD_NIGERIA_BOUNDS = {
    "minimum_latitude": 3.5,
    "maximum_latitude": 14.5,
    "minimum_longitude": 2.0,
    "maximum_longitude": 15.0,
}


def value_counts_as_dict(series: pd.Series) -> dict[str, int]:
    """Convert pandas value counts into JSON-compatible values."""

    counts = series.value_counts(dropna=False)
    return {str(key): int(value) for key, value in counts.items()}


def date_as_text(value: Any) -> str | None:
    """Convert a pandas date into ISO format or return None."""

    if pd.isna(value):
        return None

    return value.date().isoformat()


def load_dataset(path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the raw CSV without modifying the source file."""

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Dataset is empty: {path}")

    dataframe = pd.read_csv(path, low_memory=False)

    if dataframe.empty:
        raise ValueError("The CSV contains no observations.")

    return dataframe


def build_validation_report(
    dataframe: pd.DataFrame,
    source_path: Path = DEFAULT_DATA_PATH,
) -> dict[str, Any]:
    """Validate schema, values, identifiers and basic coverage."""

    missing_columns = sorted(
        set(REQUIRED_COLUMNS) - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing_columns)
        )

    # These converted Series are temporary.
    # The raw DataFrame and source CSV remain unchanged.
    dates = pd.to_datetime(dataframe["date"], errors="coerce")
    prices = pd.to_numeric(dataframe["price"], errors="coerce")
    latitudes = pd.to_numeric(dataframe["latitude"], errors="coerce")
    longitudes = pd.to_numeric(dataframe["longitude"], errors="coerce")

    exact_duplicate_rows = int(dataframe.duplicated().sum())

    logical_duplicate_mask = dataframe.duplicated(
        subset=OBSERVATION_KEY,
        keep=False,
    )

    logical_duplicate_rows = int(logical_duplicate_mask.sum())

    if logical_duplicate_rows:
        logical_duplicate_groups = int(
            dataframe.loc[logical_duplicate_mask]
            .groupby(OBSERVATION_KEY, dropna=False)
            .ngroups
        )
    else:
        logical_duplicate_groups = 0

    market_name_counts = dataframe.groupby("market_id")["market"].nunique()
    commodity_name_counts = dataframe.groupby("commodity_id")[
        "commodity"
    ].nunique()

    globally_invalid_coordinates = int(
        (
            ~latitudes.between(-90, 90)
            | ~longitudes.between(-180, 180)
        ).sum()
    )

    nigeria_bounds = BROAD_NIGERIA_BOUNDS

    coordinates_outside_nigeria_bounds = int(
        (
            ~latitudes.between(
                nigeria_bounds["minimum_latitude"],
                nigeria_bounds["maximum_latitude"],
            )
            | ~longitudes.between(
                nigeria_bounds["minimum_longitude"],
                nigeria_bounds["maximum_longitude"],
            )
        ).sum()
    )

    series_counts = dataframe.groupby(
        ["market_id", "commodity_id", "unit", "pricetype"],
        dropna=False,
    ).size()

    checks = {
        "dataset_not_empty": not dataframe.empty,
        "required_columns_present": not missing_columns,
        "dates_parseable": int(dates.isna().sum()) == 0,
        "prices_numeric": int(prices.isna().sum()) == 0,
        "prices_positive": int(prices.le(0).sum()) == 0,
        "no_exact_duplicates": exact_duplicate_rows == 0,
        "no_logical_duplicates": logical_duplicate_rows == 0,
        "coordinates_globally_valid": globally_invalid_coordinates == 0,
    }

    report = {
        "source": {
            "file_name": source_path.name,
            "file_size_bytes": int(source_path.stat().st_size),
        },
        "dataset": {
            "raw_row_count": int(len(dataframe)),
            "column_count": int(len(dataframe.columns)),
            "earliest_date": date_as_text(dates.min()),
            "latest_date": date_as_text(dates.max()),
        },
        "schema": {
            "required_columns": REQUIRED_COLUMNS,
            "missing_required_columns": missing_columns,
        },
        "quality": {
            "missing_values_by_column": {
                column: int(count)
                for column, count in dataframe.isna().sum().items()
            },
            "invalid_dates": int(dates.isna().sum()),
            "invalid_prices": int(prices.isna().sum()),
            "non_positive_prices": int(prices.le(0).sum()),
            "exact_duplicate_rows": exact_duplicate_rows,
            "logical_duplicate_rows": logical_duplicate_rows,
            "logical_duplicate_groups": logical_duplicate_groups,
            "market_ids_with_multiple_names": int(
                market_name_counts.gt(1).sum()
            ),
            "commodity_ids_with_multiple_names": int(
                commodity_name_counts.gt(1).sum()
            ),
            "globally_invalid_coordinates": globally_invalid_coordinates,
            "coordinates_outside_broad_nigeria_bounds": (
                coordinates_outside_nigeria_bounds
            ),
        },
        "coverage": {
            "state_count": int(dataframe["admin1"].nunique()),
            "market_count": int(dataframe["market_id"].nunique()),
            "commodity_count": int(dataframe["commodity_id"].nunique()),
            "series_count": int(len(series_counts)),
            "minimum_observations_per_series": int(series_counts.min()),
            "median_observations_per_series": float(series_counts.median()),
            "maximum_observations_per_series": int(series_counts.max()),
            "series_with_at_least_36_observations": int(
                series_counts.ge(36).sum()
            ),
        },
        "categories": {
            "currencies": value_counts_as_dict(dataframe["currency"]),
            "price_types": value_counts_as_dict(dataframe["pricetype"]),
            "price_flags": value_counts_as_dict(dataframe["priceflag"]),
            "units": value_counts_as_dict(dataframe["unit"]),
            "observation_days": value_counts_as_dict(dates.dt.day),
        },
        "checks": checks,
        "passes_basic_validation": all(checks.values()),
    }

    return report


def save_report(
    report: dict[str, Any],
    output_path: Path = DEFAULT_REPORT_PATH,
) -> None:
    """Save the validation results without saving cleaned observations."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run validation and print a concise result."""

    dataframe = load_dataset()
    report = build_validation_report(dataframe)
    save_report(report)

    print("Validation complete.")
    print(f"Rows checked: {report['dataset']['raw_row_count']}")
    print(
        "Date coverage:",
        report["dataset"]["earliest_date"],
        "to",
        report["dataset"]["latest_date"],
    )
    print(
        "Passes basic validation:",
        report["passes_basic_validation"],
    )
    print(f"Report saved to: {DEFAULT_REPORT_PATH}")


if __name__ == "__main__":
    main()