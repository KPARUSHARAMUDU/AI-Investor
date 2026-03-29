from utils import get_column

def calculate_rsi(data, period=14):

    close = get_column(data, 'Close')

    delta = close.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return round(rsi.iloc[-1], 2)


def moving_average_signal(data):

    close = get_column(data, 'Close')

    ma = close.rolling(20).mean()

    return "UPTREND" if close.iloc[-1] > ma.iloc[-1] else "DOWNTREND"


def calculate_macd(data):

    close = get_column(data, 'Close')

    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()

    return "BULLISH" if macd.iloc[-1] > signal.iloc[-1] else "BEARISH"

def calculate_roi(data):
    try:
        if data is None or len(data) < 2:
            return 0

        data = data.dropna()

        first_price = data['Close'].iloc[0]
        last_price = data['Close'].iloc[-1]

        if first_price == 0:
            return 0

        roi = ((last_price - first_price) / first_price) * 100

        return round(roi, 2)

    except Exception:
        return 0

def predict_trend(data):

    short_ma = data['Close'].rolling(5).mean().iloc[-1]
    long_ma = data['Close'].rolling(20).mean().iloc[-1]

    if short_ma > long_ma:
        return "📈 Likely Uptrend"
    elif short_ma < long_ma:
        return "📉 Likely Downtrend"
    else:
        return "➡️ Sideways"