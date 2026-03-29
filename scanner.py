from fetch_data import get_stock_data
from agents.signal_agent import detect_signal
from agents.pattern_agent import detect_pattern
from agents.confidence_agent import calculate_confidence
from agents.indicators_agent import calculate_rsi, moving_average_signal, calculate_macd
from agents.recommendation_agent import recommend

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
          "NOCIL.NS", "AXISBANK.NS", "ADANIPOWER.NS","CEINSYS.NS","ABCAPITAL.NS","ADANIGREEN.NS"]

def scan_market():

    results = []

    for stock in stocks:
        try:
            data = get_stock_data(stock)

            signal = detect_signal(data)
            pattern = detect_pattern(data)
            confidence = calculate_confidence(data)
            rsi = calculate_rsi(data)
            trend = moving_average_signal(data)
            macd = calculate_macd(data)

            score = 0

            if signal: score += 1
            if pattern: score += 1
            if trend == "UPTREND": score += 1
            if macd == "BULLISH": score += 1
            if confidence > 60: score += 1

            decision = recommend(score)

            results.append((stock, score, decision))

        except Exception as e:
            print(f"Error in {stock}: {e}")

    results.sort(key=lambda x: x[1], reverse=True)

    return results