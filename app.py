import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

st.set_page_config(page_title="RivalLens Pro", layout="wide")

# ----------------------------
# STYLE
# ----------------------------
st.markdown("""
<style>
.main { background-color: #f8fafc; }

.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

.metric { font-size: 26px; font-weight: bold; }
.label { color: #64748b; font-size: 14px; }

.green { border-left: 5px solid #22c55e; }
.orange { border-left: 5px solid #f59e0b; }
.blue { border-left: 5px solid #3b82f6; }

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.title("🔎 RivalLens Pro")
st.caption("Competitor pricing intelligence dashboard")

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
        return list(set(prices))[:30]

    except:
        return []

# ----------------------------
# ANALYSIS
# ----------------------------
def analyze(prices):
    nums = []

    for p in prices:
        try:
            nums.append(float(p.replace("$","")))
        except:
            pass

    if not nums:
        return None

    avg = sum(nums)/len(nums)
    low, high = min(nums), max(nums)

    if avg < 50:
        level = "Low-cost"
    elif avg < 150:
        level = "Mid-range"
    else:
        level = "Premium"

    spread = high - low

    if spread < 30:
        strategy = "Flat"
    elif spread < 100:
        strategy = "Tiered"
    else:
        strategy = "Wide"

    return nums, level, low, high, strategy

# ----------------------------
# SCORE SYSTEM
# ----------------------------
def score(level, strategy, count):
    s = 0

    if level == "Premium":
        s += 30
    elif level == "Mid-range":
        s += 20
    else:
        s += 10

    if strategy == "Tiered":
        s += 30
    elif strategy == "Wide":
        s += 20

    if count > 10:
        s += 20

    return min(s,100)

# ----------------------------
# GAP DETECTION
# ----------------------------
def gap_analysis(level, strategy):
    gaps = []

    if level != "Premium":
        gaps.append("Opportunity to introduce premium tier")

    if strategy != "Tiered":
        gaps.append("Lack of structured pricing tiers")

    gaps.append("Potential weak differentiation")

    return gaps

# ----------------------------
# RUN
# ----------------------------
if st.button("Analyze"):

    prices = get_prices(url)
    result = analyze(prices)

    if not result:
        st.warning("No pricing data found")
    else:
        nums, level, low, high, strategy = result

        comp_score = score(level, strategy, len(nums))
        gaps = gap_analysis(level, strategy)

        st.markdown(f"## 🔍 {url}")

        # ----------------------------
        # SUMMARY
        # ----------------------------
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f'<div class="card green"><div class="label">Position</div><div class="metric">{level}</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="card blue"><div class="label">Range</div><div class="metric">${low:.0f}–${high:.0f}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="card orange"><div class="label">Strategy</div><div class="metric">{strategy}</div></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="card"><div class="label">Score</div><div class="metric">{comp_score}/100</div></div>', unsafe_allow_html=True)

        # ----------------------------
        # CHART
        # ----------------------------
        st.markdown("## 📊 Price Distribution")

        df = pd.DataFrame(nums, columns=["Price"])
        st.bar_chart(df)

        # ----------------------------
        # INSIGHTS
        # ----------------------------
        st.markdown("## 🧠 Insights")

        st.markdown(f"""
        <div class="card green">
        Competitor operates in <b>{level}</b> segment with <b>{strategy}</b> pricing.
        </div>
        """, unsafe_allow_html=True)

        # ----------------------------
        # GAPS
        # ----------------------------
        st.markdown("## 🕳 Market Gaps")

        for g in gaps:
            st.markdown(f'<div class="card orange">{g}</div>', unsafe_allow_html=True)

        # ----------------------------
        # ACTIONS
        # ----------------------------
        st.markdown("## 🚀 Strategy")

        st.markdown(f"""
        <div class="card blue">
        - Position slightly above or below {level} competitor  
        - Introduce clearer pricing tiers  
        - Improve perceived value vs price  
        </div>
        """, unsafe_allow_html=True)

        st.success("Analysis Complete")
