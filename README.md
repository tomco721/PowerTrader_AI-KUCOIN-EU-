# PowerTrader_AI - KUCOIN (EU)
Fully automated crypto trading powered by a custom price prediction AI and a structured/tiered DCA system.

## About this KuCoin fork

This repository is a **fork** of the original PowerTrader_AI, which was written for **Robinhood Crypto**.  
This fork keeps the **AI, DCA logic and trailing-profit strategy** the same, but completely rewires the
trading layer to work with **KuCoin spot (USDT) – suitable for EU users and non‑US residents.**

High‑level changes in this fork:

- **Exchange migration**: All live trading calls in `pt_trader.py` now use KuCoin REST API  
  (`/api/v1/accounts`, `/api/v1/orders`, `/api/v1/symbols`, etc.) with HMAC‑SHA256 signing and KuCoin
  API key + secret + passphrase (no more Robinhood keys, no NaCl/Ed25519 signing).
- **Holdings & buying power**: Account balance and open positions are derived from KuCoin **trade accounts**
  (USDT quote), and normalized back into the original “holdings/buying_power” structure used by the GUI.
- **Order mapping layer**: KuCoin order responses (e.g. `dealFunds`, `dealSize`, `status`) are converted into
  a Robinhood‑like format so the rest of the trader logic can stay almost unchanged.
- **Cost basis fix**: Cost basis is now computed from **all filled BUY orders (including all DCA levels)**:
  - full pagination over all `status=done` orders per symbol, and  
  - a fallback to `trade_history.jsonl` to recover prices if the API omits fill details.  
  This ensures sells only happen when there is **real profit versus the entire position**, not just the last DCA.
- **Safety and robustness**: The trader caches last good bid/ask and account snapshots so transient KuCoin
  API glitches do not create fake dips in the GUI or zero out account value.
- **Settings integration**: The existing GUI **Settings** panel is reused; the “KuCoin API configured” section
  loads keys from disk and hot‑reloads DCA / PM parameters exactly like in the original bot.

Important: Many sections below in this README still mention **Robinhood** and the original key setup flow.  
For this fork, treat those Robinhood‑specific parts as historical – live trading is performed **only against
KuCoin** once you provide KuCoin API credentials in the Hub settings.

DO NOT TRUST THE POWERTRADER FORK FROM Drizztdowhateva!!!

This is my personal trading bot that I decided to make open source. I made this strategy to match my personal goals. This system is meant to be a foundation/framework for you to build your dream bot!

I know there are "commonly essential" trading features that are missing (like no stop loss for example). This is by design because many of those things would just not work with this system's strategy as it stands, for my personal reasons below:

I do not believe in selling worthwhile coins at a loss (and why would you trade anything besides worthwhile coins with a trading bot, anyways???).

I DO believe in crypto. I'd rather just wait and maybe add more money to my account if need be so that the bot can buy even more of the coin while the price is down.

I personally feel like many of those common things people use, like stop loss, are actually a trick or something, and I personally have absolutely no problem adding more money to my account to afford more DCA or having to wait for extended periods of time, if need be. In my opinion, anything else is just greedy and desperate, which is the exact OPPOSITE of needed attributes for long term growth. Plus, this is just spot trading... there's no worry of liquidation and it feels to me like many "risk management" tactics are really only meant for futures trading but people blindly apply them to spot trading when it just plain isn't necessary.

I know the AI and the trading strategy are extremely simple because I'm the one that designed and made them. I've been developing this specific trading strategy for almost a decade and the design of the AI system for the last few years. The overall strategy is based on what ACTUALLY works from real trading experience, not just stuff I read in LLM responses or search engine results.


Ok now that all of that is out of the way...

I am not selling anything. This trading bot is not a product. This system is for experimentation and education. The only reason you would EVER send me money is if you are voluntarily donating (donation routes can be found at the bottom of this readme :) ). Do not fall for any scams! PowerTrader AI is COMPLETELY FREE FOREVER!

IMPORTANT: This software places real trades automatically. You are responsible for everything it does to your money and your account. Keep your API keys private. I am not giving financial advice. I am not responsible for any losses incurred or any security breaches to your computer (the code is entirely open source and can be confirmed non-malicious). You are fully responsible for doing your own due diligence to learn and understand this trading system and to use it properly. You are fully responsible for all of your money and all of the bot's actions, and any gains or losses.

