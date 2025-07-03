from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import requests
from dotenv import load_dotenv

#Load environment variables
load_dotenv()

# Initialize Gemini with API key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")  # This pulls from your .env file
)

# Prompt template
prompt = PromptTemplate.from_template(
    """You are an assistant that converts natural language questions into SQL queries for a table named 'users'.

Question: {question}
SQL Query:"""
)

sql_chain = LLMChain(prompt=prompt, llm=llm)

def clean_sql(sql):
    return sql.replace("```sql", "").replace("```", "").strip()


def ask_question(natural_language_question):
    sql_query = sql_chain.run({"question": natural_language_question})
    cleaned_sql = clean_sql(sql_query)  
    
    print("📝 Generated SQL:", cleaned_sql)

    response = requests.post(
        os.getenv("MCP_SERVER_URL"),
        json={"query": cleaned_sql}  
    )

    try:
        result = response.json()
        return result.get("result", result)
    except Exception as e:
        return {"error": f"Invalid response from server: {e}"}
