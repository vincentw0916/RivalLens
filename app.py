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
# INPUT SECTION
# --------------------------
st.subheader("🔗 Enter Competitor Website")

url = st.text_input(
    "",
    placeholder="https://example.com or just domain (e.g. shop.com)"
)

analyze_btn = st.button("Analyze")

# --------------------------
# FUNCTIONS
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

        return list(set(prices))[:10] if prices else []

    except Exception as e:
        return [f"Error: {str(e)}"]


def analyze_pricing(prices):
    numeric_prices = []

    for p in prices:
        try:
            value = float(p.replace("$", "").replace(",", ""))
            numeric_prices.append(value)
        except:
            continue

    if not numeric_prices:
        return {
            "level": "Unknown",
            "range": "N/A",
            "strategy": "No visible pricing"
        }

    avg_price = sum(numeric_prices) / len(numeric_prices)

    if avg_price < 50:
        level = "Low-cost"
    elif avg_price < 300:
        level = "Mid-range"
    else:
        level = "Premium"

    return {
        "level": level,
        "range": f"${min(numeric_prices)} - ${max(numeric_prices)}",
        "strategy": "Transparent pricing"
    }


# --------------------------
# MAIN LOGIC
# --------------------------
if analyze_btn and url:

    st.markdown("---")
    st.subheader(f"🔍 Analyzing: {url}")

    prices = get_prices(url)

    if not prices or "Error" in prices[0]:
        st.error("❌ Could not extract pricing data")
    else:
        summary = analyze_pricing(prices)

        # --------------------------
        # 🔥 SUMMARY (TOP CARD)
        # --------------------------
        st.markdown("## 📊 Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Pricing Level", summary["level"])
        col2.metric("Price Range", summary["range"])
        col3.metric("Strategy", summary["strategy"])

        st.markdown("---")

        # --------------------------
        # 💰 DETECTED PRICES
        # --------------------------
        st.markdown("## 💰 Detected Prices")
        st.write(prices)

        st.markdown("---")

        # --------------------------
        # 🧠 INSIGHTS
        # --------------------------
        st.markdown("## 🧠 Key Insights")

        st.markdown(f"""
        - Competitor uses **{summary['strategy']}**
        - Positioned as **{summary['level']} market**
        - Pricing spans **{summary['range']}**
        - Likely targeting value-conscious vs premium buyers depending on range
        """)

        st.markdown("---")

        # --------------------------
        # 🚀 ACTION PLAN
        # --------------------------
        st.markdown("## 🚀 What You Should Do")

        st.markdown("""
        - Undercut slightly OR add more value (bundles, bonuses)
        - Improve website clarity (pricing transparency wins conversions)
        - Differentiate instead of competing only on price
        - Use urgency/offers to outperform competitor positioning
        """)

        st.success("✅ Analysis Complete")