“It’s an instance-based (kNN/kernel-style) predictor with online per-instance reliability weighting, used as a multi-timeframe trading signal.” - ChatGPT on the type of AI used in this trading bot.

So what exactly does that mean?

When people think AI, they usually think about LLM style AIs and neural networks. What many people don't realize is there are many types of Artificial Intelligence and Machine Learning - and the one in my trading system falls under the "Other" category.

When training for a coin, it goes through the entire history for that coin on multiple timeframes and saves each pattern it sees, along with what happens on the next candle AFTER the pattern. It uses these saved patterns to generate a predicted candle by taking a weighted average of the closest matches in memory to the current pattern in time. This weighted average output is done once for each timeframe, from 1 hour up to 1 week. Each timeframe gets its own predicted candle. The low and high prices from these candles are what are shown as the blue and orange horizontal lines on the price charts. 

After a candle closes, it checks what happened against what it predicted, and adjusts the weight for each "memory pattern" that was used to generate the weighted average, depending on how accurate each pattern was compared to what actually happened.

Yes, it is EXTREMELY simple. Yes, it is STILL considered AI.

Here is how the trading bot utilizes the price prediction ai to automatically make trades:

For determining when to start trades, the AI's Thinker script sends a signal to start a trade for a coin if the ask price for the coin drops below at least 3 of the the AI's predicted low prices for the coin (it predicts the currently active candle's high and low prices for each timeframe across all timeframes from 1hr to 1wk).

For determining when to DCA, it uses either the current price level from the AI that is tied to the current amount of DCA buys that have been done on the trade (for example, right after a trade starts when 3 blue lines get crossed, its first DCA wont happen until the price crosses the 4th line, so on so forth), or it uses the hardcoded drawdown % for its current level, whichever it hits first. It only allows a max of 2 DCAs within a rolling 24hr window to keep from dumping all of your money in too quickly on coins that are having an extended downtrend. Other risk management features can easily be added, as well, with just a bit of Python code!

For determining when to sell, the bot uses a trailing profit margin to maximize the potential gains. The margin line is set at either 5% gain if no DCA has happened on the trade, or 2.5% gain if any DCA has happened. The trailing margin gap is 0.5% (this is the amount the price has to go over the profit margin to begin raising the profit margin up to TRAIL after the price and maximize how much profit is gained once the price drops below the profit margin again and the bot sells the trade.


# Setup & First-Time Use (Windows)

THESE INSTRUCTIONS WERE WRITTEN BY AI! PLEASE LET ME KNOW IF THERE ARE ANY ERRORS OR ISSUES WITH THIS SETUP PROCESS!

If you already have open spot positions on the **same KuCoin account** (for coins you plan to let the bot trade), be aware that PowerTrader will treat those holdings as part of its managed positions.  
For the cleanest behavior, many users prefer to start with a **fresh KuCoin trade account / zero balances** on the coins managed by the bot, or at least understand that the bot will DCA and sell based on the *entire* quantity it sees for those coins on KuCoin.

This page walks you through installing PowerTrader AI from start to finish, in the exact order a first-time user should do it.  
No coding knowledge needed.  
These instructions are Windows-based but PowerTrader AI *should* be able to run on any OS.

IMPORTANT: This software places real trades automatically. You are responsible for everything it does to your money and your account. Keep your API keys private. I am not giving financial advice. I am not responsible for any losses incurred or any security breaches to your computer (the code is entirely open source and can be confirmed non-malicious). You are fully responsible for doing your own due diligence to learn and understand this trading system and to use it properly. You are fully responsible for all of your money and all of the bot's actions, and any gains or losses.

---

## Step 1 — Install Python

1. Go to **python.org** and download Python for Windows.
2. Run the installer.
3. **Check the box** that says: **“Add Python to PATH”**.
4. Click **Install Now**.

---

## Step 2 — Download PowerTrader AI

1. Do not download the zip file of the repo! There is an issue I have to fix.
2. Create a folder on your computer, like: `C:\PowerTraderAI\`
3. On the PowerTrader_AI repo page, go to the code page for pt_hub.py, click the "Download Raw File" button, save it into the folder you just created.
4. Repeat that for all files in the repo (except the readme and the license).

---

## Step 3 — Install PowerTrader AI (one command)

1. Open **Command Prompt** (Windows key → type **cmd** → Enter).
2. Go into your PowerTrader AI folder. Example:

   `cd C:\PowerTraderAI`

3. If using Python 3.12 or higher, run this command:

   `python -m pip install setuptools`

4. Install everything PowerTrader AI needs:

   `python -m pip install -r requirements.txt`

---

## Step 4 — Start PowerTrader AI

From the same Command Prompt window (inside your PowerTrader folder), run:

`python pt_hub.py`

The app that opens is the **PowerTrader Hub**.  
This is the only thing you need to run day-to-day.

---

## Step 5 — Set your folder, coins, and KuCoin API keys (inside the Hub)

### Open Settings

In the Hub, open **Settings** and follow these steps:

- **Main Neural Folder** – set this to the same folder that contains `pt_hub.py` (easiest option).  
- **Coins (comma)** – enter a comma‑separated list of coins, e.g. `BTC,ETH,SOL,BNB,XRP`. The bot will train the AI and trade `COIN-USDT` pairs on KuCoin for these symbols.

Then, near the bottom of the window, you will see the **KuCoin API** section:

1. Click **Setup Wizard**.
2. On the KuCoin website go to **API Management** and create a new API key:
   - enable at least the **General** and **Trade** permissions (spot trading),  
   - choose your own **Passphrase** (remember it).
3. From KuCoin, copy:
   - **API Key**,  
   - **API Secret**,  
   - **Passphrase**.
4. Paste these three values into the wizard fields in the Hub (**API Key / API Secret / Passphrase**).
5. Optionally click **Test Connection** (checks that the app can reach KuCoin’s public API).
6. Click **Save**.

After saving, three files will be created in your project folder:

- `k_key.txt` – KuCoin API Key  
- `k_secret.txt` – KuCoin API Secret  
- `k_pass.txt` – KuCoin API Passphrase  

These files contain sensitive credentials – **keep them private** and never share them with anyone.

PowerTrader AI uses a simple folder layout:  
**BTC uses the main folder**, and other coins use their own subfolders (e.g. `ETH\`), just like in the original version.

---

## Step 6 — Train (inside the Hub)

Training builds the system’s coin “memory” so it can generate signals.

1. In the Hub, click **Train All**.
2. Wait until training finishes.

---

## Step 7 — Start the system (inside the Hub)

When all coins have completed training, click:

1. **Start All**

The Hub will:  
**start pt_thinker.py**, wait until it is ready, then it will **start pt_trader.py**.  
You don’t need to manually start separate programs. The hub handles everything!

---

## Neural Levels (the LONG/SHORT numbers)

- These are signal strength levels from low to high.
- They are the predicted high and low prices for all timeframes from 1hr to 1wk.
- They are used to show how stretched a coin's price is and for determining when to start trades and potentially when to DCA for the first few levels of DCA (Whichever price is higher, the Neural level or the hardcoded drawdown % for the current DCA level.
- Higher number = stronger signal.
- LONG = buy-direction signal. SHORT = No-start signal

A TRADE WILL START FOR A COIN IF THAT COIN REACHES A LONG LEVEL OF 3 OR HIGHER WHILE HAVING A SHORT LEVEL OF 0! This is adjustable in the settings.

---

## Adding more coins (later)

1. Open **Settings**
2. Add one new coin
3. Save
4. Click **Train All**, wait for training to complete
5. Click **Start All**

---

## Donate

PowerTrader AI is COMPLETELY free and open source! If you want to support the project, you can donate or become a member:

- Cash App: **$garagesteve**
- PayPal: **@garagesteve**
- Facebook (Subscribe to my Facebook page for only $1/month): **https://www.facebook.com/stephen.bryant.hughes**

---

## License

PowerTrader AI is released under the **Apache 2.0** license.

---

IMPORTANT: This software places real trades automatically. You are responsible for everything it does to your money and your account. Keep your API keys private. I am not giving financial advice. I am not responsible for any losses incurred or any security breaches to your computer (the code is entirely open source and can be confirmed non-malicious). You are fully responsible for doing your own due diligence to learn and understand this trading system and to use it properly. You are fully responsible for all of your money and all of the bot's actions, and any gains or losses.
