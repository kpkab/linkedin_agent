import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool, tool
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain.schema import AgentAction, AgentFinish
from typing import Union, List

dotenv_path = ".env"  # Ensure correct path
load_dotenv(dotenv_path)
if not load_dotenv(dotenv_path):
    print("Failed to load .env file!")


# Retrieve values from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_project_name = os.getenv("OPENAI_PROJECT_NAME")


@tool
def get_text_length(text: str) -> int:
    """Get the length of the text."""
    text = text.strip("'\n").strip('"')
    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")

if __name__ == "__main__":
    # print(get_text_length("Hello world!")) # this will give the following error. 
    """
    LangChainDeprecationWarning: The method `BaseTool.__call__` was deprecated in langchain-core 0.1.47 and will be removed in 1.0. Use :meth:`~invoke` instead.
    print(get_text_length("Hello world!"))
    """
    # to invoke a tool, we need to use the invoke method.
    # print(get_text_length.invoke("Hello world!")) # this will give the correct output.
    tools = [get_text_length]
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    

    Begin!

    Question: {input}
    Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        # tools=[tool.name for tool in tools],
        tools=render_text_description(tools),
        tool_names=", ".join([tool.name for tool in tools]),
        # input="What is the length of the text 'Hello world!'?",
    )
    
    llm = OllamaLLM(
        model="llama3",
        temperature=0,
        stop=["\nObservation"],
    )
    # llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", openai_api_key=openai_api_key,verbose=True, stop=["\nObservation"]) #agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,)
    agent = {"input": lambda x: x["input"]} | prompt | llm | ReActSingleInputOutputParser()
    
    # agent_execution = agent.invoke({"input": "What is the length of 'Dog and Cat' in characters?"})
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke({"input": "How many characters are there in the word: Dog ?"})
    print(agent_step)

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        print(f"{observation=}")