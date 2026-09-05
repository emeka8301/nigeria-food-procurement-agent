# Data Documentation

## Overview

This directory contains documentation and local storage locations for the public datasets used by the Nigeria Food Procurement Intelligence Agent.

Raw and processed datasets are deliberately excluded from Git because they can be downloaded or reproduced from their original public sources.

## Core Dataset

### Nigeria – Food Prices

| Field | Details |
|---|---|
| Dataset name | Nigeria – Food Prices |
| Original publisher | World Food Programme |
| Hosting platform | Humanitarian Data Exchange |
| Source classification | Official WFP dataset hosted by HDX |
| Country | Nigeria |
| Dataset ID | `42db041f-7aaf-4ab4-961f-2a12096861e7` |
| Food-price resource ID | `12b51155-0cd3-4806-9924-61ede4077591` |
| Format | CSV with Humanitarian Exchange Language tags |
| Approximate size | Approximately 6–7 MB; exact size is recorded after each download |
| Time coverage | 15 January 2002 to 15 April 2026 |
| Expected update frequency | Monthly, although actual updates may occur more or less frequently |
| Latest source-page modification observed | 30 August 2026 |
| Licence | Creative Commons Attribution for Intergovernmental Organisations |
| Access date | 4 September 2026 |

### Source Page

https://data.humdata.org/dataset/wfp-food-prices-for-nigeria

### Direct CSV Resource

https://data.humdata.org/dataset/42db041f-7aaf-4ab4-961f-2a12096861e7/resource/12b51155-0cd3-4806-9924-61ede4077591/download/wfp_food_prices_nga.csv

## Important Variables

The source data is expected to include variables representing:

- observation date;
- first-level administrative area or state;
- second-level administrative area where available;
- market name;
- market coordinates;
- commodity category;
- commodity name;
- measurement unit;
- actual or aggregated price flag;
- retail or wholesale price type;
- currency;
- local-currency price;
- US-dollar price where available.

The acquisition and validation scripts will verify the actual column names rather than assuming that the schema has remained unchanged.

## Intended Use

The dataset will be used to:

1. measure historical price coverage across Nigerian states and markets;
2. identify commodities with sufficiently complete monthly histories;
3. analyse price trends, variability and missing periods;
4. establish transparent forecasting baselines;
5. support a later risk-aware procurement optimisation system;
6. provide evidence to a later AI-agent workflow.

A forecast will be treated as uncertain decision-support evidence, not as a guaranteed future price.

## Known Limitations

- Market coverage is not uniform across Nigeria.
- Some commodities have missing months.
- Different commodities may use kilograms, litres, units, baskets or large wholesale bags.
- Retail and wholesale prices must not be combined without justification.
- Actual and aggregated prices may represent different observation processes.
- Market names and administrative labels may change over time.
- Extreme price movements may be genuine economic events or data-quality problems.
- Public prices do not include supplier reliability, product quality, transportation costs, storage costs or quantity discounts.
- Historical price relationships may change because of inflation, exchange-rate movements, insecurity, fuel prices, climate events and policy changes.
- The dataset is not a live quotation service and should not be presented as one.

## Data-Handling Rules

- Do not commit raw CSV files.
- Do not commit processed datasets that can be reproduced.
- Preserve the original raw file without manual editing.
- Store cleaning logic in scripts or notebooks.
- Record the download date, row count, file size and checksum.
- Document every exclusion, conversion and imputation rule.
- Do not silently remove missing values, duplicates or extreme observations.
- Do not combine incompatible measurement units.
- Do not include employer, customer or client information.

## Directory Structure

```text
data/
├── README.md
├── raw/
│   └── .gitkeep
└── processed/
    └── .gitkeep

```

## Dataset Acquisition

Activate the project environment and run:

```powershell
python scripts/download_wfp_data.py
```

The acquisition script downloads the public CSV into `data/raw/`, records acquisition metadata and calculates a SHA-256 checksum. Downloaded files remain local and are excluded from Git.

## Attribution

This project uses the Nigeria Food Prices dataset published by the World Food Programme and distributed through the Humanitarian Data Exchange. Any public use of the dataset and resulting analysis should preserve the publisher attribution and comply with the stated licence.
