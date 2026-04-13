import streamlit as st
import requests
from bs4 import BeautifulSoup

# -----------------------------
# 🔍 Simple price scraper
# -----------------------------
def get_prices(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text()

        import re
        prices = re.findall(r"\$\d+(?:\.\d{1,2})?", text)

        return prices[:5] if prices else ["No prices found"]

    except Exception as e:
        return [f"Error: {str(e)}"]


# -----------------------------
# 🎯 UI
# -----------------------------
st.title("RivalLens 🔍")
st.write("AI-powered competitor pricing analysis")

url = st.text_input("Enter competitor website (e.g. https://example.com)")

if st.button("Analyze"):
    if not url:
        st.warning("Please enter a website URL")
    else:
        st.write("Analyzing:", url)

        prices = get_prices(url)

        st.subheader("💰 Detected Prices")
        st.write(prices)

        # Simple analysis (no API needed yet)
        if "Error" in prices[0]:
            st.error("Failed to fetch website")
        elif prices == ["No prices found"]:
            st.info("No pricing detected on this page")
        else:
            st.subheader("📊 Basic Insight")

            st.write("• Competitor likely uses visible pricing")
            st.write("• Consider undercutting or bundling strategy")
            st.write("• Opportunity: add value instead of price war")

        st.success("Done ✅")
