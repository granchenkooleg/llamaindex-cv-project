import pandas as pd
from llama_index.core import Document

def load_resumes(sample_size=30):
    # Adjust the path to where you placed Resume.csv
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




# import kagglehub
# import pandas as pd
# from llama_index.core import Document

# def load_resumes(sample_size=30):
#     file_path = "UpdatedResumeData.csv"
#     df = kagglehub.load_dataset(
#         kagglehub.KaggleDatasetAdapter.PANDAS,
#         "snehaanbhawal/resume-dataset",
#         file_path,
#     )

#     sampled_df = df.sample(n=sample_size, random_state=42)

#     documents = []
#     for _, row in sampled_df.iterrows():
#         metadata = {
#             "id": row["ID"],
#             "category": row["Category"]
#         }
#         documents.append(Document(text=row["Resume_str"], metadata=metadata))

#     return documents