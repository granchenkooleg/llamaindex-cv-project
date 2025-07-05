import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.readers.web import SimpleWebPageReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from gen_engine_llm import GenerativeEngineLLM
import requests
import certifi

# Force Python to use certifi's certificate bundle
os.environ['SSL_CERT_FILE'] = certifi.where()


# Patch requests to always use certifi's CA bundle
original_get = requests.get
def patched_get(*args, **kwargs):
    kwargs['verify'] = certifi.where()
    return original_get(*args, **kwargs)
requests.get = patched_get

def main(url: str) -> None:
    print("📄 Loading documents...")
    documents = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])

    print("🧠 Initializing LLM and embedding model...")
    llm = GenerativeEngineLLM()
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    Settings.llm = llm
    Settings.embed_model = embed_model

    print("📊 Building index...")
    index = VectorStoreIndex.from_documents(documents)

    print("🔍 Querying index...")
    query_engine = index.as_query_engine()
    response = query_engine.query("What is LlamaIndex?")
    
    print("✅ Response received:")
    print(response)

# ✅ This block runs the script
if __name__ == '__main__':
    load_dotenv()
    print('Hello World LlamaIndexCourse')
    print(f"KEY is: {os.environ.get('API_KEY', 'No key found')}\n")
    print("******")
    try:
        main(url='https://example.com')
    except Exception as e:
        print(f"❌ Exception occurred: {e}")


