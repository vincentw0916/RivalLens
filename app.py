import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

st.set_page_config(page_title="RivalLens Pro", layout="wide")

# --------------------------
# CLEAN DARK UI (FIXED)
# --------------------------
st.markdown("""
<style>
body { background-color: #0e1117; color: #e6edf3; }

.card {
    background: #161b22;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #30363d;
    margin-bottom: 15px;
}

.metric {
    font-size: 26px;
    font-weight: bold;
    color: #ffffff;
}

.label {
    color: #8b949e;
    font-size: 14px;
}

.section-title {
    font-size: 22px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# URL FIX
# --------------------------
def fix_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url

# --------------------------
# SCRAPER
# --------------------------
def get_prices(url):
    try:
        url = fix_url(url)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()

        prices = re.findall(r"\$\s?\d+(?:\.\d{1,2})?", text)
        nums = [float(p.replace("$", "").strip()) for p in prices]

        return nums[:30]

    except:
        return []

# --------------------------
# ADVANCED ANALYSIS
# --------------------------
def analyze(nums):

    if not nums:
        return None

    avg = np.mean(nums)
    median = np.median(nums)
    low = min(nums)
    high = max(nums)
    spread = high - low

    # Tier detection
    tiers = len(set(nums))

    if tiers <= 3:
        tier_type = "Simple pricing"
    elif tiers <= 8:
        tier_type = "Tiered pricing"
    else:
        tier_type = "Complex catalog pricing"

    # Positioning
    if avg < 50:
        position = "Low-cost"
    elif avg < 150:
        position = "Mid-market"
    else:
        position = "Premium"

    return {
        "avg": avg,
        "median": median,
        "low": low,
        "high": high,
        "spread": spread,
        "tiers": tiers,
        "tier_type": tier_type,
        "position": position
    }

# --------------------------
# UI
# --------------------------
st.title("🔎 RivalLens Pro")
st.caption("Competitor pricing intelligence (real analysis)")

url = st.text_input("Enter competitor website")

if st.button("Analyze"):

    prices = get_prices(url)
    data = analyze(prices)

    st.markdown(f"### 🔍 {fix_url(url)}")

    # --------------------------
    # SUMMARY
    # --------------------------
    if data:
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f"""
        <div class="card">
        <div class="label">Position</div>
        <div class="metric">{data['position']}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
        <div class="label">Price Range</div>
        <div class="metric">${int(data['low'])} - ${int(data['high'])}</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
        <div class="label">Median Price</div>
        <div class="metric">${int(data['median'])}</div>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown(f"""
        <div class="card">
        <div class="label">Pricing Model</div>
        <div class="metric">{data['tier_type']}</div>
        </div>
        """, unsafe_allow_html=True)

        # --------------------------
        # BETTER GRAPH
        # --------------------------
        st.markdown("### 📊 Price Distribution")

        st.write("This shows how prices are spread across their offering.")

        hist = np.histogram(prices, bins=5)

        chart_data = {
            "Range": [f"${int(hist[1][i])}-{int(hist[1][i+1])}" for i in range(len(hist[0]))],
            "Count": hist[0]
        }

        st.bar_chart(chart_data, x="Range", y="Count")

        # --------------------------
        # INSIGHTS (REAL)
        # --------------------------
        st.markdown("### 🧠 Insights")

        insights = []

        if data["spread"] > 100:
            insights.append("Wide pricing spread → targeting multiple customer segments")

        if data["median"] < data["avg"]:
            insights.append("Higher-end skew → premium products influence pricing")

        if data["tiers"] > 10:
            insights.append("Large catalog → volume-based strategy")

        if data["spread"] < 40:
            insights.append("Tight pricing → weak differentiation opportunity")

        if data["position"] == "Low-cost":
            insights.append("Competing on price → likely thin margins")

        for i in insights:
            st.markdown(f"<div class='card'>{i}</div>", unsafe_allow_html=True)

        # --------------------------
        # ACTIONABLE STRATEGY
        # --------------------------
        st.markdown("### 🚀 What You Should Do")

        actions = []

        if data["position"] == "Low-cost":
            actions.append("Avoid price war → compete with branding or bundles")

        if data["spread"] < 40:
            actions.append("Introduce clear pricing tiers to outperform")

        if data["tiers"] > 10:
            actions.append("Niche down instead of competing broadly")

        if data["median"] > 80:
            actions.append("Undercut slightly to capture conversions")

        for a in actions:
            st.markdown(f"<div class='card'>{a}</div>", unsafe_allow_html=True)

    else:
        st.error("No pricing data detected (JS-based or hidden pricing)")
