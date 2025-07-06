from load_data import load_resumes
from build_index import build_index
from summarize import summarize_candidates
from rank_candidates import rank_top_candidates


def main():
    documents = load_resumes(10)
    index = build_index(documents)
    # summarize_candidates(index, documents)
    rank_top_candidates("archive/Resume/Resume.csv", category="INFORMATION-TECHNOLOGY", top_n=3)

if __name__ == "__main__":
    main()