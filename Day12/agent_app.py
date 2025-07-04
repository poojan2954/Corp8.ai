import os
import requests
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load .env variables
load_dotenv()
MCP_URL = os.getenv("MCP_SERVER_URL")

# Define the tool
@tool
def search_papers(query: str) -> str:
    """Searches academic papers using a query string."""
    response = requests.get(f"{MCP_URL}/papers/", params={"query": query})
    papers = response.json()
    return "\n\n".join([f"Title: {p['title']}\nURL: {p['url']}" for p in papers])

# Gemini model setup
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

# ✅ Proper ReAct PromptTemplate
prompt_template = PromptTemplate.from_template(
    """You are a helpful academic assistant. Use the following tools to help you answer questions.

{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
{agent_scratchpad}"""
)

# Create the ReAct agent
agent = create_react_agent(
    llm=llm,
    tools=[search_papers],
    prompt=prompt_template
)

# AgentExecutor for LangChain
agent_executor = AgentExecutor(agent=agent, tools=[search_papers], verbose=True)

# Final callable function
def ask(question: str) -> str:
    return agent_executor.invoke({"input": question})["output"]
