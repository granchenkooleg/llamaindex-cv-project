import os
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.vector_stores.postgres import PGVectorStore
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from gen_engine_llm import GenerativeEngineLLM
from embedding_model import get_openai_embedding_model

load_dotenv()

def create_resume_retrieval_tool():
    db_params = {
        "database": os.getenv("PG_DATABASE"),
        "host": os.getenv("PG_HOST", "localhost"),
        "password": os.getenv("PG_PASSWORD"),
        "port": int(os.getenv("PG_PORT", 5432)),
        "user": os.getenv("PG_USER"),
        "table_name": "resumes"
    }

    embed_model = get_openai_embedding_model()
    # embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = PGVectorStore.from_params(**db_params)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
    query_engine = index.as_query_engine(llm=llm)
    # query_engine = index.as_query_engine(llm=GenerativeEngineLLM())

    return QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="ResumeRetriever",
        description="Retrieves and summarizes candidate information from the resume database."
    )

def query_tool(tool, query):
    return tool.query_engine.query(query)