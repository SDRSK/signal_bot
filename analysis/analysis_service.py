from analysis.ema import ema_signal
from analysis.rsi import rsi_signal
from analysis.volume import volume_signal

def analyze(symbol_data):
    """
    symbol_data: dict {
        'prices': list[float],
        'volumes': list[float]
    }
    Повертає готовий сигнал LONG / SHORT / NEUTRAL
    """
    prices = symbol_data['prices']
    volumes = symbol_data['volumes']
    avg_volume = sum(volumes[:-1]) / (len(volumes)-1)
    current_volume = volumes[-1]

    signals = []

    # EMA
    signals.append(ema_signal(prices))
    # RSI
    signals.append(rsi_signal(prices))
    # Volume
    signals.append(volume_signal(current_volume, avg_volume))

    # Якщо всі три сигналу в одну сторону → беремо його
    if signals.count("LONG") >= 2:
        final_signal = "LONG"
    elif signals.count("SHORT") >= 2:
        final_signal = "SHORT"
    else:
        final_signal = "NEUTRAL"

    return {
        "final_signal": final_signal,
        "details": {
            "EMA": signals[0],
            "RSI": signals[1],
            "Volume": signals[2]
        }
    }