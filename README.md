Risk Indicator Dashboard
A tactical market risk monitoring dashboard tracking two complementary short-term indicators — VIX9D/VIX ratio and SPMO/SPLV ratio — alongside SPY price, with velocity analysis on both. Auto-updates every weekday after US market close.
Live dashboard → (your Vercel URL here)
---
What It Shows
Panel	What It Measures	Horizon
SPY Price	S&P 500 ETF price context	—
VIX9D / VIX Ratio	Short-term vs longer-term implied volatility	1–3 days
VIX9D / VIX Velocity	Rate of change in the ratio (acceleration)	Same day
SPMO / SPLV Ratio + Z-Score	Momentum vs low-volatility factor leadership	Weekly
SPMO / SPLV Velocity	Rate of change in factor rotation	Same day
Each indicator fires independently. Agreement between them raises conviction. Divergence flags ambiguity.
---
Signal Logic
VIX9D / VIX Ratio
Bullish → ratio < 0.95 (short-term fear lower than medium-term; market calm, risk-on)
Neutral → ratio 0.95–1.05
Bearish → ratio > 1.05 (short-term fear elevated vs medium-term; stress building)
SPMO / SPLV Z-Score (20-day rolling)
Bullish → Z-Score > +1.0 (momentum stocks leading defensives; risk-on regime)
Neutral → Z-Score between −1.0 and +1.0
Bearish → Z-Score < −1.0 (defensives leading momentum; risk-off rotation)
Velocity (both indicators)
The bars show the 1-day change in the ratio (green = rising, red = falling)
The amber line shows the 5-day average rate of change
When the bar is larger than the line, the move is accelerating
When the bar is smaller, the move is decelerating
---
Reading the Last 3 Readings Panel
Each indicator shows the current reading plus the previous two days, so you can see direction at a glance without reading the full chart:
Current card has a blue border
Each card shows: ratio value, underlying prices, signal badge, 1-day velocity, and 5-day average velocity
Green arrow (▲) = ratio rose from prior day; Red arrow (▼) = ratio fell
---
Highest-Conviction Scenarios
VIX Signal	SPMO Signal	Read
Bullish	Bullish	Strong risk-on — both short-term calm and factor rotation confirm
Bearish	Bearish	Strong risk-off — fear elevated and defensives leading
Bullish	Bearish	Mixed — calm surface but defensive rotation underneath; caution
Bearish	Bullish	Mixed — fear spike but momentum still leading; may be short-lived
---
Date Range Buttons
Button	Shows
3M	Last 90 days — useful for recent regime context
6M	Last 180 days — a full market cycle in most conditions
1Y	Default — balances history with readability
ALL	Full dataset from April 2021
---
Repo Structure
```
├── index.html                          # Dashboard (auto-updated by GitHub Actions)
├── update_data.py                      # Fetches prices and rebuilds data in index.html
├── vercel.json                         # Tells Vercel to serve as a static site
├── .github/
│   └── workflows/
│       └── update_dashboard.yml        # Runs update_data.py weekdays at 5:30pm ET
└── README.md                           # This file
```
---
How Auto-Update Works
GitHub Actions triggers at 21:30 UTC (5:30pm ET) every Monday–Friday
`update_data.py` fetches the latest prices for SPY, VIX9D, VIX, SPMO, SPLV from Yahoo Finance (free, no API key required)
All ratios, signals, Z-scores, and velocities are recomputed
The data inside `index.html` is replaced and committed back to the repo
Vercel detects the new commit and redeploys — usually live within 30 seconds
To trigger a manual update at any time: go to the Actions tab in GitHub → select Update Dashboard Data → click Run workflow.
---
Data Sources
All prices are fetched via yfinance from Yahoo Finance:
Ticker	Description
SPY	SPDR S&P 500 ETF
^VIX9D	CBOE 9-Day Volatility Index
^VIX	CBOE 30-Day Volatility Index
SPMO	Invesco S&P 500 Momentum ETF
SPLV	Invesco S&P 500 Low Volatility ETF
---
Important Notes
Signals are shown on a 1-day lag — yesterday's indicator reading is compared to today's SPY move
The Z-score uses a 20-day rolling window — it resets context roughly every month
VIX9D/VIX is a short-term trigger; SPMO/SPLV is a slower regime read — they are designed to complement, not replace, each other
No single signal should be used in isolation; look for convergence across both indicators and velocity
