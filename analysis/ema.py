def ema_signal(prices, short_period=9, long_period=21):
    """
    Простий EMA кросовер
    prices: list[float] - історія цін від старої до нової
    """
    if len(prices) < long_period:
        return "NEUTRAL"

    short_ema = sum(prices[-short_period:]) / short_period
    long_ema = sum(prices[-long_period:]) / long_period

    if short_ema > long_ema:
        return "LONG"
    elif short_ema < long_ema:
        return "SHORT"
    else:
        return "NEUTRAL"