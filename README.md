# PowerTrader_AI
Fully automated crypto spot trading powered by a custom price-prediction AI and a structured, tiered DCA system.

## What Is Different In This Fork
This repository is a fork of the original PowerTrader_AI, which was built around Robinhood Crypto.
This fork keeps the AI/trading philosophy, but rewires the live trading stack for KuCoin spot trading.

Main fork differences:

- Live trading in `pt_trader.py` uses KuCoin REST API with HMAC-SHA256 signing.
- The Hub stores and reads runtime data from `hub_data/`:
  - `trader_status.json`
  - `trade_history.jsonl`
  - `pnl_ledger.json`
  - `account_value_history.jsonl`
  - `runner_ready.json`
- `pt_hub.py` starts the neural runner first and only starts the trader after the runner reports real readiness.
- Training freshness is enforced. A coin is not considered ready just because files exist; it must have a recent training timestamp.
- DCA, trailing-profit, and start-allocation settings are controlled from the Hub and hot-reloaded by the trader.
- The trader keeps a local pending-order ledger so startup/restarts can reconcile unfinished orders safely.
- Very old unresolved pending orders are quarantined into `stale_pending` instead of blocking startup forever.
- `stale_pending` orders can be audited and repaired later from KuCoin order history using the order id as the source of truth.
- Trade history and realized/open-position accounting are written locally for GUI display and restart recovery.
- Telegram trade notifications can be configured from the Hub for confirmed BUY, DCA BUY, and SELL events.
- Dust positions are ignored for fresh-entry blocking and for most DCA/trailing decisions.
- Trailing exits have a short-lived retry intent so a temporary API hiccup does not immediately waste a profitable exit.

Important:
KuCoin order history is the source of truth.
The local `hub_data` files are the bot's working ledger/cache layer for the GUI and restart recovery.

Useful recovery commands in this fork:

- `python pt_trader.py --audit-stale-orders`
  Dry-run audit of `stale_pending` against KuCoin order history.
- `python pt_trader.py --repair-stale-orders`
  Backfills confirmed missing trades from `stale_pending` into local history/ledger.

## Philosophy
This is my personal trading bot that I decided to make open source.
I built this strategy to match my own goals. It is meant to be a framework/foundation that you can extend for your own use.

I know there are "commonly expected" trading features missing, such as stop-loss behavior. That is intentional.
This bot is designed around spot trading, long holding periods when needed, and averaging into worthwhile coins rather than mechanically selling at a loss.

I believe the AI and the overall trading strategy are simple on purpose.
The design is based on real trading experience and on what actually works for this system, not on making the stack look complicated.

I am not selling anything. This bot is not a product. It is for experimentation and education.
Do not fall for scams. PowerTrader AI is free and open source.

IMPORTANT:
This software places real trades automatically. You are responsible for everything it does to your money and your account.
Keep your API keys private. I am not giving financial advice. I am not responsible for losses, security issues on your machine, or misuse of the software.

## What The AI Is Doing
The AI in this system is not an LLM and not a standard neural network.
It is closer to an instance-based / kernel-style pattern-matching predictor with online reliability weighting.

At training time, the system walks historical candles for each supported timeframe and stores memory patterns together with what happened on the following candle.
At run time, it compares the current pattern with the saved memory set and builds weighted predicted candles across multiple timeframes.
Those predicted highs/lows are the blue and orange levels shown in the UI.

After real candles close, the system compares reality with prediction and adjusts the reliability weights of the memory patterns that participated in the forecast.

## How The Trader Uses The Signals
Trade start:
- A fresh trade can start when the long signal reaches at least the configured start level and the short signal is `0`.
- Default trade-start level is `3`.

DCA:
- DCA can trigger from either:
  - the neural level assigned to the current DCA stage, or
  - the hard drawdown threshold for that stage,
  whichever is hit first.
- The system also enforces a rolling max DCA count per 24 hours.

