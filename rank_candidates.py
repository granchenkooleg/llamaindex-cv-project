import pandas as pd
from gen_engine_llm import GenerativeEngineLLM

def rate_candidate(llm, resume_text, category):
    prompt = (
        f"You are a hiring expert evaluating resumes for the category '{category}'.\n"
        f"Based on the following resume, rate this candidate from 1 to 10 for a role in {category}. "
        f"Consider experience, skills, and relevance. Then provide a brief summary of their strengths.\n\n"
        f"Resume:\n{resume_text[:2000]}\n\n"
        f"Response format:\n"
        f"Score: <number>\nSummary: <summary>"
    )
    response = llm.complete(prompt)
    text = response.text.strip()

    score = 0
    summary = ""
    for line in text.splitlines():
        if line.lower().startswith("score:"):
            try:
                score = int(line.split(":")[1].strip())
            except:
                score = 0
        elif line.lower().startswith("summary:"):
            summary = line.split(":", 1)[1].strip()

    return score, summary

def rank_top_candidates(csv_path: str, category: str, top_n: int, sample_size: int = 5):
    df = pd.read_csv(csv_path)

    # Normalize category column and input
    df["Category"] = df["Category"].str.upper().str.strip()
    category = category.upper().strip()

    # Validate category
    if category not in df["Category"].unique():
        print(f"Category '{category}' not found. Available categories: {df['Category'].unique()}")
        return

    # Filter and sample
    filtered_df = df[df["Category"] == category]
    sample_size = min(sample_size, len(filtered_df))
    sampled_df = filtered_df.sample(n=sample_size, random_state=42)

    llm = GenerativeEngineLLM()
    candidates = []

    for _, row in sampled_df.iterrows():
        score, summary = rate_candidate(llm, row["Resume_str"], category)
        candidates.append({
            "id": row["ID"],
            "score": score,
            "summary": summary
        })

    top_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:top_n]

    for i, candidate in enumerate(top_candidates, 1):
        print(f"\nTop {i} Candidate")
        print(f"ID: {candidate['id']}")
        print(f"Score: {candidate['score']}")
        print(f"Summary: {candidate['summary']}")