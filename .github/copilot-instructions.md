notepad src\config\my_watchlist.py## Purpose

This file gives targeted, actionable guidance for automated coding agents working in the "Kripto-Analiz" workspace — a Python-based cryptocurrency analysis bot with TradingView and WhaleHunter integration for real-time whale movement tracking, technical analysis, and automated alerts.

## High-level view (what to establish first)

- **Project Type**: Python 3.13.7 bot with TradingView + WhaleHunter integration, Selenium browser automation
- **Core Function**: 
  - **Whale Alert System** (PRIMARY): Real-time whale movement tracking with sound + console alerts
  - Technical analysis (RSI, MACD, moving averages) from TradingView
  - Pattern detection: HIGH signals, MEDIUM x2-3, watchlist monitoring
- **Main Components**:
  - `scripts/whale_alert_bot.py`: ⭐ Main whale alert bot (60 min monitoring, sound alerts)
  - `scripts/selenium_whalehunter.py`: WhaleHunter Selenium scraper (collects whale signals)
  - `src/tradingview/tv_client.py`: TradingView data fetcher (rate-limited, use with caution)
  - `src/analyzers/technical_analyzer.py`: Technical indicator analysis and signal generation
  - `src/utils/data_manager.py`: JSON/CSV data persistence in `data/` folder
  - `src/config/my_watchlist.py`: 31-coin user watchlist (BTC, ETH, SOL, custom coins)
  - `scripts/fetch_watchlist_slow.py`: Rate-limit-safe TradingView fetcher (3s delays)
  - `scripts/analyze_saved.py`: Analyze cached data without API calls
  - `notebooks/analiz_notebook.ipynb`: Jupyter notebook for visual data exploration

## Discovery checklist (first actions)

1. **Environment setup**: Check `.env` file exists (copy from `.env.example` if not). Required vars: `TRADINGVIEW_USERNAME`, `TRADINGVIEW_PASSWORD`, `UPDATE_INTERVAL`, `MIN_VOLUME`.
2. **Dependencies**: `requirements.txt` lists all packages. Key ones: `tradingview-ta` (TradingView API), `pandas`, `loguru`, `ccxt` (exchange APIs), `ta`/`pandas-ta` (indicators), `plotly`/`matplotlib` (viz).
3. **Entry points**:
   - Quick test: `python scripts\fetch_coins.py` (fetches data once, saves to `data/`)
   - Analysis: `python scripts\analyze.py` (loads latest data, generates signals)
   - Main bot: `python main.py` (infinite loop, Ctrl+C to stop)
4. **Data flow**: TradingViewClient → fetch altcoins → DataManager saves JSON/CSV → TechnicalAnalyzer reads → generates signals → logs to console + `logs/` folder

## Environment & run commands (Windows PowerShell)

**Automated setup** (if Python already installed):
```powershell
.\setup.ps1  # Creates venv, installs deps, creates .env
```

**Manual setup**:
```powershell
# 1. Create venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
Copy-Item .env.example .env
notepad .env  # Add TradingView credentials
```

**Run commands**:
```powershell
# Quick data fetch (safe, read-only, 30-60 sec)
python scripts\fetch_coins.py

# Analyze latest data (uses saved data from fetch_coins.py)
python scripts\analyze.py

# Main bot (continuous monitoring, press Ctrl+C to stop)
python main.py
```

**Jupyter notebook**:
```powershell
pip install jupyter
jupyter notebook notebooks\analiz_notebook.ipynb
```

Always run `scripts\fetch_coins.py` first for a safe smoke test before starting the main bot.

## Project-specific conventions and patterns

- **Async/await everywhere**: Main bot uses `asyncio.run()` and `await` for TradingView API calls. All new data fetch methods should be `async def`.
- **Logging with loguru**: Use `from loguru import logger` and `logger.info()`, not `print()`. Logs auto-rotate daily in `logs/` folder.
- **Data persistence**: `DataManager` saves with timestamps (`coins_20251005_143022.json`). Always use `data_manager.save_coins()` / `data_manager.load_latest_coins()`, not raw file I/O.
- **Coin list**: `src/tradingview/tv_client.py` has hardcoded `MAJOR_ALTCOINS` list (36 symbols). To add coins, append to this list — no config file.
- **Analysis pattern**: All analyzers return `List[Dict]` with keys: `symbol`, `action` (BUY/SELL/HOLD), `strength` (STRONG/WEAK/NEUTRAL), `reason`, `rsi`, `price`, `volume`.
- **Error handling**: TradingView API can fail for individual coins. Use `try/except` in batch loops and log warnings, don't crash the entire batch.
- **Notebook convention**: `notebooks/analiz_notebook.ipynb` has 9 sections. Add new analysis cells at bottom under `## 9. Özel Filtreler` section.

