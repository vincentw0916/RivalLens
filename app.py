import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="RivalLens", page_icon="🔎", layout="centered")

# --------------------------
# HEADER
# --------------------------
st.title("RivalLens 🔎")
st.markdown("### AI-powered competitor pricing intelligence")

st.markdown("---")

# --------------------------
# INPUT
# --------------------------
st.subheader("🔗 Enter Competitor Website")

url = st.text_input(
    "",
    placeholder="https://example.com or just domain (e.g. shop.com)"
)

analyze_btn = st.button("Analyze")

# --------------------------
# SCRAPER
# --------------------------
def get_prices(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url

        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()

        prices = re.findall(r"\$\s?\d+(?:,\d{3})*(?:\.\d{2})?", text)

        return list(set(prices))[:15] if prices else []

    except Exception as e:
        return [f"Error: {str(e)}"]


# --------------------------
# SMART ANALYSIS ENGINE (🔥 NEW)
# --------------------------
def analyze_pricing(prices):
    numeric_prices = []

    for p in prices:
        try:
            value = float(p.replace("$", "").replace(",", ""))
            if value > 0:  # 🔥 remove junk values
                numeric_prices.append(value)
        except:
            continue

    if not numeric_prices:
        return None

    min_price = min(numeric_prices)
    max_price = max(numeric_prices)
    avg_price = sum(numeric_prices) / len(numeric_prices)

    spread = max_price - min_price

    # 🎯 POSITIONING
    if avg_price < 50:
        level = "Low-cost"
    elif avg_price < 300:
        level = "Mid-range"
    else:
        level = "Premium"

    # 🧠 STRATEGY DETECTION
    if spread < 20:
        strategy = "Single-tier / consistent pricing"
    elif spread < 100:
        strategy = "Moderate tiered pricing"
    else:
        strategy = "Wide range (multi-segment strategy)"

    # 💡 SEGMENTATION INSIGHT
    if len(numeric_prices) <= 3:
        model = "Focused offering"
    else:
        model = "Multiple product tiers"

    return {
        "level": level,
        "range": f"${min_price:.0f} - ${max_price:.0f}",
        "strategy": strategy,
        "model": model,
        "avg": avg_price,
        "spread": spread
    }


# --------------------------
# INSIGHT GENERATOR (🔥 CORE UPGRADE)
# --------------------------
def generate_insights(summary):
    insights = []

    # Positioning insight
    insights.append(f"Competitor is positioned as **{summary['level']} market**")

    # Pricing structure insight
    insights.append(f"Pricing structure suggests **{summary['strategy']}**")

    # Product strategy insight
    insights.append(f"Business model indicates **{summary['model']}**")

    # Strategic interpretation
    if summary["spread"] > 100:
        insights.append("Wide pricing range suggests targeting **multiple customer segments**")
    else:
        insights.append("Narrow pricing range suggests a **focused niche strategy**")

    # Competitive implication
    if summary["level"] == "Low-cost":
        insights.append("Competing primarily on **price advantage and accessibility**")
    elif summary["level"] == "Premium":
        insights.append("Competing on **brand, quality, or perceived value**")
    else:
        insights.append("Balancing between **affordability and value perception**")

    return insights


# --------------------------
# ACTION GENERATOR
# --------------------------
def generate_actions(summary):
    actions = []

    if summary["level"] == "Low-cost":
        actions.append("Differentiate with branding instead of competing purely on price")
        actions.append("Offer bundles or upsells to increase order value")

    elif summary["level"] == "Premium":
        actions.append("Undercut slightly OR justify higher pricing with stronger value")
        actions.append("Emphasize quality, trust, and differentiation")

    else:
        actions.append("Position yourself clearly (either more premium OR more affordable)")
        actions.append("Avoid being stuck in the middle")

    if summary["spread"] > 100:
        actions.append("Consider tiered pricing to capture multiple segments")
    else:
        actions.append("Focus on dominating a specific niche")

    actions.append("Improve website clarity and conversion UX")

    return actions


# --------------------------
# MAIN APP
# --------------------------
if analyze_btn and url:

    st.markdown("---")
    st.subheader(f"🔍 Analyzing: {url}")

    prices = get_prices(url)

    if not prices or "Error" in prices[0]:
        st.error("❌ Could not extract pricing data")
    else:

        summary = analyze_pricing(prices)

        if not summary:
            st.warning("⚠️ No meaningful pricing data found")
        else:

            # --------------------------
            # SUMMARY
            # --------------------------
            st.markdown("## 📊 Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric("Positioning", summary["level"])
            col2.metric("Price Range", summary["range"])
            col3.metric("Strategy", summary["strategy"])

            st.markdown("---")

            # --------------------------
            # PRICES
            # --------------------------
            st.markdown("## 💰 Detected Prices")
            st.write(prices)

            st.markdown("---")

            # --------------------------
            # SMART INSIGHTS
            # --------------------------
            st.markdown("## 🧠 Key Insights")

            insights = generate_insights(summary)
            for i in insights:
                st.markdown(f"- {i}")

            st.markdown("---")

            # --------------------------
            # ACTION PLAN
            # --------------------------
            st.markdown("## 🚀 What You Should Do")

            actions = generate_actions(summary)
            for a in actions:
                st.markdown(f"- {a}")

            st.success("✅ Analysis Complete")
