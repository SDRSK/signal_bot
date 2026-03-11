def rsi_signal(prices, period=14):
    """
    RSI сигнал
    """
    if len(prices) < period + 1:
        return "NEUTRAL"

    gains = [max(0, prices[i] - prices[i-1]) for i in range(1, len(prices))]
    losses = [max(0, prices[i-1] - prices[i]) for i in range(1, len(prices))]

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return "LONG"

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    if rsi < 30:
        return "LONG"
    elif rsi > 70:
        return "SHORT"
    else:
        return "NEUTRAL"