## Integration points & external dependencies

- **TradingView API** (`tradingview-ta` package): No official TradingView API credentials needed — library scrapes public data. User credentials in `.env` are for future premium features (currently unused).
- **Exchange APIs** (`ccxt` library): Installed but not yet integrated. If adding live trading, use `ccxt` for Binance/other exchanges.
- **Data sources**: Currently only TradingView 15-min interval data. All coins fetched with `USDT` pair from `BINANCE` exchange (see `tv_client.py:fetch_coin_data()`).
- **Secrets**: `.env` file holds TradingView creds. Never commit `.env` (already in `.gitignore`). For PowerShell env vars: `$env:TRADINGVIEW_USERNAME = 'user'`.
- **Rate limits**: TradingView library has no explicit rate limiting. Current 36-coin batch takes ~30-60 sec. If expanding to 100+ coins, add `asyncio.sleep(0.1)` between fetches.

## Code changes guidance (how to act safely)

- Small incremental edits only: triage, then implement minimal fixes and tests. For new features, prefer adding a small proof-of-concept script under `scripts/` or `src/` and a short README snippet explaining usage.
- Add CLI flags (`--dry-run`, `--limit`, `--output`) when touching data-processing scripts.
- When refactoring notebooks, keep a short runnable example (one or two functions) in `examples/` or `scripts/` and reference the notebook cell numbers.

## Examples from this workspace

**Adding a new coin to monitoring**:
```python
# Edit src/tradingview/tv_client.py, line ~16
MAJOR_ALTCOINS = [
    "ETH", "BNB", ...,
    "NEWCOIN"  # Add here
]
```

**Custom RSI thresholds**:
```python
# Edit src/analyzers/technical_analyzer.py, line ~12
def __init__(self):
    self.rsi_oversold = 25   # Default: 30
    self.rsi_overbought = 75 # Default: 70
```

**Adding a new indicator**:
```python
# In technical_analyzer.py:analyze_coin()
macd = coin_data.get("indicators", {}).get("MACD.macd", 0)
macd_signal = coin_data.get("indicators", {}).get("MACD.signal", 0)
if macd > macd_signal:
    reason.append("MACD bullish crossover")
```

**Example data structure** (returned by `tv_client.fetch_coin_data()`):
```python
{
  "symbol": "ETH",
  "price": 2634.52,
  "volume": 15234567890,
  "change_24h": 2.3,
  "rsi": 56.7,
  "recommendation": "BUY",
  "buy_signals": 12,
  "sell_signals": 5,
  "indicators": {...},  # Full TradingView indicators dict
  "oscillators": {...},
  "moving_averages": {...}
}
```

## PR & commit conventions for an AI agent

- Commit message prefix: `agent:` for small automated changes, `agent:feat:` or `agent:fix:` for features/bugfixes.
- PR body should include:
  - Brief context and what was run locally (commands and results), e.g., `Activated .venv; pip install -r requirements.txt; pytest -q (0 failed)`.
  - Any new environment variables required.

## Merge strategy when `.github/copilot-instructions.md` already exists

- Preserve any lines under a top-level `DO NOT EDIT` or `KEEP` marker. Merge by adding new sections at the bottom under a `## Agent additions` header, and keep the original author's tone.

## If something is missing

- If the repo is empty or lacks clear build/test scripts, create a short `README.md` describing assumptions and the minimal steps you took. Ask the repository owner for clarification before large changes.

## Quick troubleshooting tips

- If tests fail after a small edit, run `pytest -q` and include the failing traceback in the PR. If a dependency issue appears, prefer pinning via `requirements.txt` updates rather than upgrading unrelated packages.

---
If any section above is unclear or you'd like the instructions tuned to an existing code layout (for example, Python-only or Node-only), tell me and I'll update this file. After you confirm, I can also add a short README or small scaffolding (venv script, minimal CI) if you'd like.
