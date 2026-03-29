from utils import get_column

def detect_signal(data):

    volume = get_column(data, 'Volume')

    latest_volume = volume.iloc[-1]
    avg_volume = volume.mean()

    ratio = latest_volume / avg_volume

    if ratio > 2:
        return {
            "signal": "High Volume Spike",
            "details": f"{round(ratio,2)}x higher",
            "strength": "strong"
        }

    elif ratio < 0.5:
        return {
            "signal": "Low Volume",
            "details": f"{round(ratio,2)}x of avg",
            "strength": "weak"
        }

    else:
        return {
            "signal": "Normal Volume",
            "details": f"{round(ratio,2)}x of avg",
            "strength": "neutral"
        }