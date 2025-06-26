import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
parser = StrOutputParser()
sports_prompt = PromptTemplate(
    template="Tell me an amazing sports fact about {topic}.",
    input_variables=["topic"]
)

tech_prompt = PromptTemplate(
    template="Tell me an amazing tech fact about {topic}.",
    input_variables=["topic"]
)
topic = "cricket"  # Try changing to "AI", "robotics", "football", etc.
if "sport" in topic.lower() or "cricket" in topic.lower() or "football" in topic.lower():
    chain = sports_prompt | model | parser
else:
    chain = tech_prompt | model | parser
result = chain.invoke({"topic": topic})
print("🤖 Result:", result)
