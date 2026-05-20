from pybit.unified_trading import HTTP
import pandas as pd
import ta

session = HTTP(testnet=False)

TF_MAP = {
    "1m": "1",
    "5m": "5",
    "10m": "10",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "2h": "120",
    "4h": "240",
    "1d": "D",
    "1w": "W",
    "1M": "M"
}


def get_data(symbol, timeframe):
    interval = TF_MAP[timeframe]

    res = session.get_kline(
        category="linear",
        symbol=symbol,
        interval=interval,
        limit=200
    )

    df = pd.DataFrame(res["result"]["list"])
    df = df.iloc[::-1]

    df.columns = ["time", "open", "high", "low", "close", "volume", "turnover"]

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["volume"] = df["volume"].astype(float)

    return df


# ===== СТРАТЕГІЇ =====

def ema_signal(df):
    ema50 = ta.trend.ema_indicator(df["close"], window=50)
    ema200 = ta.trend.ema_indicator(df["close"], window=200)

    if ema50.iloc[-1] > ema200.iloc[-1]:
        return "LONG"
    elif ema50.iloc[-1] < ema200.iloc[-1]:
        return "SHORT"


def rsi_signal(df):
    rsi = ta.momentum.rsi(df["close"], window=14)

    if rsi.iloc[-1] < 30:
        return "LONG"
    elif rsi.iloc[-1] > 70:
        return "SHORT"


def volume_signal(df):
    avg_volume = df["volume"].rolling(20).mean()

    if df["volume"].iloc[-1] > avg_volume.iloc[-1]:
        return "LONG"


STRATEGY_MAP = {
    "EMA Trend": ema_signal,
    "RSI": rsi_signal,
    "Volume": volume_signal,
}


def run_analysis(symbol, timeframe, strategies):
    df = get_data(symbol, timeframe)

    price = df["close"].iloc[-1]
    high = df["high"].max()
    low = df["low"].min()

    results = []
    long_count = 0
    short_count = 0

    for strat in strategies:
        func = STRATEGY_MAP.get(strat)

        if func:
            signal = func(df)

            if signal:
                if signal == "LONG":
                    long_count += 1
                    emoji = "🟢"
                else:
                    short_count += 1
                    emoji = "🔴"

                results.append(f"{emoji} {strat}: {signal}")

    final = "❌"
    if long_count > short_count:
        final = "🟢 LONG"
    elif short_count > long_count:
        final = "🔴 SHORT"

    message = f"""
📊 {symbol}
⏱ TF: {timeframe}

💰 Ціна: {price:.2f}
📈 High: {high:.2f}
📉 Low: {low:.2f}

📊 Стратегії:
{chr(10).join(results) if results else "нема сигналів"}

🔥 Результат: {final}
"""

    return message