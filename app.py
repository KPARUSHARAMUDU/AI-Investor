import streamlit as st
import time
import pandas as pd
import math

from fetch_data import get_stock_data
from agents.signal_agent import detect_signal
from agents.pattern_agent import detect_pattern
from agents.confidence_agent import calculate_confidence
from agents.indicators_agent import (
    calculate_rsi,
    moving_average_signal,
    calculate_macd,
    calculate_roi,
    predict_trend
)
from agents.recommendation_agent import recommend
from scanner import scan_market
from agents.chat_agent import ask_ai
from agents.voice_agent import listen_voice, speak_text

st.set_page_config(page_title="AI Investor", layout="wide")

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center;'>📊 AI Investor Dashboard</h1>", unsafe_allow_html=True)
st.caption("💡 AI-powered stock intelligence system")

st.markdown("---")

# ---------- SIDEBAR ----------
mode = st.sidebar.radio("Select Mode", ["Market Scanner", "Single Stock"])

# ---------- MARKET SCANNER ----------
if mode == "Market Scanner":

    st.subheader("🔥 Market Opportunities")

    if st.button("🚀 Scan Now"):
        
        with st.spinner("🔍 Scanning market using AI..."):
            time.sleep(1.5)
            results = scan_market()

        if results:

            # ✅ Strong (BUY)
            strong_results = [r for r in results if r[1] >= 4 and "BUY" in r[2]]

            # ✅ Moderate (WATCH)
            moderate_results = [r for r in results if r[1] >= 3 and "WATCH" in r[2]]

            # ✅ Sort both
            strong_results = sorted(strong_results, key=lambda x: x[1], reverse=True)
            moderate_results = sorted(moderate_results, key=lambda x: x[1], reverse=True)

            # ✅ Combine (priority: BUY first)
            final_results = strong_results + moderate_results

            # ✅ Top 5 only
            top5 = final_results[:5]

            if not top5:
                st.warning("⚠️ No strong opportunities found today")
            else:

                # 🏆 Top Opportunity
                st.markdown("### 🏆 Top Opportunity")
                top = top5[0]

                if "BUY" in top[2]:
                    st.success(f"{top[0]} | Score: {top[1]} ⭐ | {top[2]}")
                else:
                    st.warning(f"{top[0]} | Score: {top[1]} ⭐ | {top[2]}")

                # 🥇 Top 5 List
                st.markdown("### 🥇 Top Opportunities")

                for i, (stock, score, decision) in enumerate(top5):

                    if "BUY" in decision:
                        st.success(f"{i+1}. {stock} → {score} ⭐ → {decision}")
                    elif "WATCH" in decision:
                        st.warning(f"{i+1}. {stock} → {score} ⭐ → {decision}")
                    else:
                        st.error(f"{i+1}. {stock} → {score} ⭐ → {decision}")

               
