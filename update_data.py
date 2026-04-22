
import yfinance as yf
import pandas as pd
import json
import re
import os

# ── 1. Fetch data ────────────────────────────────────────────────────────────
TICKERS = ["SPY", "^VIX9D", "^VIX", "SPMO", "SPLV"]
print("Fetching price data from Yahoo Finance...")

raw = yf.download(TICKERS, period="5y", auto_adjust=True, progress=False)["Close"]
raw.columns = ["SPMO", "SPY", "SPLV", "VIX", "VIX9D"]   # yfinance sorts alphabetically
raw = raw.dropna(subset=["SPY", "VIX9D", "VIX", "SPMO", "SPLV"])
raw = raw.sort_index()

# ── 2. Compute VIX9D/VIX signals ─────────────────────────────────────────────
df = pd.DataFrame()
df["date"]      = raw.index
df["spy"]       = raw["SPY"].values
df["spy_pct"]   = raw["SPY"].pct_change().values * 100
df["vix9d"]     = raw["VIX9D"].values
df["vix"]       = raw["VIX"].values
df["spmo"]      = raw["SPMO"].values
df["splv"]      = raw["SPLV"].values

df["vix_ratio"] = df["vix9d"] / df["vix"]
df["spm_ratio"] = df["spmo"] / df["splv"]

# VIX velocity
df["vix_vel"]   = df["vix_ratio"].diff()
df["vix_vel5"]  = df["vix_ratio"].diff(5) / 5

# SPMO velocity
df["spm_vel"]   = df["spm_ratio"].diff()
df["spm_vel5"]  = df["spm_ratio"].diff(5) / 5

# SPMO Z-score (20-day rolling)
df["spm_mean20"] = df["spm_ratio"].rolling(20).mean()
df["spm_std20"]  = df["spm_ratio"].rolling(20).std()
df["spm_zscore"] = (df["spm_ratio"] - df["spm_mean20"]) / df["spm_std20"]

# Signal labels
def vix_signal(r):
    if pd.isna(r):   return "Neutral"
    if r < 0.95:     return "Bullish"
    if r > 1.05:     return "Bearish"
    return "Neutral"

def spm_signal(z):
    if pd.isna(z):   return "Neutral"
    if z > 1.0:      return "Bullish"
    if z < -1.0:     return "Bearish"
    return "Neutral"

df["vix_signal"] = df["vix_ratio"].apply(vix_signal)
df["spm_signal"] = df["spm_zscore"].apply(spm_signal)

# ── 3. Build JSON records ─────────────────────────────────────────────────────
def f(v, dec=4):
    """Round float or return None if NaN."""
    try:
        return None if pd.isna(v) else round(float(v), dec)
    except Exception:
        return None

records = []
for _, row in df.iterrows():
    records.append({
        "d":    row["date"].strftime("%Y-%m-%d"),
        "spy":  f(row["spy"], 2),
        "spy_pct": f(row["spy_pct"], 2),
        "vr":   f(row["vix_ratio"]),
        "vv":   f(row["vix_vel"]),
        "vv5":  f(row["vix_vel5"]),
        "vs":   row["vix_signal"],
        "vix9d": f(row["vix9d"], 2),
        "vix":  f(row["vix"], 2),
        "sr":   f(row["spm_ratio"]),
        "sz":   f(row["spm_zscore"], 3),
        "sv":   f(row["spm_vel"]),
        "sv5":  f(row["spm_vel5"]),
        "ss":   row["spm_signal"],
        "spmo": f(row["spmo"], 2),
        "splv": f(row["splv"], 2),
    })

print(f"Built {len(records)} records. Latest date: {records[-1]['d']}")

# ── 4. Inject into index.html ─────────────────────────────────────────────────
html_path = os.path.join(os.path.dirname(__file__), "index.html")

with open(html_path, "r", encoding="utf-8") as fh:
    html = fh.read()

new_json = json.dumps(records)

# Replace the data block — matches: const RAW = [...];
updated = re.sub(
    r"const RAW = \[.*?\];",
    f"const RAW = {new_json};",
    html,
    count=1,
    flags=re.DOTALL,
)

if updated == html:
    print("WARNING: Could not find 'const RAW = [...]' in index.html — no changes written.")
else:
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(updated)
    print(f"index.html updated successfully ({len(records)} rows).")
