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
# Setup
# ------------------------
st.set_page_config(page_title="RivalLens Pro V9", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

DATA_FILE = "history.json"

# ------------------------
# Storage (simple local DB)
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
# Styling (FIXED)
# ------------------------
st.markdown("""
<style>
body { background-color: #0f172a; color: #e5e7eb; }
.card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
}
.green { border-left: 5px solid #22c55e; }
.blue { border-left: 5px solid #3b82f6; }
.orange { border-left: 5px solid #f59e0b; }
.red { border-left: 5px solid #ef4444; }
.title { font-size: 34px; font-weight: 700; }
.subtitle { color: #9ca3af; }
</style>
""", unsafe_allow_html=True)

# ------------------------
# Helpers
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
# AI Analysis (STRUCTURED)
# ------------------------
def ai_analysis(prices, url):

    if not prices:
        return {
            "positioning": "Unknown",
            "strategy": "Hidden pricing",
            "insights": ["No visible pricing detected"],
            "actions": ["Manual review required"]
        }

    prompt = f"""
You are a senior competitive strategy consultant.

Data:
Prices: {prices}
Website: {url}

Return STRICT JSON:
{{
"positioning": "",
"strategy": "",
"insights": ["", "", "", "", ""],
"actions": ["", "", "", "", ""]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {
            "positioning": "Error",
            "strategy": "Parsing failed",
            "insights": ["AI output error"],
            "actions": ["Retry"]
        }

# ------------------------
# UI Layout
# ------------------------
st.markdown('<div class="title">🔎 RivalLens Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Competitor pricing intelligence dashboard</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Analyze", "📁 History"])

# ========================
# TAB 1: ANALYZE
# ========================
with tab1:

    url = st.text_input("Enter competitor website")

    if st.button("Analyze"):

        with st.spinner("Running analysis..."):

            raw = get_prices(url)
            prices = clean_prices(raw)
            analysis = ai_analysis(prices, url)

        st.markdown(f"### 🔗 {normalize_url(url)}")

        # Summary
        if prices:
            min_p, max_p = min(prices), max(prices)
            avg = round(np.mean(prices), 2)

            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="card green"><b>Position</b><br>{analysis["positioning"]}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="card blue"><b>Range</b><br>${min_p} - ${max_p}</div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="card orange"><b>Strategy</b><br>{analysis["strategy"]}</div>', unsafe_allow_html=True)

            # Chart
            st.subheader("📊 Price Distribution")
            fig, ax = plt.subplots()
            ax.hist(prices, bins=5)
            ax.set_xlabel("Price ($)")
            ax.set_ylabel("Count")
            st.pyplot(fig)

        else:
            st.warning("No prices found")

        # Insights
        st.subheader("🧠 Insights")
        for i in analysis["insights"]:
            st.markdown(f'<div class="card green">{i}</div>', unsafe_allow_html=True)

        # Actions
        st.subheader("🚀 Strategy")
        for a in analysis["actions"]:
            st.markdown(f'<div class="card orange">{a}</div>', unsafe_allow_html=True)

        # Save
        save_history({
            "url": url,
            "prices": prices,
            "analysis": analysis
        })

# ========================
# TAB 2: HISTORY
# ========================
with tab2:

    history = load_history()

    if not history:
        st.info("No history yet")
    else:
        for item in reversed(history[-10:]):
            st.markdown(f"### 🔗 {item['url']}")
            st.write(item["analysis"]["positioning"], "-", item["analysis"]["strategy"])
