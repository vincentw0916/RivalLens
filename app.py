import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import matplotlib.pyplot as plt
from openai import OpenAI
import json
import os

# ------------------------
# CONFIG
# ------------------------
st.set_page_config(page_title="RivalLens Pro", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

DATA_FILE = "history.json"

# ------------------------
# STORAGE
# ------------------------
def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f)

# ------------------------
# UI STYLING (FIXED COLORS)
# ------------------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0f172a;
    color: #e5e7eb;
}

/* Cards */
.card {
    background: #111827;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    font-size: 15px;
    color: #f9fafb;
}

/* Color accents */
.green { border-left: 5px solid #22c55e; }
.blue { border-left: 5px solid #3b82f6; }
.orange { border-left: 5px solid #f59e0b; }

/* Titles */
.title {
    font-size: 34px;
    font-weight: 700;
    color: #ffffff;
}
.subtitle {
    color: #9ca3af;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# HELPERS
# ------------------------
def normalize_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url

def get_prices(url):
    try:
        url = normalize_url(url)
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        prices = re.findall(r"\$\s?\d+(?:\.\d{1,2})?", text)

        return list(set(prices))[:20]
    except:
        return []

def clean_prices(prices):
    nums = []
    for p in prices:
        try:
            nums.append(float(p.replace("$", "")))
        except:
            pass
    return nums

# ------------------------
# AI ANALYSIS (SAFE)
# ------------------------
def ai_analysis(prices, url):

    if not prices:
        return {
            "positioning": "Unknown",
            "strategy": "Hidden pricing",
            "insights": [
                "No visible pricing detected",
                "Likely consultation-based funnel",
                "Possible premium positioning",
                "Reduced price transparency",
                "Higher friction in conversion"
            ],
            "actions": [
                "Use transparent pricing to win trust",
                "Offer quick purchase options",
                "Highlight pricing tiers clearly",
                "Test entry-level offers",
                "Improve conversion flow"
            ]
        }

    prompt = f"""
You are a senior competitive strategist.

Analyze:
Prices: {prices}
Website: {url}

Return JSON ONLY:

{{
"positioning": "",
"strategy": "",
"insights": ["", "", "", "", ""],
"actions": ["", "", "", "", ""]
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        start = content.find("{")
        end = content.rfind("}") + 1
        json_str = content[start:end]

        return json.loads(json_str)

    except:
        avg = sum(prices) / len(prices)

        return {
            "positioning": "Low-cost" if avg < 50 else "Mid-range",
            "strategy": "Competitive pricing",
            "insights": [
                "Pricing suggests competitive positioning",
                "Limited differentiation in tiers",
                "Targets price-sensitive segment",
                "No strong premium anchor",
                "Relatively simple pricing model"
            ],
            "actions": [
                "Differentiate beyond price",
                "Introduce premium tier",
                "Improve value perception",
                "Bundle products/services",
                "Strengthen branding"
            ]
        }

# ------------------------
# UI HEADER
# ------------------------
st.markdown('<div class="title">🔎 RivalLens Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Competitor pricing intelligence dashboard</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Analyze", "📁 History"])

# ========================
# ANALYZE TAB
# ========================
with tab1:

    url = st.text_input("Enter competitor website")

    if st.button("Analyze"):

        with st.spinner("Analyzing competitor..."):

            raw_prices = get_prices(url)
            prices = clean_prices(raw_prices)
            analysis = ai_analysis(prices, url)

        st.markdown(f"### 🔗 {normalize_url(url)}")

        # ------------------------
        # SUMMARY CARDS
        # ------------------------
        if prices:
            min_p, max_p = min(prices), max(prices)
            avg = round(np.mean(prices), 2)

            c1, c2, c3 = st.columns(3)

            c1.markdown(f'<div class="card green"><b>Position</b><br>{analysis["positioning"]}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="card blue"><b>Range</b><br>${min_p} - ${max_p}</div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="card orange"><b>Strategy</b><br>{analysis["strategy"]}</div>', unsafe_allow_html=True)

            # ------------------------
            # CHART (FIXED SIZE)
            # ------------------------
            st.subheader("📊 Price Distribution")

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.hist(prices, bins=5)
            ax.set_xlabel("Price ($)")
            ax.set_ylabel("Products")
            ax.set_title("Price Spread")
            ax.grid(alpha=0.2)

            st.pyplot(fig)

        else:
            st.warning("No pricing found")

        # ------------------------
        # INSIGHTS
        # ------------------------
        st.subheader("🧠 Insights")

        for i in analysis["insights"]:
            st.markdown(f'<div class="card green">{i}</div>', unsafe_allow_html=True)

        # ------------------------
        # ACTIONS
        # ------------------------
        st.subheader("🚀 What You Should Do")

        for a in analysis["actions"]:
            st.markdown(f'<div class="card orange">{a}</div>', unsafe_allow_html=True)

        # ------------------------
        # SAVE
        # ------------------------
        save_history({
            "url": url,
            "analysis": analysis
        })

# ========================
# HISTORY TAB
# ========================
with tab2:

    history = load_history()

    if not history:
        st.info("No history yet")
    else:
        for item in reversed(history[-10:]):
            st.markdown(f"### 🔗 {item['url']}")
            st.write(item["analysis"]["positioning"], "-", item["analysis"]["strategy"])
