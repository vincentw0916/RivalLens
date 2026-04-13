import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

st.set_page_config(page_title="RivalLens Pro", layout="wide")

# ---------------- UI FIX (HIGH CONTRAST) ----------------
st.markdown("""
<style>
body { background-color: #0e1117; }

.card {
    background: #161b22;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #30363d;
    margin-bottom: 12px;
    color: white;
}

.metric {
    font-size: 26px;
    font-weight: bold;
    color: white;
}

.label {
    color: #9da7b3;
    font-size: 13px;
}

.section {
    margin-top: 30px;
    margin-bottom: 10px;
    font-size: 22px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- URL FIX ----------------
def fix_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url

# ---------------- SCRAPER ----------------
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

# ---------------- DEEP ANALYSIS ----------------
def analyze(nums):

    avg = np.mean(nums)
    median = np.median(nums)
    low = min(nums)
    high = max(nums)
    spread = high - low

    tiers = len(set(nums))

    insights = []
    actions = []

    # POSITION
    if avg < 50:
        position = "Low-cost"
    elif avg < 150:
        position = "Mid-market"
    else:
        position = "Premium"

    # STRUCTURE
    if tiers <= 3:
        structure = "Simple pricing"
        insights.append("Very limited pricing tiers → weak segmentation strategy")
        actions.append("Introduce multiple tiers to capture different customer groups")

    elif tiers <= 10:
        structure = "Tiered pricing"
        insights.append("Uses structured pricing tiers → standard competitive model")

    else:
        structure = "Complex catalog"
        insights.append("Large number of price points → broad product coverage")
        actions.append("Focus on a niche instead of competing broadly")

    # SPREAD ANALYSIS
    if spread < 40:
        insights.append("Tight price range → poor differentiation")
        actions.append("Create clear premium vs budget tiers to stand out")

    elif spread > 100:
        insights.append("Wide pricing spread → targeting multiple segments")
        actions.append("Identify and dominate one profitable segment")

    # PRICING PSYCHOLOGY
    endings = [str(n).split('.')[-1] for n in nums if '.' in str(n)]
    if any(e in ["99", "95"] for e in endings):
        insights.append("Uses psychological pricing (.99/.95) → optimized for conversions")
    else:
        insights.append("Rounded pricing → likely premium or simplified positioning")

    # COMPETITIVE LOGIC
    if position == "Low-cost":
        insights.append("Competing primarily on price → likely thin margins and high competition")
        actions.append("Avoid price war — win via branding, bundles, or perceived value")

    elif position == "Mid-market":
        insights.append("Positioned in the middle → risk of being undifferentiated")
        actions.append("Move clearly upmarket or downmarket to avoid being stuck")

    else:
        insights.append("Premium positioning → strong margins but smaller audience")
        actions.append("Win through brand authority and trust signals")

    return {
        "avg": avg,
        "median": median,
        "low": low,
        "high": high,
        "spread": spread,
        "tiers": tiers,
        "structure": structure,
        "position": position
    }, insights, actions

# ---------------- UI ----------------
st.title("🔎 RivalLens Pro")
st.caption("Deep competitor pricing intelligence")

url = st.text_input("Enter competitor website")

if st.button("Analyze"):

    prices = get_prices(url)

    if not prices:
        st.error("No pricing data detected (site may use JavaScript or hidden pricing)")
        st.stop()

    data, insights, actions = analyze(prices)

    st.markdown(f"### 🔍 {fix_url(url)}")

    # -------- SUMMARY --------
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
    <div class="label">Median</div>
    <div class="metric">${int(data['median'])}</div>
    </div>
    """, unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="card">
    <div class="label">Model</div>
    <div class="metric">{data['structure']}</div>
    </div>
    """, unsafe_allow_html=True)

    # -------- GRAPH --------
    st.markdown('<div class="section">📊 Price Distribution</div>', unsafe_allow_html=True)

    hist = np.histogram(prices, bins=5)

    chart_data = {
        "Range": [f"${int(hist[1][i])}-{int(hist[1][i+1])}" for i in range(len(hist[0]))],
        "Count": hist[0]
    }

    st.bar_chart(chart_data, x="Range", y="Count")

    st.caption("Shows how many products fall into each price range")

    # -------- INSIGHTS --------
    st.markdown('<div class="section">🧠 Insights</div>', unsafe_allow_html=True)

    for i in insights:
        st.markdown(f"<div class='card'>{i}</div>", unsafe_allow_html=True)

    # -------- ACTIONS --------
    st.markdown('<div class="section">🚀 What You Should Do</div>', unsafe_allow_html=True)

    for a in actions:
        st.markdown(f"<div class='card'>{a}</div>", unsafe_allow_html=True)

    st.success("Analysis complete")
