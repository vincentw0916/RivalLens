import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="RivalLens Pro", layout="wide")

# ---------------- BRAND HEADER ----------------
st.markdown("""
<style>
.header {
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:10px;
}
.logo {
    width:36px;
    height:36px;
    border-radius:10px;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
}
.title {
    font-size:28px;
    font-weight:700;
}
.subtitle {
    color:#888;
    font-size:14px;
}
.card {
    padding:18px;
    border-radius:14px;
    background: #0f172a;
    color:white;
}
.metric {
    font-size:20px;
    font-weight:600;
}
.small {
    color:#94a3b8;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <div class="logo"></div>
    <div>
        <div class="title">RivalLens Pro</div>
        <div class="subtitle">Competitor pricing intelligence</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
url = st.text_input("Enter competitor website")

# ---------------- SCRAPER ----------------
def scrape_prices(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()
        prices = re.findall(r"\$\d+(?:\.\d{1,2})?", text)
        return [float(p.replace("$", "")) for p in prices]
    except:
        return []

# ---------------- ANALYSIS ----------------
def analyze(prices):
    if not prices:
        return None

    prices = sorted(prices)

    return {
        "min": min(prices),
        "max": max(prices),
        "mean": round(np.mean(prices), 2),
        "median": round(np.median(prices), 2),
        "count": len(prices)
    }

# ---------------- UI ----------------
if st.button("Analyze"):
    prices = scrape_prices(url)
    stats = analyze(prices)

    if not prices:
        st.error("No pricing data found")
    else:
        # -------- SUMMARY --------
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f"""
        <div class="card">
            <div class="small">Min Price</div>
            <div class="metric">${stats['min']}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
            <div class="small">Max Price</div>
            <div class="metric">${stats['max']}</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
            <div class="small">Average</div>
            <div class="metric">${stats['mean']}</div>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown(f"""
        <div class="card">
            <div class="small">Products Found</div>
            <div class="metric">{stats['count']}</div>
        </div>
        """, unsafe_allow_html=True)

        # -------- CHART (FIXED SIZE) --------
        st.markdown("### Price Distribution")

        fig, ax = plt.subplots(figsize=(6, 3))  # smaller chart
        ax.hist(prices, bins=5)
        ax.set_xlabel("Price ($)")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # -------- REAL INSIGHTS --------
        st.markdown("### Insights")

        insights = []

        if stats["mean"] < 50:
            insights.append("Competitor is targeting budget-conscious customers.")
        else:
            insights.append("Competitor operates in mid-to-premium pricing.")

        if stats["max"] - stats["min"] > 200:
            insights.append("Wide pricing range suggests multiple customer segments.")
        else:
            insights.append("Tight pricing range indicates focused positioning.")

        if stats["median"] < stats["mean"]:
            insights.append("Higher-end products are pulling average price up.")
        else:
            insights.append("Pricing is evenly distributed across products.")

        for i in insights:
            st.markdown(f"- {i}")

        # -------- STRATEGY --------
        st.markdown("### What You Should Do")

        strategy = []

        if stats["mean"] < 50:
            strategy.append("Differentiate via branding instead of price wars.")
        else:
            strategy.append("Consider undercutting slightly for faster conversions.")

        strategy.append("Introduce bundles to increase perceived value.")
        strategy.append("Highlight best-selling price points clearly.")
        strategy.append("Test premium tier to capture higher-margin customers.")

        for s in strategy:
            st.markdown(f"- {s}")
