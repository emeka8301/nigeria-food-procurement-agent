\# Problem Definition

\## Project

Nigeria Food Procurement Intelligence Agent

\## Background

Nigerian restaurants, caterers and small food retailers must purchase food commodities while managing changing prices, limited budgets and purchasing deadlines.

Procurement decisions may depend on recent supplier prices, informal market knowledge and manual comparisons. Historical public data could provide additional evidence about price movements, seasonality and uncertainty.

This project treats that business need as a hypothesis to be tested. Direct interviews with Nigerian food businesses would still be required before claiming that the final product solves their complete procurement process.

\## Decision to Improve

The system should help a user answer:

> Given my food basket, budget, preferred location and purchasing deadline, which commodities should I buy now, monitor or postpone?

The system will provide decision support. It will not make purchases or guarantee future prices.

\## Intended Users

The initial users are:

\- Small restaurants

\- Caterers

\- Food retailers

\- Procurement officers in small food businesses

\- Business owners who purchase recurring food supplies

\## Current Project Inputs

The first version will use:

\- Public historical food-price observations

\- Market and geographic information

\- Commodity names and measurement units

\- Retail or wholesale price classifications

\- User-selected purchasing deadlines

\- Clearly labelled synthetic procurement baskets

No employer, customer or confidential information will be used.

\## Expected Outputs

The completed system should provide:

\- Historical price trends

\- Data-quality and coverage warnings

\- Short-term forecasting estimates

\- Forecast uncertainty

\- Buy, monitor or postpone recommendations

\- Reasons supporting each recommendation

\- Human approval before any proposed action

\## Main Questions

The project should answer:

1\. Which Nigerian markets and commodities have sufficient historical coverage?

2\. How have selected food prices changed over time?

3\. Are recurring seasonal patterns visible?

4\. How accurately do simple forecasting baselines perform?

5\. Can a more advanced model improve meaningfully on those baselines?

6\. How should forecast uncertainty affect a procurement recommendation?

7\. When is the available evidence too weak to support a recommendation?

\## Minimum Viable Product Scope

The first complete version will:

\- Reproducibly acquire the public dataset

\- Validate its structure and important variables

\- Analyse market and commodity coverage

\- Select a small number of suitable pilot series

\- Compare transparent forecasting baselines

\- Evaluate forecasts using chronological testing

\- Produce simple procurement recommendations

\- Explain the evidence and uncertainty

\- Provide a small public demonstration application

\## Out of Scope

The first version will not:

\- Guarantee future market prices

\- Execute purchases

\- Recommend specific suppliers

\- Use private client procurement records

\- Estimate food quality

\- Claim to provide real-time prices

\- Replace supplier quotations

\- Optimise delivery routes

\- Include confidential employer or customer data

\## Analytical Framing

For a selected commodity and market, the project will model price observations over time.

A useful model must improve on simple alternatives such as:

\- Using the most recently observed price

\- Using the median of the previous three observations

\- Using the price observed during the same period in the previous year

Recommendations will consider expected price movement, uncertainty and data quality. A forecast will not automatically become a recommendation.

\## Success Criteria

The project will be considered successful when:

\- Data acquisition is reproducible

\- Data-quality failures are detected and documented

\- Raw and processed data remain excluded from Git

\- Forecasting uses chronological rather than random evaluation

\- Advanced models are compared against honest baselines

\- Recommendations include uncertainty and limitations

\- The system can refuse to recommend when evidence is insufficient

\- A user remains responsible for the final procurement decision

\- No employer, client or confidential information is present

\## Key Limitations

The public dataset may contain:

\- Missing months

\- Uneven geographic coverage

\- Different commodity units

\- Retail and wholesale observations

\- Delayed observations

\- Market-level rather than supplier-level prices

\- No transport, storage or food-quality information

These limitations must be considered before interpreting model results.
