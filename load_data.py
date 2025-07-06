import pandas as pd
from llama_index.core import Document

# As we have certificate issues with the Kaggle API, we will load the dataset directly from a CSV file.
def load_resumes(sample_size=30):
    # The path to Resume.csv
    df = pd.read_csv("archive/Resume/Resume.csv")

    sampled_df = df.sample(n=sample_size, random_state=42)

    documents = []
    for _, row in sampled_df.iterrows():
        metadata = {
            "id": row["ID"],
            "category": row["Category"]
        }
        documents.append(Document(text=row["Resume_str"], metadata=metadata))

    return documents