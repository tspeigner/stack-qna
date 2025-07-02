from chromadb import Client
from chromadb.config import Settings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

chroma_client = Client(Settings(persist_directory=CHROMA_PATH))

# Utility to get or create the collection for Q&A embeddings
COLLECTION_NAME = "stackoverflow_qa"

def get_qa_collection():
    return chroma_client.get_or_create_collection(COLLECTION_NAME)
