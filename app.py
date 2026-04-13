import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# -----------------------------
# 🔍 Price Scraper (Improved)
# -----------------------------
def get_prices(url):
    try:
        # Auto-add https if missing
        if not url.startswith("http"):
            url = "https://" + url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return [f"Error: Website returned status {response.status_code}"]

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Find prices like $19.99
        prices = re.findall(r"\$\d+(?:\.\d{1,2})?", text)

        return prices[:5] if prices else ["No prices found"]

    except Exception as e:
        return [f"Error: {str(e)}"]


# -----------------------------
# 🎯 Streamlit UI
# -----------------------------
st.set_page_config(page_title="RivalLens", page_icon="🔍")

st.title("RivalLens 🔍")
st.write("AI-powered competitor pricing analysis")

url = st.text_input(
    "Enter competitor website (e.g. https://example.com or just domain)"
)

if st.button("Analyze"):
    if not url:
        st.warning("Please enter a website URL")
    else:
        st.write(f"Analyzing: {url}")

        prices = get_prices(url)

        st.subheader("💰 Detected Prices")
        st.write(prices)

        # -----------------------------
        # 📊 Basic Insights
        # -----------------------------
        if "Error" in prices[0]:
            st.error("Failed to fetch website")
        elif prices == ["No prices found"]:
            st.info("No pricing detected (site may block scraping or use dynamic loading)")
        else:
            st.subheader("📊 Basic Insight")

            st.write("• Competitor shows visible pricing")
            st.write("• Likely targeting transparent pricing strategy")
            st.write("• Consider undercutting or adding value bundles")
            st.write("• Opportunity: differentiate instead of price war")

        st.success("Done ✅")
