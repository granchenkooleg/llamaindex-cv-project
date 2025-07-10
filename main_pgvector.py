from load_data import load_resumes
from build_pgvector_index import build_pgvector_index
from summarize import summarize_candidates

def main():
    sample_size = 5
    documents = load_resumes(sample_size)
    index = build_pgvector_index(documents)
    summarize_candidates(index, documents)

if __name__ == "__main__":
    main()
