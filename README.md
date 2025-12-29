# PowerTrader_AI
Fully automated crypto trading powered by a custom price prediction AI and a structured/tiered DCA system.

“It’s an instance-based (kNN/kernel-style) predictor with online per-instance reliability weighting, used as a multi-timeframe trading signal.” - ChatGPT on the type of AI used in this trading bot.

So what exactly does that mean?

When people think AI, they usually think about LLM style AIs and neural networks. What many people don't realize is there are many types of Artificial Intelligence and Machine Learning - and the one in my trading system falls under the "Other" category.

When training for a coin, it goes through the entire history for that coin on multiple timeframes and saves each pattern it sees, along with what happens on the next candle AFTER the pattern. It uses these saved patterns to generate a predicted candle by taking a weighted average of the closest matches in memory to the current pattern in time. This weighted average output is done once for each timeframe, from 1 hour up to 1 week. Each timeframe gets its own predicted candle. The low and high prices from these candles are what are shown as the blue and orange horizontal lines on the price charts. 

After a candle closes, it checks what happened against what it predicted, and adjusts the weight for each "memory pattern" that was used to generate the weighted average, depending on how accurate each pattern was compared to what actually happened.

Yes, it is EXTREMELY simple. Yes, it is STILL considered AI.

Here is how the trading bot utilizes the price prediction ai to automatically make trades:

For determining when to start trades, the AI's Thinker script sends a signal to start a trade for a coin if the ask price for the coin drops below at least 3 of the the AI's predicted low prices for the coin (it predicts the currently active candle's high and low prices for each timeframe across all timeframes from 1hr to 1wk).

For determining when to DCA, it uses either the current price level from the AI that is tied to the current amount of DCA buys that have been done on the trade (for example, right after a trade starts when 3 blue lines get crossed, its first DCA wont happen until the price crosses the 4th line, so on so forth), or it uses the hardcoded drawdown % for its current level, whichever it hits first. It allows a max of 2 DCAs within a rolling 24hr window to keep from dumping all of your money in too quickly on coins that are having an extended downtrend!

For determining when to sell, the bot uses a trailing profit margin to maximize the potential gains. The margin line is set at either 5% gain if no DCA has happened on the trade, or 2.5% gain if any DCA has happened. The trailing margin gap is 0.5% (this is the amount the price has to go over the profit margin to begin raising the profit margin up to TRAIL after the price and maximize how much profit is gained once the price drops below the profit margin again and the bot sells the trade.


# Setup & First-Time Use (Windows)

I would probably stick to < Python 3.12 btw...

THESE INSTRUCTIONS WERE WRITTEN BY AI! PLEASE LET ME KNOW IF THERE ARE ANY ERRORS OR ISSUES WITH THIS SETUP PROCESS!

If you have any crypto holdings in Robinhood currently, either transfer them out of your Robinhood account or sell them to dollars BEFORE going through this setup process!

This page walks you through installing PowerTrader AI from start to finish, in the exact order a first-time user should do it.  
No coding knowledge needed.  
These instructions are Windows-based but PowerTrader AI can run on any OS.

**Important:** This software can place trades automatically. You are responsible for what it does.  
Keep your API keys private. We are not giving financial advice. We are not responsible for any losses incurred. You are fully responsible for doing your own due diligence to learn and understand this trading system and to use it properly. You are fully responsible for all of your money, and any gains or losses.

---

## Step 1 — Install Python

1. Go to **python.org** and download Python for Windows.
2. Run the installer.
3. **Check the box** that says: **“Add Python to PATH”**.
4. Click **Install Now**.

---

## Step 2 — Download PowerTrader AI

1. On the PowerTrader AI GitHub page, click **Code** → **Download ZIP**.
2. Extract the ZIP somewhere simple, like: `C:\PowerTraderAI\`

---

## Step 3 — Install PowerTrader AI (one command)

1. Open **Command Prompt** (Windows key → type **cmd** → Enter).
2. Go into your PowerTrader AI folder. Example:

   `cd C:\PowerTraderAI`

3. Install everything PowerTrader AI needs:

   `python -m pip install -r requirements.txt`

---

## Step 4 — Start PowerTrader AI

From the same Command Prompt window (inside your PowerTrader folder), run:

`python pt_hub.py`

The app that opens is the **PowerTrader Hub**.  
This is the only thing you need to run day-to-day.

---

## Step 5 — Set your folder, coins, and Robinhood keys (inside the Hub)

### Open Settings

In the Hub, open **Settings** and do this in order:

- **Main Neural Folder**: set this to the same folder that contains `pt_hub.py` (recommended easiest).
- **Choose which coins to trade**: start with **BTC**.
- **While you are still in Settings**, click **Robinhood API Setup** and do this:

1. Click **Generate Keys**.
2. Copy the **Public Key** shown in the wizard.
3. On Robinhood, add a new API key and paste that Public Key.
4. Set permissions to allow trading (the wizard tells you what to select).
5. Robinhood will show your API Key (often starts with `rh`). Copy it.
6. Paste the API Key back into the wizard and click **Save**.
7. Close the wizard and go back to the **Settings** screen.
8. **NOW** click **Save** in Settings.

After saving, you will have two files in your PowerTrader AI folder:  
`r_key.txt` and `r_secret.txt`  
Keep them private.

PowerTrader AI uses a simple folder style:  
**BTC uses the main folder**, and other coins use their own subfolders (like `ETH\`).

---

## Step 6 — Train (inside the Hub)

Training builds the system’s coin “memory” so it can generate signals.

1. In the Hub, click **Train All**.
2. Wait until training finishes.

---

## Step 7 — Start the system (inside the Hub)

When training is done, click:

1. **Start All**

The Hub will:  
**start pt_thinker.py**, wait until it is ready, then it will **start pt_trader.py**.  
You don’t need to manually start separate programs. The hub handles everything!

---

## Neural Levels (the LONG/SHORT numbers)

- These are signal strength levels from low to high.
- Higher number = stronger signal.
- LONG = buy-direction signal. SHORT = sell-direction signal.

A TRADE WILL START FOR A COIN IF THAT COIN REACHES A LONG LEVEL OF 3 OR HIGHER WHILE HAVING A SHORT LEVEL OF 0!

---

## Adding more coins (later)

1. Open **Settings**
2. Add one new coin
3. Save
4. Click **Train All**, wait for training to complete
5. Click **Start All**

---

## Donate

PowerTrader AI is COMPLETELY free and open source! If you want to support the project:

- Cash App: **$garagesteve**
- PayPal: **@garagesteve**
- Patreon: **patreon.com/MakingMadeEasy**

---

## License

PowerTrader AI is released under the **Apache 2.0** license.
