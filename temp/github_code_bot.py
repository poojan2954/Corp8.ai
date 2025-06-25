from git import Repo 
import os 
from langchain_community.document_loaders import DirectoryLoader, TextLoader 
from langchain_community.vectorstores import FAISS 
from langchain.chains import RetrievalQA 
from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_huggingface import HuggingFaceEmbeddings 

 
load_dotenv() 
 
model= ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
 
code_extensions = [ 
    "*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.c", "*.cs", "*.html", "*.css", 
    "*.json", "*.xml", "*.php", "*.rb", "*.go", "*.rs", "*.swift", "*.kt", "*.scala", 
    "*.sql", "*.sh", "*.ipynb"] 
 
def clone_repo(github_url, clone_path="cloned_repo"): 
    if os.path.exists(clone_path): 
        print("Repository already cloned.") 
    else: 
        print(f"Cloning from {github_url}...") 
        Repo.clone_from(github_url, clone_path) 
    return clone_path 
 
def load_code_documents(repo_path): 
    documents = [] 
    for ext in code_extensions: 
        loader = DirectoryLoader(repo_path, glob=f"**/{ext}", loader_cls=TextLoader) 
        documents.extend(loader.load()) 
    return documents 
 
def create_retriever(documents): 
    embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2") 
    db = FAISS.from_documents(documents, embeddings) 
    retriever = db.as_retriever() 
    return retriever 
 
def create_chatbot(retriever): 
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2) 
    qa_chain = RetrievalQA.from_chain_type( 
        llm=llm, 
        retriever=retriever, 
        return_source_documents=True 
    ) 
    return qa_chain 
 
if __name__ == "__main__": 
    github_url = input("Enter the repository link: ") 
    repo_path = clone_repo(github_url) 
    documents = load_code_documents(repo_path) 
    retriever = create_retriever(documents) 
    qa_bot = create_chatbot(retriever) 
 
    print("\nAsk me anything about the repo!") 
    while True: 
        query = input(">> ") 
        if query.lower() == 'exit': 
            break 
        response = qa_bot.invoke(query) 
        print(f"\n{response['result']}\n") 