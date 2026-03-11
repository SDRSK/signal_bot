def volume_signal(current_volume, avg_volume):
    """
    Простий сигнал по обсягу
    """
    if current_volume > avg_volume * 1.5:
        return "LONG"
    elif current_volume < avg_volume * 0.5:
        return "SHORT"
    else:
        return "NEUTRAL"