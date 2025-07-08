# vectorstore.py
import json
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

def build_vectorstore():
    with open("recipes.json", "r") as f:
        data = json.load(f)

    docs = [Document(page_content=item["ingredients"], metadata=item) for item in data]

    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(docs, embedding)
    db.save_local("recipes_index")

if __name__ == "__main__":
    build_vectorstore()
