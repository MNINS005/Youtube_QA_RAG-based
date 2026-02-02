import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

embeddings = SentenceTransformerEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