Sell / trailing profit margin:
- If no DCA happened, the base PM line starts at `+5.0%` by default.
- If DCA happened, the base PM line starts at `+2.5%` by default.
- Default trailing gap is `0.5%` behind the peak once trailing activates.

In this fork, these values are configurable from the Hub:
- Trade start level
- Start allocation %
- DCA multiplier
- DCA levels
- Max DCA buys per 24h
- PM start % (no DCA / with DCA)
- Trailing gap %

These settings are hot-reloaded by the trader while the system is running.

## Setup And First-Time Use (Windows)
If you already have open spot positions on the same KuCoin account for coins managed by the bot, PowerTrader will treat those holdings as part of the managed positions.
For the cleanest behavior, many users prefer to start with a clean KuCoin trade account or zero managed balances.

### 1. Install Python
1. Go to `python.org` and install Python.
2. During install, enable `Add Python to PATH`.

### 2. Download The Repo Files
1. Create a folder for the bot, for example `C:\PowerTraderAI`.
2. Copy the repository files into that folder.

### 3. Install Dependencies
From Command Prompt in the project folder:

```bash
python -m pip install setuptools
python -m pip install -r requirements.txt
```

### 4. Start The Hub
From the project folder:

```bash
python pt_hub.py
```

The Hub is the main app you use day to day.

### 5. Configure The Hub
Open `Settings` in the Hub and set:
- Main neural folder
- Coin list
- Trade start level
- Start allocation %
- DCA multiplier / DCA levels / max DCA buys per 24h
- Trailing PM values
- Optional Telegram notification settings

In the KuCoin API section:
1. Open the Setup Wizard.
2. Create a KuCoin API key with at least `General` and `Trade` permissions.
3. Copy API key, secret, and passphrase into the wizard.
4. Save.

This creates:
- `k_key.txt`
- `k_secret.txt`
- `k_pass.txt`

Keep these files private.

### 6. Optional Telegram Notifications
The Hub can configure Telegram notifications for confirmed trades.
Current V1 scope:

- BUY
- DCA BUY
- SELL

Setup flow:
1. Create a Telegram bot with `@BotFather`.
2. Send a message to your bot from your Telegram account.
3. In Hub `Settings`, enable Telegram notifications.
4. Fill in:
   - Telegram bot token
   - Telegram chat ID
5. Use `Send Test Message` before saving if you want to verify the setup immediately.

Message contents in V1:
- action
- symbol
- quantity
- fill price
- realized PnL on SELL
- buying power
- total account value
- brief list of open trades

Safety rules in this fork:
- notifications are sent only after the trade is confirmed and written to local history
- Telegram failures must not interrupt trading
- if Telegram is disabled or not configured, the trader silently skips notifications

### 7. Train
In the Hub:
1. Click `Train All`.
2. Wait for training to finish.

The Hub uses training freshness, not only file existence. If a coin is stale or missing its training timestamp, it stays not-ready until retrained.

### 8. Start The System
In the Hub:
1. Click `Start All`.

The Hub will:
1. start `pt_thinker.py`
2. wait for `runner_ready.json` to report readiness
3. start `pt_trader.py`

Runtime notes for this fork:
- The trader is gated on real runner readiness.
- Temporary API misses fall back to cached good values where possible to avoid fake account crashes in the GUI.
- Pending/stale order recovery is built into trader startup.

## Neural Levels
- Levels run from low to high signal strength.
- They come from predicted highs/lows across timeframes.
- LONG is the buy-direction signal.
- SHORT is the no-start / opposing signal.
- By default, a fresh trade can start when LONG is at least `3` and SHORT is `0`.

## Adding More Coins Later
1. Open `Settings`.
2. Add coin symbols.
3. Save.
4. Retrain.
5. Start the system again.

## Donate
PowerTrader AI is free and open source. If you want to support the project:
- Cash App: `$garagesteve`
- PayPal: `@garagesteve`
- Facebook: `https://www.facebook.com/stephen.bryant.hughes`

## License
PowerTrader AI is released under the Apache 2.0 license.
