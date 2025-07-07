import random

def rank_top_candidates_with_index(index, documents, category: str, top_n: int, custom_question: str = None):
    from gen_engine_llm import GenerativeEngineLLM
    import streamlit as st

    category = category.upper().strip()
    filtered_docs = documents
    random.shuffle(filtered_docs)

    # filtered_docs = [doc for doc in documents if doc.metadata.get("category", "").upper().strip() == category]

    if not filtered_docs:
        st.warning(f"Category '{category}' not found in the provided documents.")
        return

    llm = GenerativeEngineLLM()
    query_engine = index.as_query_engine(llm=llm)

    candidates = []
    for doc in filtered_docs:
        default_query = (
            f"You are a hiring expert evaluating resumes for the category '{category}'.\n"
            f"Based on the following information, rate this candidate from 1 to 10 for a role in {category}. "
            f"Consider experience, skills, and relevance. Then provide a brief summary of their strengths.\n\n"
            f"Response format:\n"
            f"Score: <number>\nSummary: <summary>"
        )

        query = (custom_question + "\n\nResponse format:\nScore: <number>\nSummary: <summary>") if custom_question else default_query

        print("Using query:", query)

        response = query_engine.query(query)
        text = str(response).strip()

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

        candidates.append({
            "id": doc.metadata["id"],
            "score": score,
            "summary": summary
        })

    top_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:top_n]

    for i, candidate in enumerate(top_candidates, 1):
        print(f"\nTop {i} Candidate")
        print(f"ID: {candidate['id']}")
        print(f"Score: {candidate['score']}")
        print(f"Summary: {candidate['summary']}")
        
        # Streamlit display
        st.markdown(f"### 🥇 Top {i} Candidate") 
        st.markdown(f"**ID:** {candidate['id']}")
        st.markdown(f"**Score:** {candidate['score']}")
        st.markdown(f"**Summary:** {candidate['summary']}")

