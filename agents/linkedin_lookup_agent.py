# This agent will receive the name of the person and return the LinkedIn profile URL of that person
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url  

dotenv_path = ".env"  # Ensure correct path
load_dotenv(dotenv_path)
if not load_dotenv(dotenv_path):
    print("Failed to load .env file!")


# Retrieve values from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_project_name = os.getenv("OPENAI_PROJECT_NAME")


if not openai_api_key:
    print("Error: OPENAI_API_KEY is missing!")
if not openai_project_name:
    print("Error: OPENAI_PROJECT_NAME is missing!")


def lookup(name: str) -> str:
    """Looks up the LinkedIn information about a person and returns the LinkedIn profile URL of that person."""
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url=f"https://www.linkedin.com/in/{name}/", mock=False)
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
        openai_api_key=openai_api_key
    )
    template = """ Given the name {name_of_person}, I want you to find their LinkedIn profile URL. Your response should only be the URL. 
                    Here's an example of the expected output: https://www.linkedin.com/in/abkpk/"""
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"],
        template=template
    )

    # tools
    tools_for_agent = [
        Tool(
            name="Search Google for the LinkedIn profile URL of the person",
            func=get_profile_url,
            description="Looks up the LinkedIn profile URL of a person by their name.",
        )
    ]

    react_prompt = hub.pull("hwchase17/react") # this a predefined react prompt that we can pull inot our code, rather than creating a new one. This prompt is sent tot he LLM. 
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt,
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
    ) # this is the final agent. or the agent that will be used to execute the task.

    # invoke the agent
    result = agent_executor.invoke(
        input={
            "input": prompt_template.format(name_of_person=name),
        }
    )

    # output parser.
    linkedin_profile_url = result["output"]
    # return "https://www.linkedin.com/in/abkpk/"
    return linkedin_profile_url

if __name__ == '__main__':
    # Test the lookup function
    name = "Karthick Appadurai Baskaran"
    linkedin_profile_url = lookup(name)
    print(f"LinkedIn profile URL of {name}: {linkedin_profile_url}")