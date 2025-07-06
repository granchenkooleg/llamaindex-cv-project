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

def rank_top_candidates(csv_path, category="Information-Technology", top_n=3):
    df = pd.read_csv(csv_path)
    filtered_df = df[df["Category"] == category].sample(n=10, random_state=42)

    llm = GenerativeEngineLLM()
    candidates = []

    for _, row in filtered_df.iterrows():
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