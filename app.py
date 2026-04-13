import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="RivalLens",
    page_icon="🔎",
    layout="wide"
)

# ----------------------------
# PREMIUM STYLING
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
h1, h2, h3, h4 {
    color: white;
}
p, li {
    color: #c9d1d9;
}
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #30363d;
}
.highlight-green {
    border-left: 5px solid #3fb950;
}
.highlight-orange {
    border-left: 5px solid #d29922;
}
.metric {
    font-size: 28px;
    font-weight: bold;
}
.subtle {
    color: #8b949e;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
# 🔎 RivalLens

### Smarter competitor pricing intelligence  
Understand positioning. Beat competitors. Win faster.
""")

# ----------------------------
# INPUT
# ----------------------------
url = st.text_input("Enter competitor website")

# ----------------------------
# SCRAPER
# ----------------------------
def get_prices(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url

        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        prices = re.findall(r"\$\s?\d+(?:\.\d{1,2})?", text)

        return list(set(prices))[:20]

    except Exception:
        return []

# ----------------------------
# SMART ANALYSIS
# ----------------------------
def analyze_prices(prices):
    numeric = []

    for p in prices:
        try:
            numeric.append(float(p.replace("$", "").strip()))
        except:
            pass

    if not numeric:
        return "Unknown", "No range", "No pricing detected"

    avg = sum(numeric) / len(numeric)
    low = min(numeric)
    high = max(numeric)

    if avg < 50:
        level = "Low-cost"
    elif avg < 150:
        level = "Mid-range"
    else:
        level = "Premium"

    spread = high - low

    if spread < 30:
        strategy = "Flat pricing"
    elif spread < 100:
        strategy = "Moderate tiered pricing"
    else:
        strategy = "Wide tiered pricing"

    return level, f"${low:.0f} - ${high:.0f}", strategy

# ----------------------------
# INSIGHTS ENGINE
# ----------------------------
def generate_insights(level, strategy, prices):
    insights = []
    actions = []

    if level == "Low-cost":
        insights.append("Competitor is aggressively priced for volume")
        actions.append("Avoid competing purely on price — margins will suffer")

    if level == "Mid-range":
        insights.append("Balanced pricing suggests broad audience targeting")
        actions.append("Differentiate clearly — don't stay in the middle")

    if level == "Premium":
        insights.append("Premium positioning focused on value perception")
        actions.append("Compete via branding, trust, and added value")

    if "tiered" in strategy:
        insights.append("Multiple pricing tiers indicate segmentation strategy")
        actions.append("Introduce clear packages or bundles")

    if len(prices) > 10:
        insights.append("Wide product range detected")
        actions.append("Focus on best-selling niche instead of everything")

    if not insights:
        insights.append("Limited data — competitor may hide pricing")
        actions.append("Use transparency as your advantage")

    return insights, actions

# ----------------------------
# BUTTON ACTION
# ----------------------------
if st.button("Analyze"):

    with st.spinner("Analyzing competitor..."):
        prices = get_prices(url)
        level, price_range, strategy = analyze_prices(prices)
        insights, actions = generate_insights(level, strategy, prices)

    st.markdown(f"## 🔍 Analyzing: {url}")

    # ----------------------------
    # SUMMARY CARDS
    # ----------------------------
    st.markdown("## 📊 Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card highlight-green">
            <div class="subtle">Positioning</div>
            <div class="metric">{level}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="subtle">Price Range</div>
            <div class="metric">{price_range}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card highlight-orange">
            <div class="subtle">Strategy</div>
            <div class="metric">{strategy}</div>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------
    # PRICES
    # ----------------------------
    st.markdown("## 💰 Detected Prices")

    if prices:
        for p in prices:
            st.markdown(f"""
            <div class="card">
                {p}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No prices found")

    # ----------------------------
    # INSIGHTS
    # ----------------------------
    st.markdown("## 🧠 Key Insights")

    for i in insights:
        st.markdown(f"""
        <div class="card highlight-green">
            {i}
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------
    # ACTIONS
    # ----------------------------
    st.markdown("## 🚀 What You Should Do")

    for a in actions:
        st.markdown(f"""
        <div class="card highlight-orange">
            {a}
        </div>
        """, unsafe_allow_html=True)

    st.success("Analysis Complete ✅")
