\# Security and Privacy Policy

\## Purpose

This document defines the security, privacy and data-handling boundaries for the Nigeria Food Procurement Intelligence Agent.

The project is a public portfolio and decision-support demonstration. All code, documentation, examples and demonstrations must be suitable for public release.

\## Permitted Data

The project may use:

\- Public WFP and Humanitarian Data Exchange datasets

\- Other independently verified public datasets

\- Official Nigerian public-data sources

\- Public documentation and openly available economic information

\- Clearly labelled synthetic procurement baskets

\- Artificial test records created specifically for software testing

Synthetic information must never be presented as observed real-world evidence.

\## Prohibited Data

The project must never contain:

\- Employer information that is not already public

\- Customer or employee information

\- Internal usernames, email addresses or account identifiers

\- Internal IP addresses or hostnames

\- Internal alerts, tickets or investigation records

\- SIEM, endpoint or network logs

\- Internal database information

\- Private architecture or infrastructure relationships

\- Confidential screenshots

\- Internal security controls

\- Private detection rules

\- Confidential vulnerabilities or incidents

\- Client procurement records obtained without permission

\- Credentials, passwords, tokens or API keys

\- Information derived from confidential workplace data

Anonymising confidential workplace information is not sufficient. Such information must not be reused, transformed or published.

\## Approved Demonstration Method

Public demonstrations will use:

\- Verified public food-price data

\- Synthetic business names

\- Synthetic food baskets

\- Synthetic budgets and purchasing deadlines

\- Publicly reproducible model outputs

No real business will be represented as a client unless explicit written permission has been obtained.

\## Data Storage

Downloaded raw data is stored locally under `data/raw/`.

Generated processed data is stored locally under `data/processed/`.

Both locations are excluded from Git. The repository stores acquisition code and documentation instead of downloaded datasets.

\## Secrets Management

Secrets must not be written directly into source code, notebooks or committed configuration files.

If an API key is required later, it must be:

\- Stored in a local `.env` file

\- Loaded through an environment variable

\- Represented publicly only through `.env.example`

\- Excluded from Git

\- Revoked immediately if accidentally exposed

Before every commit, `git status` should be inspected to confirm that no secret or unintended file is staged.

\## Data Integrity

The acquisition process records:

\- Dataset source

\- Download timestamp

\- File size

\- File name

\- SHA-256 checksum

The checksum helps identify whether the downloaded file has changed. It does not prove that the publisher’s data is accurate.

Raw source files must not be silently edited. Cleaning and transformation must produce separate processed outputs.

\## Model and Recommendation Safety

Forecasts are estimates, not facts.

The system must:

\- Explain important limitations

\- Report uncertainty where possible

\- Identify insufficient data

\- Avoid guaranteed price claims

\- Separate observed data from model predictions

\- Separate predictions from procurement recommendations

\- Allow the user to reject every recommendation

The application must not autonomously purchase goods, contact suppliers or transfer money.

\## AI-Agent Safety

If an AI-agent layer is added later, it must:

\- Use only approved tools

\- Validate structured outputs

\- Log tool calls and failures

\- Treat retrieved documents as untrusted input

\- Resist prompt-injection instructions contained in data

\- Escalate uncertain decisions to a human

\- Avoid inventing prices, suppliers or dataset observations

\- Require human approval before any external action

\- Provide fallback behaviour when tools fail

The language model will explain and coordinate validated analytical outputs. It will not replace the underlying data-validation, forecasting or optimisation logic.

\## Responsible Interpretation

The public dataset may be incomplete, delayed or unevenly distributed across locations and commodities.

Results must not be presented as:

\- Guaranteed future prices

\- Real-time supplier quotations

\- Financial advice

\- Evidence about a specific business

\- Proof that a market condition currently exists

\- A replacement for human procurement judgement

\## Pre-Commit Safety Check

Before pushing work to GitHub, confirm that:

\- Only public or synthetic data is used

\- Synthetic examples are clearly labelled

\- No confidential identifiers are present

\- No credentials or API keys are present

\- Raw and processed datasets remain excluded

\- Charts reveal no private information

\- Notebook outputs contain no unintended data

\- Documentation does not describe private workplace systems

\- Model claims match the available evidence

\- The final decision remains human-controlled

\## Response to Accidental Exposure

If a credential or confidential record is accidentally committed:

1\. Stop further sharing.

2\. Revoke or rotate the exposed credential immediately.

3\. Identify every affected file and commit.

4\. Remove the material from Git history using an appropriate history-cleaning process.

5\. Review remote copies, forks, releases and automated logs.

6\. Document the cause and introduce a preventive control.

Deleting only the latest visible file is not sufficient because older Git commits may still contain the information.
