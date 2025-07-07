from load_data import load_resumes
from build_index import build_index
from summarize import summarize_candidates
from rank_candidates import rank_top_candidates_with_index


def main():
    sample_size = 3
    top_n = 3

    # Ensure sample_size is at least top_n
    sample_size = max(sample_size, top_n)

    documents = load_resumes(sample_size)
    index = build_index(documents)
    # summarize_candidates(index, documents)
    rank_top_candidates_with_index(index, documents, category="INFORMATION-TECHNOLOGY", top_n=top_n)

if __name__ == "__main__":
    main()
    print("Ranking completed successfully.")
    print("To view the candidates in a web interface, run 'streamlit run app.py' in the terminal.") 