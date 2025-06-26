import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
prompt = PromptTemplate(
    template="Generate interesting facts about {topic}",
    input_variables=["topic"]
)
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # or gemini-pro or gemini-1.5-pro
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
parser = StrOutputParser()
chain = prompt | model | parser
result = chain.invoke({"topic": "cricket"})
print(result)
