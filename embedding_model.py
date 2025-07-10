from llama_index.embeddings.openai import OpenAIEmbedding

def get_openai_embedding_model():
    return OpenAIEmbedding(model="text-embedding-3-small")