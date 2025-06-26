import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
prompt1 = PromptTemplate(
    template="Generate interesting facts about {topic}",
    input_variables=["topic"]
)
prompt2 = PromptTemplate(
    template="Generate interesting facts about {topic}",
    input_variables=["topic"]
)
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
parser = StrOutputParser()
chain = prompt1 | model | parser | prompt2 | model | parser
result = chain.invoke({"topic": "football"})
print(result)
