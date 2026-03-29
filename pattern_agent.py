from utils import get_column

def detect_pattern(data):

    high = get_column(data, 'High')
    close = get_column(data, 'Close')

    recent_high = high.rolling(10).max().iloc[-2]
    latest_close = close.iloc[-1]

    if latest_close > recent_high:
        return {"pattern": "Breakout"}

    return None