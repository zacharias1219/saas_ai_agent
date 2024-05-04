#!/usr/bin/env python
from saas_ai_agent.crew import SaaSCrew
from dotenv import load_dotenv
import agentops

load_dotenv()
agentops.init()

def get_product_idea():
    # In a real-world application, this might query a database or an input form
    # Here, we'll simulate obtaining an idea description from the user
    print("🚀 Please enter a brief description of your SaaS product idea:")
    idea_description = input()
    return idea_description

def run():
    product_idea = get_product_idea()
    if not product_idea:
        print("🚨 No product idea provided.")
        return

    inputs = {
        "product_idea": product_idea,
        "market_analysis": True,
        "technology_assessment": True,
        "financial_projection": True
    }

    crew = SaaSCrew()
    result = crew.crew().kickoff(inputs=inputs)
    print("Analysis Result:")
    print(result)


if __name__ == "__main__":
    run()
