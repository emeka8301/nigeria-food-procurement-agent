"""Download the public WFP Nigeria food-price dataset."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests


SOURCE_URL = (
    "https://data.humdata.org/dataset/"
    "42db041f-7aaf-4ab4-961f-2a12096861e7/resource/"
    "12b51155-0cd3-4806-9924-61ede4077591/download/"
    "wfp_food_prices_nga.csv"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIRECTORY = PROJECT_ROOT / "data" / "raw"
DATA_PATH = RAW_DIRECTORY / "wfp_food_prices_nga.csv"
METADATA_PATH = RAW_DIRECTORY / "wfp_food_prices_nga.metadata.json"
TEMPORARY_PATH = RAW_DIRECTORY / "wfp_food_prices_nga.csv.part"

CHUNK_SIZE = 1024 * 1024


def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 checksum of a file."""
    checksum = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b""):
            checksum.update(chunk)

    return checksum.hexdigest()


def download_data() -> None:
    """Download the dataset and record acquisition metadata."""
    RAW_DIRECTORY.mkdir(parents=True, exist_ok=True)

    if DATA_PATH.exists():
        print(f"Dataset already exists: {DATA_PATH}")
        print("The existing raw file was not overwritten.")
        return

    headers = {
        "User-Agent": "nigeria-food-procurement-agent/0.1"
    }

    try:
        with requests.get(
            SOURCE_URL,
            headers=headers,
            timeout=60,
            stream=True,
        ) as response:
            response.raise_for_status()

            with TEMPORARY_PATH.open("wb") as file:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        file.write(chunk)

        TEMPORARY_PATH.replace(DATA_PATH)

    except Exception:
        if TEMPORARY_PATH.exists():
            TEMPORARY_PATH.unlink()
        raise

    metadata = {
        "dataset": "Nigeria - Food Prices",
        "publisher": "World Food Programme",
        "platform": "Humanitarian Data Exchange",
        "source_url": SOURCE_URL,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "file_name": DATA_PATH.name,
        "file_size_bytes": DATA_PATH.stat().st_size,
        "sha256": calculate_sha256(DATA_PATH),
    }

    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print(f"Downloaded: {DATA_PATH}")
    print(f"Size: {DATA_PATH.stat().st_size:,} bytes")
    print(f"Metadata: {METADATA_PATH}")


if __name__ == "__main__":
    download_data()