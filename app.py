import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import os
from openai import OpenAI

# -----------------------------
# 🔐 OpenAI setup (Streamlit secrets)
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# 🔍 Price scraper
# -----------------------------
def get_prices(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        prices = re.findall(r"\$\d+(?:\.\d{1,2})?", text)

        return prices[:10] if prices else ["No prices found"]

    except Exception as e:
        return [f"Error: {str(e)}"]

# -----------------------------
# 🤖 AI Analysis
# -----------------------------
def analyze_with_ai(url, prices):
    try:
        prompt = f"""
        You are a business strategist.

        Analyze this competitor:

        Website: {url}
        Prices found: {prices}

        Give:
        1. Pricing strategy (premium, low-cost, etc)
        2. Target market
        3. Weaknesses
        4. What I should do to beat them
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"

# -----------------------------
# 🎯 UI
# -----------------------------
st.set_page_config(page_title="RivalLens", page_icon="🔍")

st.title("RivalLens 🔍")
st.write("AI-powered competitor pricing intelligence")

url = st.text_input("Enter competitor website")

if st.button("Analyze"):
    if not url:
        st.warning("Enter a URL")
    else:
        st.write(f"Analyzing: {url}")

        prices = get_prices(url)

        st.subheader("💰 Detected Prices")
        st.write(prices)

        if "Error" in prices[0]:
            st.error("Failed to fetch website")

        else:
            st.subheader("🤖 AI Analysis")

            with st.spinner("Analyzing with AI..."):
                result = analyze_with_ai(url, prices)

            st.write(result)

        st.success("Done ✅")
