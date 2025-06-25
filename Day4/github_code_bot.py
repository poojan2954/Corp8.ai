import os
import shutil
from git import Repo
from dotenv import load_dotenv
from colorama import Fore, Style, init

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize color output
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Supported file types for code analysis
SUPPORTED_EXTENSIONS = [
    "*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.c", "*.cs",
    "*.html", "*.css", "*.json", "*.xml", "*.php", "*.rb",
    "*.go", "*.rs", "*.swift", "*.kt", "*.scala", "*.sql",
    "*.sh", "*.ipynb"
]

# Instantiate the LLM
llm_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def download_repository(repo_url: str, target_dir="repo_clone"):
    """Clone the GitHub repository into a clean folder."""
    if os.path.exists(target_dir):
        print(Fore.YELLOW + "[INFO] Cleaning up previous clone...")
        shutil.rmtree(target_dir)

    try:
        print(Fore.CYAN + f"[INFO] Cloning repository: {repo_url}")
        Repo.clone_from(repo_url, target_dir)
        print(Fore.GREEN + "[SUCCESS] Repository cloned successfully.\n")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to clone repository: {e}")
        exit(1)

    return target_dir

def extract_documents_from_repo(directory: str):
    """Load source code documents from the cloned repository."""
    all_docs = []
    print(Fore.CYAN + "[INFO] Extracting documents...")
    for ext in SUPPORTED_EXTENSIONS:
        loader = DirectoryLoader(directory, glob=f"**/{ext}", loader_cls=TextLoader)
        all_docs.extend(loader.load())

    if not all_docs:
        print(Fore.RED + "[WARNING] No supported files found in the repository.")
        exit(1)

    print(Fore.GREEN + f"[SUCCESS] Loaded {len(all_docs)} documents.")
    return all_docs

def build_context_index(documents):
    """Convert documents into a retrievable FAISS index."""
    print(Fore.CYAN + "[INFO] Embedding documents...")
    embedder = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents, embedder)
    return vector_store.as_retriever()

def create_qa_bot(retriever):
    """Initialize the retrieval-based question-answer bot."""
    print(Fore.CYAN + "[INFO] Initializing chatbot...")
    chain = RetrievalQA.from_chain_type(
        llm=llm_model,
        retriever=retriever,
        return_source_documents=True
    )
    print(Fore.GREEN + "[READY] Chatbot is ready to answer your queries!\n")
    return chain

def main():
    print(Style.BRIGHT + Fore.MAGENTA + "\n\U0001F50D GitHub Repository QA Bot \U0001F50D\n")

    github_url = input("\U0001F4CE Enter GitHub repo URL: ").strip()
    repo_path = download_repository(github_url)
    docs = extract_documents_from_repo(repo_path)
    retriever = build_context_index(docs)
    bot = create_qa_bot(retriever)

    print(Fore.YELLOW + "\n\U0001F4AC Ask anything about the repository (type 'exit' to quit):\n")
    while True:
        question = input(Fore.BLUE + ">> ").strip()
        if question.lower() == "exit":
            print(Fore.CYAN + "\n\U0001F44B Exiting. Thank you!")
            break

        try:
            answer = bot.invoke(question)
            print(Fore.GREEN + "\n\U0001F9E0 Answer:\n" + answer['result'] + "\n")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to get response: {e}")

if __name__ == "__main__":
    main()