# ---------- SINGLE STOCK ----------
else:

    st.subheader("📈 Analyze Stock")

    stock_list = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
        "NOCIL.NS", "AXISBANK.NS", "ADANIPOWER.NS",
        "CEINSYS.NS","ABCAPITAL.NS","ADANIGREEN.NS"
    ]

    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = stock_list[0]

    ticker = st.selectbox(
        "Choose Stock",
        stock_list,
        index=stock_list.index(st.session_state.selected_ticker)
    )

    st.session_state.selected_ticker = ticker

    analyze_clicked = st.button("🔍 Analyze")

    if analyze_clicked:

        data = get_stock_data(ticker)

        signal = detect_signal(data)
        pattern = detect_pattern(data)
        confidence = calculate_confidence(data)
        rsi = calculate_rsi(data)
        trend = moving_average_signal(data)
        macd = calculate_macd(data)
        roi = calculate_roi(data)
        prediction = predict_trend(data)

        score = sum([
            bool(signal),
            bool(pattern),
            trend == "UPTREND",
            macd == "BULLISH",
            confidence > 60
        ])

        decision = recommend(score)

        if "auto_insight" in st.session_state:
            del st.session_state.auto_insight

        st.session_state.context_data = {
            "data": data,
            "ticker": ticker,
            "signal": signal,
            "pattern": pattern,
            "confidence": confidence,
            "rsi": rsi,
            "trend": trend,
            "macd": macd,
            "roi": roi,
            "prediction": prediction,
            "decision": decision
        }

    # ---------- DISPLAY ----------
    if "context_data" in st.session_state:

        ctx = st.session_state.context_data

        st.success("✅ Analysis Ready")

        # ---------- INDICATORS ----------
        st.markdown("### 📊 Indicators")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Trend", ctx["trend"])
        c2.metric("RSI", ctx["rsi"])
        c3.metric("MACD", ctx["macd"])
        c4.metric("Confidence", f"{ctx['confidence']}%")

        # ---------- SIGNAL ----------
        st.markdown("### 🔍 Signal & Pattern")

        s1, s2 = st.columns(2)
        s1.metric("Signal", ctx["signal"]["signal"] if ctx["signal"] else "None")
        s2.metric("Pattern", ctx["pattern"]["pattern"] if ctx["pattern"] else "None")

        # ---------- ROI ----------

        roi_value = ctx["roi"]

        if roi_value is None or (isinstance(roi_value, float) and math.isnan(roi_value)):
          roi_value = 0
 
        st.metric("Return", f"{round(roi_value, 2)}%")

        # ---------- ✅ NEW: FINAL DECISION ----------
        st.markdown("### 🎯 Final Decision")

        if "BUY" in ctx["decision"]:
            st.success(ctx["decision"])
        elif "WATCH" in ctx["decision"]:
            st.warning(ctx["decision"])
        else:
            st.error(ctx["decision"])

        # ---------- ✅ NEW: RISK LEVEL ----------
        st.markdown("### ⚠️ Risk Level")

        if ctx["rsi"] > 70:
            st.error("HIGH RISK 🔴")
        elif ctx["rsi"] < 40:
            st.success("LOW RISK 🟢")
        else:
            st.warning("MEDIUM RISK 🟡")

        # ---------- ✅ NEW: ALERT SYSTEM ----------
        st.markdown("### 🔔 Alerts")

        alerts = []

        if ctx["rsi"] > 70:
            alerts.append("RSI indicates overbought ⚠️")
        if ctx["rsi"] < 30:
            alerts.append("RSI indicates oversold 📈")
        if ctx["confidence"] > 75:
            alerts.append("High confidence signal 🚀")
        if ctx["trend"] == "UPTREND":
            alerts.append("Strong uptrend 📊")

        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("No major alerts")

        # ---------- SIMULATOR ----------
        st.markdown("### 💡 Investment Simulator")

        investment = st.slider("Investment (₹)", 1000, 100000, 10000, step=1000)

        growth = 0

        if ctx["trend"] == "UPTREND":
            growth += 0.05
        elif ctx["trend"] == "DOWNTREND":
            growth -= 0.04

        growth += (ctx["confidence"] / 100) * 0.05

        if ctx["rsi"] > 70:
            growth -= 0.03
        elif ctx["rsi"] < 30:
            growth += 0.03

        growth *= (1 + investment / 200000)
        growth = max(min(growth, 0.2), -0.1)

        future_value = investment * (1 + growth)
        profit = future_value - investment

        st.write(f"Growth Rate: {round(growth*100,2)}%")

        if profit > 0:
            st.success(f"₹{future_value:.2f} (+₹{profit:.2f}) 📈")
        else:
            st.error(f"₹{future_value:.2f} (₹{profit:.2f}) 📉")

        # ---------- AUTO AI INSIGHT ----------
        st.markdown("### 🤖 Auto AI Insight")

        context = str(ctx)

        if "auto_insight" not in st.session_state:
            with st.spinner("Generating insight..."):
                st.session_state.auto_insight = ask_ai(
                    "Explain this stock clearly",
                    context
                )

        st.success(st.session_state.auto_insight)

        # ---------- CHART ----------
        st.line_chart(ctx["data"]["Close"])

        # ---------- COMPARISON ----------
        st.markdown("### 🔄 Compare Stocks")

        compare_stock = st.selectbox("Compare with", ["TCS.NS", "INFY.NS", "HDFCBANK.NS"])

        data2 = get_stock_data(compare_stock)

        combined = pd.concat([
            ctx["data"]["Close"].rename(ctx["ticker"]),
            data2["Close"].rename(compare_stock)
        ], axis=1).ffill()

        st.line_chart(combined)

        # ---------- CHAT ----------
        st.markdown("### 🤖 AI Chat Assistant")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        user_input = st.chat_input("Ask about this stock...")

        if user_input:

            st.chat_message("user").write(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            reply = ask_ai(user_input, str(ctx))

            st.chat_message("assistant").write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------- VOICE ASSISTANT ----------
st.markdown("### 🎤 Voice Assistant")

# 🌍 Language Selector
language = st.selectbox(
    "🌍 Select Language",
    ["English", "Hindi", "Telugu"]
)

# 🎯 Language codes
lang_code_input = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Telugu": "te-IN"
}[language]

lang_code_output = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}[language]

if st.button("🎙️ Speak"):

    with st.spinner("🎤 Listening..."):
     user_voice = listen_voice(lang_code_input)

    if not user_voice or "Sorry" in user_voice:
        st.error("❌ Could not understand voice")
        st.stop()

    st.write(f"🗣️ You said: {user_voice}")

            # 🔥 FORCE LANGUAGE RESPONSE
    prompt = f"""
    User asked in {language}.
    Respond ONLY in {language}.
    Question: {user_voice}
    """
    if "context_data" in st.session_state:
        ctx = st.session_state.context_data

    reply = ask_ai(prompt, str(ctx))

    st.success(reply)

    # 🔊 Multilingual Voice Output (gTTS)
    try:
        
        audio_bytes = speak_text(reply, lang_code_output)
        if audio_bytes:
         st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
         st.warning("⚠️ Voice output failed")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("⚠️ This is not financial advice. For educational purposes only.")
