import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="RivalLens Pro", layout="wide")

# -----------------------------
# CLEAN UI (FIXED COLORS)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #ffffff;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #ffffff;
}

.card {
    background: #161b22;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #30363d;
}

.green { border-left: 4px solid #2ea043; }
.blue { border-left: 4px solid #58a6ff; }
.orange { border-left: 4px solid #f0883e; }

.big {
    font-size: 22px;
    font-weight: bold;
}

.small {
    color: #8b949e;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# URL FIX
# -----------------------------
def fix_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url

# -----------------------------
# SCRAPER
# -----------------------------
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

# -----------------------------
# DEEP ANALYSIS ENGINE
# -----------------------------
def deep_analysis(nums):

    if not nums:
        return {}, ["No pricing data detected"], ["Manual review required"]

    avg = np.mean(nums)
    low = min(nums)
    high = max(nums)
    spread = high - low

    insights = []
    actions = []

    # POSITION
    if avg < 50:
        position = "Low-cost"
    elif avg < 150:
        position = "Mid-market"
    else:
        position = "Premium"

    # STRATEGY
    if spread > 100:
        strategy = "Multi-tier segmentation"
        insights.append("Wide pricing range → multiple customer segments targeted")
        actions.append("Exploit gaps between tiers with focused offer")

    elif spread < 30:
        strategy = "Flat pricing"
        insights.append("Tight pricing → weak differentiation")
        actions.append("Introduce clearer tiers to outperform")

    else:
        strategy = "Moderate tiered pricing"
        insights.append("Balanced pricing structure → standard competitive setup")

    # PSYCHOLOGY
    endings = [str(n).split('.')[-1] for n in nums if '.' in str(n)]
    if any(e in ["99", "95"] for e in endings):
        insights.append("Uses psychological pricing (.99/.95) → conversion focused")
    else:
        insights.append("Rounded pricing → premium or simplified positioning")

    # CUSTOMER TARGET
    if avg < 50:
        insights.append("Targeting price-sensitive customers")
        actions.append("Compete with branding, not price war")

    elif avg < 150:
        insights.append("Targeting mass market")
        actions.append("Differentiate strongly — avoid middle positioning")

    else:
        insights.append("Targeting premium buyers")
        actions.append("Win via authority, trust, and brand perception")

    # PRODUCT DEPTH
    if len(nums) > 15:
        insights.append("Large catalog → volume-based strategy")
        actions.append("Win by specializing in a niche")

    else:
        insights.append("Focused offering → niche positioning")

    # WEAKNESSES
    if spread < 40:
        insights.append("Weak tier separation → opportunity to outperform with clear pricing ladder")
        actions.append("Create 3 clear packages (basic / pro / premium)")

    # SCORE
    score = int((spread + avg) / 2)
    score = max(30, min(score, 95))

    return {
        "avg": avg,
        "low": low,
        "high": high,
        "position": position,
        "strategy": strategy,
        "score": score
    }, insights, actions


# -----------------------------
# UI
# -----------------------------
st.title("🔎 RivalLens Pro")
st.caption("Real competitor pricing intelligence")

url = st.text_input("Enter competitor website")

if st.button("Analyze"):

    prices = get_prices(url)
    data, insights, actions = deep_analysis(prices)

    st.markdown(f"### 🔍 {fix_url(url)}")

    # -----------------------------
    # SUMMARY CARDS
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="card green">
        <div class="small">Position</div>
        <div class="big">{data.get('position')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card blue">
        <div class="small">Price Range</div>
        <div class="big">${int(data.get('low',0))} - ${int(data.get('high',0))}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card orange">
        <div class="small">Strategy</div>
        <div class="big">{data.get('strategy')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="card">
        <div class="small">Score</div>
        <div class="big">{data.get('score')}/100</div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # CHART
    # -----------------------------
    if prices:
        st.subheader("📊 Price Distribution")
        st.bar_chart(prices)

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    st.subheader("🧠 Insights")
    for i in insights:
        st.markdown(f"""
        <div class="card green">{i}</div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # ACTION PLAN
    # -----------------------------
    st.subheader("🚀 What You Should Do")
    for a in actions:
        st.markdown(f"""
        <div class="card orange">{a}</div>
        """, unsafe_allow_html=True)

    st.success("Analysis complete")
