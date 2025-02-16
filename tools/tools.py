from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

dotenv_path = ".env"  # Ensure correct path
load_dotenv(dotenv_path)
if not load_dotenv(dotenv_path):
    print("Failed to load .env file!")


# Retrieve values from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_project_name = os.getenv("OPENAI_PROJECT_NAME")
scrapin_api_key = os.getenv("SCRAPIN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")


def get_profile_url(name: str) -> str:
    """This function looks up the LinkedIn information about a person and returns the LinkedIn profile URL of that person."""
    search = TavilySearchResults()
    res = search.run(
        f"{name}"
    )
    return res
    
