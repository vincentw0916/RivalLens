import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="RivalLens", layout="wide")

# ----------------------------
# CLEAN LIGHT + PREMIUM STYLE
# ----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* MAIN BACKGROUND */
.main {
    background-color: #f8fafc;
}

/* HEADINGS */
h1 {
    font-size: 42px;
    font-weight: 700;
    color: #0f172a;
}

h2 {
    color: #0f172a;
    margin-top: 30px;
}

/* CARD */
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 16px;
}

/* METRICS */
.metric {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
}

.label {
    color: #64748b;
    font-size: 14px;
}

/* TAG COLORS */
.green { border-left: 5px solid #22c55e; }
.orange { border-left: 5px solid #f59e0b; }
.blue { border-left: 5px solid #3b82f6; }

/* PRICE TAG */
.price {
    font-size: 18px;
    font-weight: 600;
    color: #111827;
}

/* SECTION SPACING */
.block {
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
# 🔎 RivalLens  
Smarter competitor pricing intelligence  
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

    except:
        return []

# ----------------------------
# ANALYSIS
# ----------------------------
def analyze_prices(prices):
    nums = []

    for p in prices:
        try:
            nums.append(float(p.replace("$", "")))
        except:
            pass

    if not nums:
        return "Unknown", "No range", "No data"

    avg = sum(nums) / len(nums)
    low = min(nums)
    high = max(nums)

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
        strategy = "Tiered pricing"
    else:
        strategy = "Wide pricing model"

    return level, f"${low:.0f} – ${high:.0f}", strategy

# ----------------------------
# INSIGHTS
# ----------------------------
def generate_insights(level, strategy):
    insights = []
    actions = []

    if level == "Low-cost":
        insights.append("Aggressive pricing targeting volume")
        actions.append("Avoid price wars — focus on value")

    if level == "Mid-range":
        insights.append("Balanced positioning for mass market")
        actions.append("Differentiate clearly to stand out")

    if level == "Premium":
        insights.append("High-value perception strategy")
        actions.append("Compete via branding and trust")

    if "Tiered" in strategy:
        insights.append("Multiple pricing tiers indicate segmentation")
        actions.append("Offer structured packages")

    return insights, actions

# ----------------------------
# RUN
# ----------------------------
if st.button("Analyze"):

    with st.spinner("Analyzing..."):
        prices = get_prices(url)
        level, price_range, strategy = analyze_prices(prices)
        insights, actions = generate_insights(level, strategy)

    st.markdown(f"## 🔍 {url}")

    # ----------------------------
    # SUMMARY
    # ----------------------------
    st.markdown("## 📊 Summary")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card green">
        <div class="label">Positioning</div>
        <div class="metric">{level}</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card blue">
        <div class="label">Price Range</div>
        <div class="metric">{price_range}</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card orange">
        <div class="label">Strategy</div>
        <div class="metric">{strategy}</div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # PRICES GRID
    # ----------------------------
    st.markdown("## 💰 Detected Prices")

    if prices:
        cols = st.columns(4)
        for i, p in enumerate(prices):
            cols[i % 4].markdown(f"""
            <div class="card">
                <div class="price">{p}</div>
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
        <div class="card green">
            {i}
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------
    # ACTIONS
    # ----------------------------
    st.markdown("## 🚀 What You Should Do")

    for a in actions:
        st.markdown(f"""
        <div class="card orange">
            {a}
        </div>
        """, unsafe_allow_html=True)

    st.success("Analysis Complete ✅")
