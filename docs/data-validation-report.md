# Data Validation Report

## Validation Run

| Field | Result |
|---|---|
| Dataset | Nigeria – Food Prices |
| Publisher | World Food Programme |
| Hosting platform | Humanitarian Data Exchange |
| Local file | `wfp_food_prices_nga.csv` |
| Acquisition timestamp | 4 September 2026 at 11:50:01 UTC |
| Validation date | 5 September 2026 |
| File size | 9.49 MiB (9,948,580 bytes) |
| SHA-256 | `b78b4aaefd6aaba6e9bf45eed80e9e6947cf869a716e99f7d135638d868808c9` |
| Raw observations | 81,534 |
| Variables | 16 |
| Date coverage | 15 January 2002 to 15 July 2026 |
| Basic validation result | Passed |

## Reproduction

Run from the repository root:

```powershell
python scripts/download_wfp_data.py
python src/validation.py
python -m pytest tests/test_validation.py -v
```

The validation script creates a machine-readable report at:

```text
data/processed/validation_report.json
```

The generated JSON and downloaded CSV remain local and are excluded from Git.

## Schema Validation

All 16 required variables were present:

- `date`
- `admin1`
- `admin2`
- `market`
- `market_id`
- `latitude`
- `longitude`
- `category`
- `commodity`
- `commodity_id`
- `unit`
- `priceflag`
- `pricetype`
- `currency`
- `price`
- `usdprice`

## Basic Quality Results

| Check | Result |
|---|---:|
| Missing values | 0 |
| Invalid dates | 0 |
| Invalid prices | 0 |
| Zero or negative prices | 0 |
| Exact duplicate rows | 0 |
| Rows with duplicate observation keys | 0 |
| Duplicate observation-key groups | 0 |
| Globally invalid coordinates | 0 |
| Coordinates outside broad Nigeria bounds | 0 |
| Market IDs linked to multiple names | 0 |
| Commodity IDs linked to multiple names | 0 |

No failures were detected by the implemented basic validation checks.

## Dataset Coverage

| Measure | Result |
|---|---:|
| State names represented | 14 |
| Markets represented | 68 |
| Commodities represented | 43 |
| Market–commodity–unit–price-type series | 1,857 |
| Minimum observations per series | 1 |
| Median observations per series | 31 |
| Maximum observations per series | 232 |
| Series with at least 36 observations | 875 |

Only 14 state names are represented, so the dataset does not provide complete national geographic coverage.

Approximately 47.1% of the identified series contain at least 36 observations. Observation count alone does not prove that those series contain uninterrupted monthly histories.

## Observation Types

All observations use Nigerian naira (`NGN`).

| Price type | Observations |
|---|---:|
| Retail | 61,868 |
| Wholesale | 19,666 |

| Price flag | Observations |
|---|---:|
| actual | 47,771 |
| aggregate | 32,646 |
| actual,aggregate | 1,117 |

Retail and wholesale prices must be analysed separately.

Price flags must be retained until their methodological meaning and effect on the analysis have been investigated.

## Measurement Units

The dataset uses multiple measurement units, including:

- Kilograms and fractional kilogram quantities
- 50-kilogram and 100-kilogram quantities
- Litres and millilitres
- Piece counts
- Tuber counts
- The ambiguous label `Unit`

Prices recorded with different measurement units must not be combined without a documented and defensible conversion.

Seventeen commodities are represented using more than one measurement unit.

## Time Structure

Every recorded date falls on the 15th day of its month.

This suggests that the date functions as a monthly reporting timestamp. It should not automatically be interpreted as the exact day on which every market price was observed.

## Geographic Coverage Findings

The preliminary exploratory analysis found:

- Borno had the highest observation coverage with 29,024 records.
- Sokoto had the lowest observation coverage with 576 records.
- Potiskum was the most represented market with 3,664 records.
- Millet was the most represented commodity with 4,753 records.

These are dataset-coverage findings. They do not prove that Borno has Nigeria's largest food market, that Potiskum has the greatest market activity or that millet is Nigeria's most consumed commodity.

## Interpretation

Passing basic validation means that the dataset satisfies the structural and value rules currently implemented.

It does not prove that:

- Every month is present
- Every price is economically reasonable
- Large price movements are genuine
- Data-collection methods are consistent
- Every Nigerian state is represented
- Individual series can be forecast accurately
- A trained model will generalise to future periods

Missing-period detection, outlier investigation and out-of-sample forecasting evaluation are still required.

## Security and Privacy

This report contains only aggregated findings from a public WFP dataset.

It contains no employer, customer, client or confidential information.
