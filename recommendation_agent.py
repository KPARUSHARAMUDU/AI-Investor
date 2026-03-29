def recommend(score):

    if score >= 5:
        return "🚀 BUY"

    elif score >= 3:
        return "⚠️ WATCH"

    else:
        return "❌ AVOID"