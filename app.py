import os
import requests
from bs4 import BeautifulSoup
from crewai import Agent, Task, Crew

# 🔐 Your API key
import os
api_key = os.getenv("OPENAI_API_KEY")

# 🧠 LLM
llm = "gpt-4o-mini"

# 🌐 Function to scrape prices
def get_prices(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        prices = []
        for tag in soup.find_all(["span", "div", "p"]):
            text = tag.get_text()
            if "$" in text:
                prices.append(text.strip())

        return list(set(prices))[:10]

    except:
        return ["Could not extract prices"]

# 👇 Ask user for website
while True:
    url = input("\nEnter competitor website (or type 'exit'): ")

    if url.lower() == "exit":
        break

    prices = get_prices(url)

    task = Task(
        description=f"""
        Competitor website: {url}

        Detected prices: {prices}

        Analyze:
        1. Pricing strategy
        2. Market positioning
        3. What we should do
        """,
        expected_output="Clear pricing strategy and recommendation",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()

    print("\n=== COMPETITOR ANALYSIS ===\n")
    print(result)

# 🔍 Get prices
prices = get_prices(url)

# 🤖 Agent
agent = Agent(
    role="Competitor Analyst",
    goal="Analyze competitor pricing and suggest strategy",
    backstory="Expert in pricing strategy and e-commerce",
    llm=llm
)

# 📋 Task
task = Task(
    description=f"""
    Competitor website: {url}

    Detected prices: {prices}

    Analyze:
    1. Pricing strategy
    2. Market positioning
    3. What we should do
    """,
    expected_output="Clear pricing strategy and recommendation",
    agent=agent
)

# 🚀 Run
crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()

print("\n=== COMPETITOR ANALYSIS ===\n")
print(result)