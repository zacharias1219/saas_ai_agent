from crewai_tools import BaseTool
import requests
import os
import logging

# Base class for SaaS related tools
class BaseSaaSTool(BaseTool):
    def handle_api_error(self, response):
        """Handle common API errors based on response status code."""
        if response.status_code == 400:
            raise Exception("Bad Request - Query was malformed.")
        elif response.status_code == 401:
            raise Exception("Unauthorized - API key is invalid.")
        elif response.status_code == 403:
            raise Exception("Forbidden - Access to the resource is denied.")
        elif response.status_code == 404:
            raise Exception("Not Found - The specified resource was not found.")
        else:
            response.raise_for_status()  # Raise any other HTTP errors as exceptions

class SaasDataTool(BaseSaaSTool):
    name: str = "SaaS Market Data Fetcher"
    description: str = "Fetches and processes market data relevant to the SaaS industry from various API endpoints."

    def _run(self, query_params: dict) -> list:
        """Fetch market data from a specified API endpoint based on query parameters."""
        data_collected = []
        base_url = "https://api.saas-market-data.com/v1/reports"  # Example API URL
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(base_url, headers=headers, params=query_params)
            if response.status_code == 200:
                data = response.json()
                data_collected = self.process_data(data)
            else:
                self.handle_api_error(response)
        except Exception as e:
            logging.error(f"Failed to fetch or process data: {str(e)}")
            return f"Error: {str(e)}"

        return data_collected

    def process_data(self, data):
        """Process and format the data fetched from API."""
        processed_data = []
        for item in data.get("results", []):
            processed_item = {
                "title": item.get("title"),
                "summary": item.get("summary"),
                "date": item.get("date"),
                "source": item.get("source")
            }
            processed_data.append(processed_item)
        return processed_data

class TechnologyTool(BaseSaaSTool):
    name: str = "Technology Stack Analyzer"
    description: str = "Analyzes and recommends technology stacks suitable for SaaS applications based on current trends."

    def _run(self, tech_requirements: dict) -> list:
        """Fetch and analyze technology stacks from an API."""
        tech_data = []
        base_url = "https://api.technology-trends.com/v1/techstacks"  # Example API URL
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(base_url, headers=headers, params=tech_requirements)
            if response.status_code == 200:
                data = response.json()
                tech_data = self.analyze_technology(data)
            else:
                self.handle_api_error(response)
        except Exception as e:
            logging.error(f"Failed to fetch or analyze technology data: {str(e)}")
            return f"Error: {str(e)}"

        return tech_data

    def analyze_technology(self, data):
        """Process and evaluate technology options."""
        analyzed_data = []
        for tech in data.get("technologies", []):
            analyzed_data.append({
                "technology": tech["name"],
                "advantages": tech["advantages"],
                "popularity": tech["popularity"]
            })
        return analyzed_data

class FinancialTool(BaseSaaSTool):
    name: str = "Financial Analysis Tool"
    description: str = "Performs financial analysis and projections for SaaS products."

    def _run(self, financial_params: dict) -> list:
        """Perform financial analysis based on provided parameters."""
        financial_analysis = []
        base_url = "https://api.financial-projections.com/v1/analyze"  # Example API URL
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(base_url, headers=headers, params=financial_params)
            if response.status_code == 200:
                data = response.json()
                financial_analysis = self.process_financial_data(data)
            else:
                self.handle_api_error(response)
        except Exception as e:
            logging.error(f"Failed to perform financial analysis: {str(e)}")
            return f"Error: {str(e)}"

        return financial_analysis

    def process_financial_data(self, data):
        """Extract and format financial data for reporting."""
        formatted_data = []
        for financial_item in data.get("results", []):
            formatted_data.append({
                "type": financial_item["type"],
                "value": financial_item["value"],
                "description": financial_item["description"]
            })
        return formatted_data
