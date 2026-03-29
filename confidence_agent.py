from utils import get_column
def calculate_confidence(data):

    # Fix multi-column issue
    close_prices = data['Close']

    if isinstance(close_prices, type(data)):  # if DataFrame
        close_prices = close_prices.iloc[:, 0]

    # Calculate returns
    returns = close_prices.pct_change().dropna()

    positive_days = (returns > 0).sum()
    total_days = len(returns)

    confidence = (positive_days / total_days) * 100

    return round(float(confidence), 2)
