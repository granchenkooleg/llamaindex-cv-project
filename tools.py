from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import FunctionTool  # <-- make sure this is here and before using it!
from llama_index.core.prompts import PromptTemplate
from llama_index.tools.wikipedia import WikipediaToolSpec
from dotenv import load_dotenv
import os

from embedding_model import get_openai_embedding_model

load_dotenv()

# Resume Retrieval Tool
# This tool retrieves candidate information from resumes stored in a PostgreSQL database.
# It uses a vector store to index the resumes and allows querying based on user input.
def resume_query_function(input: str) -> str:
    print("📄 Resume Retrieval Tool invoked")
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
        response_mode="compact",
        return_source=True
    )

    return query_engine.query(input).response

resume_qa_tool = FunctionTool.from_defaults(
    fn=resume_query_function,
    name="resume_qa_tool",
    description="Query candidate resume database for specific skills or experience.",
)


# General Knowledge Tool
llm = OpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=0.2,
    system_prompt="You are a concise assistant. Always respond with 2–3 sentences maximum."
)

def general_knowledge_tool(query: str) -> str:
    print("🌐 General Knowledge Tool invoked")
    return llm.complete(query).text

general_qa_tool = FunctionTool.from_defaults(
    fn=general_knowledge_tool,
    name="general_knowledge_tool",
    description="Answer general questions not related to resumes or candidate data.",
)


# Wikipedia Tool
def wiki_query_function(query: str) -> str:
    print("🌍 Wikipedia Tool invoked")
    return wiki_tools[0].query(query).response  # ← this will still work, but only if manually managed

wiki_qa_tool = FunctionTool.from_defaults(
    fn=wiki_query_function,
    name="wiki_qa_tool",
    description="Answer general knowledge questions using Wikipedia data."
)

# Function to get all tools
def get_all_tools():
    return [resume_qa_tool, general_qa_tool, wiki_qa_tool]