from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import QueryEngineTool
from embedding_model import get_openai_embedding_model
from dotenv import load_dotenv
import os

load_dotenv()

def create_resume_retrieval_tool():
    print("⏳ Creating the retrieval tool...")

    embed_model = get_openai_embedding_model()

    vector_store = PGVectorStore.from_params(
        database=os.getenv("PG_DATABASE"),
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT")),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        table_name="resumes"
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, embed_model=embed_model)

    retriever = index.as_retriever(similarity_top_k=3)

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=OpenAI(),
        response_mode="compact",             # <-- Clear summarization
        return_source=True                   # <-- Important: enables access to source documents
    )

    tool = QueryEngineTool.from_defaults(
        name="resume_retrieval_tool",
        description="Retrieve candidate information from resumes based on user queries.",
        query_engine=query_engine,
    )

    print("✅ Retrieval tool created successfully!")
    return tool