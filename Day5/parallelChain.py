import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
prompt1 = PromptTemplate(
    template="Tell me an interesting fact about {topic}.",
    input_variables=["topic"]
)
prompt2 = PromptTemplate(
    template="Write a catchy blog title about {topic}.",
    input_variables=["topic"]
)
prompt3 = PromptTemplate(
    template="List 3 key points to include in an article about {topic}.",
    input_variables=["topic"]
)
parser = StrOutputParser()
parallel_chain = RunnableParallel({
    "fact": prompt1 | model | parser,
    "title": prompt2 | model | parser,
    "points": prompt3 | model | parser
})
result = parallel_chain.invoke({"topic": "football"})
print(result)
