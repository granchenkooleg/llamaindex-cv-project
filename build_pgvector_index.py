from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from embedding_model import get_openai_embedding_model
from dotenv import load_dotenv
import os

load_dotenv()
print("✅ OPENAI_API_KEY loaded:", os.getenv("OPENAI_API_KEY"))

def build_pgvector_index(documents):
    parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = parser.get_nodes_from_documents(documents)

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
    index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embed_model)

    print(f"✅ Indexed {len(nodes)} chunks (nodes)")
    return index