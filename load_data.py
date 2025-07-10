import os
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
from llama_index.core import Document
from embedding_model import get_openai_embedding_model

# ✅ Load environment variables
load_dotenv()
print("✅ OPENAI_API_KEY loaded:", os.getenv("OPENAI_API_KEY"))

# ✅ Initialize embedding model
embed_model = get_openai_embedding_model()

# ✅ Connect to PostgreSQL using env vars
conn = psycopg2.connect(
    dbname=os.getenv("PG_DATABASE", "resume_db"),
    user=os.getenv("PG_USER", "resume_admin"),
    password=os.getenv("PG_PASSWORD", "securepass123"),
    host=os.getenv("PG_HOST", "localhost"),
    port=os.getenv("PG_PORT", "5432")
)
cur = conn.cursor()

def load_resumes(sample_size=5):
    # ✅ Load the resumes dataset from the CSV
    df = pd.read_csv("archive/Resume/Resume.csv")

    # ✅ Sample data
    sampled_df = df.sample(n=sample_size, random_state=42)

    documents = []
    for _, row in sampled_df.iterrows():
        metadata = {
            "id": row["ID"],
            "category": row["Category"]
        }
        resume_text = row["Resume_str"]

        # ✅ Generate embedding (string in → vector out)
        embedding = embed_model.get_text_embedding(resume_text)

        # ✅ Ensure it's a list of floats (to be safe)
        embedding = list(map(float, embedding))

        # ✅ Append Document
        documents.append(Document(text=resume_text, metadata=metadata, embedding=embedding))

    return documents

# ✅ Load and insert documents
documents = load_resumes()

for doc in documents:
    query = """
    INSERT INTO resumes (doc_id, content, metadata, embedding)
    VALUES (%s, %s, %s, %s)
    """
    values = (doc.metadata["id"], doc.text, Json(doc.metadata), doc.embedding)
    cur.execute(query, values)

# ✅ Finalize
conn.commit()
cur.close()
conn.close()

print("✅ Resumes ingested successfully!")