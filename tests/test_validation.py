"""Automated tests for the food-price validation module."""

from pathlib import Path

import pandas as pd
import pytest

from src.validation import build_validation_report, load_dataset


@pytest.fixture
def valid_dataframe() -> pd.DataFrame:
    """Create a small synthetic dataset with valid values."""

    return pd.DataFrame(
        [
            {
                "date": "2024-01-15",
                "admin1": "Lagos",
                "admin2": "Ikeja",
                "market": "Synthetic Test Market",
                "market_id": 1,
                "latitude": 6.60,
                "longitude": 3.35,
                "category": "cereals and tubers",
                "commodity": "Rice",
                "commodity_id": 64,
                "unit": "KG",
                "priceflag": "actual",
                "pricetype": "Retail",
                "currency": "NGN",
                "price": 1000.00,
                "usdprice": 1.00,
            },
            {
                "date": "2024-02-15",
                "admin1": "Lagos",
                "admin2": "Ikeja",
                "market": "Synthetic Test Market",
                "market_id": 1,
                "latitude": 6.60,
                "longitude": 3.35,
                "category": "cereals and tubers",
                "commodity": "Rice",
                "commodity_id": 64,
                "unit": "KG",
                "priceflag": "actual",
                "pricetype": "Retail",
                "currency": "NGN",
                "price": 1100.00,
                "usdprice": 1.10,
            },
        ]
    )


def write_sample_csv(
    dataframe: pd.DataFrame,
    temporary_directory: Path,
) -> Path:
    """Write a synthetic CSV used only during a test."""

    path = temporary_directory / "sample.csv"
    dataframe.to_csv(path, index=False)
    return path


def test_valid_dataframe_passes(
    valid_dataframe: pd.DataFrame,
    tmp_path: Path,
) -> None:
    """A complete valid dataset should pass basic validation."""

    source_path = write_sample_csv(valid_dataframe, tmp_path)

    report = build_validation_report(
        valid_dataframe,
        source_path,
    )

    assert report["passes_basic_validation"] is True
    assert report["dataset"]["raw_row_count"] == 2
    assert report["quality"]["invalid_dates"] == 0
    assert report["quality"]["invalid_prices"] == 0


def test_missing_required_column_raises_error(
    valid_dataframe: pd.DataFrame,
    tmp_path: Path,
) -> None:
    """A missing required column should stop validation."""

    invalid_dataframe = valid_dataframe.drop(columns=["price"])
    source_path = write_sample_csv(invalid_dataframe, tmp_path)

    with pytest.raises(
        ValueError,
        match="Missing required columns: price",
    ):
        build_validation_report(
            invalid_dataframe,
            source_path,
        )


def test_non_positive_price_fails_validation(
    valid_dataframe: pd.DataFrame,
    tmp_path: Path,
) -> None:
    """A zero or negative price should fail validation."""

    invalid_dataframe = valid_dataframe.copy()
    invalid_dataframe.loc[0, "price"] = 0
    source_path = write_sample_csv(invalid_dataframe, tmp_path)

    report = build_validation_report(
        invalid_dataframe,
        source_path,
    )

    assert report["passes_basic_validation"] is False
    assert report["quality"]["non_positive_prices"] == 1


def test_logical_duplicate_is_detected(
    valid_dataframe: pd.DataFrame,
    tmp_path: Path,
) -> None:
    """Two records with the same observation key should be detected."""

    duplicate = valid_dataframe.iloc[[0]].copy()
    duplicate["price"] = 99999.00

    invalid_dataframe = pd.concat(
        [valid_dataframe, duplicate],
        ignore_index=True,
    )

    source_path = write_sample_csv(invalid_dataframe, tmp_path)

    report = build_validation_report(
        invalid_dataframe,
        source_path,
    )

    assert report["passes_basic_validation"] is False
    assert report["quality"]["exact_duplicate_rows"] == 0
    assert report["quality"]["logical_duplicate_rows"] == 2
    assert report["quality"]["logical_duplicate_groups"] == 1


def test_impossible_coordinate_fails_validation(
    valid_dataframe: pd.DataFrame,
    tmp_path: Path,
) -> None:
    """A globally impossible latitude should fail validation."""

    invalid_dataframe = valid_dataframe.copy()
    invalid_dataframe.loc[0, "latitude"] = 100.00
    source_path = write_sample_csv(invalid_dataframe, tmp_path)

    report = build_validation_report(
        invalid_dataframe,
        source_path,
    )

    assert report["passes_basic_validation"] is False
    assert report["quality"]["globally_invalid_coordinates"] == 1


def test_empty_file_is_rejected(tmp_path: Path) -> None:
    """An empty CSV file should be rejected before parsing."""

    empty_path = tmp_path / "empty.csv"
    empty_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Dataset is empty"):
        load_dataset(empty_path)