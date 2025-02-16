from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import summary_parser

# information = ["Tim Cook is the CEO of Apple.","Elon Musk is the CEO of Tesla."] 
# information = "Tim Cook is the CEO of Apple."

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

# Print project name (for debugging)
print(f"Using OpenAI Project: {openai_project_name}")

def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username,
        mock=True
    )
    summary_template = """
        given the LinkedIn information {information} about a person, I want you to create:
        1. a short summary
        2. two interesting facts about them

        \n{format_instructions}
    """
    # the {information} is a placeholder that will be replaced by the actual information about the person. Its similar to a variable in programming.
    summary_prompt_tempate = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions(),
        },
    )

    # now we will create a chat model
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", openai_api_key=openai_api_key)
    # chain = summary_prompt_tempate | llm  | StrOutputParser()
    chain = summary_prompt_tempate | llm | summary_parser

    # information = scrape_linkedin_profile(
    #     # linkedin_profile_url="https://www.linkedin.com/in/abkpk/",
    #     linkedin_profile_url="https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json",
    #     mock=True
    # )

    res = chain.invoke(input = {"information": linkedin_data})
    
    return res


if __name__ == '__main__':
    print(
        ice_break_with(
            name="Name_of_the_person",
        )
    )