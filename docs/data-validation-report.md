\# Data Validation Report

\## Validation Run

| Field | Result |

|---|---|

| Dataset | Nigeria – Food Prices |

| Publisher | World Food Programme |

| Hosting platform | Humanitarian Data Exchange |

| Local file | `wfp\_food\_prices\_nga.csv` |

| Acquisition timestamp | 4 September 2026 at 11:50:01 UTC |

| Validation date | 5 September 2026 |

| File size | 9.49 MiB (9,948,580 bytes) |

| SHA-256 | `b78b4aaefd6aaba6e9bf45eed80e9e6947cf869a716e99f7d135638d868808c9` |

| Raw observations | 81,534 |

| Variables | 16 |

| Date coverage | 15 January 2002 to 15 July 2026 |

| Basic validation result | Passed |

\## Reproduction

Run the following commands from the repository root:

```powershell

python scripts/download\_wfp\_data.py

python src/validation.py

python -m pytest tests/test\_validation.py -v
