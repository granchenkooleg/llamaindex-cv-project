import streamlit as st
import pandas as pd

# Configuration
CSV_PATH = "archive/Resume/Resume.csv"
CATEGORY = "INFORMATION-TECHNOLOGY"
TOP_N = 5
SAMPLE_SIZE = 5

# Mocked LLM scoring function (for testing)
def mock_rate_candidate(resume_text, category):
    score = 7  # fixed score for testing
    summary = "This is a mock summary for testing purposes."
    return score, summary

# Load and rank candidates
@st.cache_data(show_spinner=True)
def get_ranked_candidates():
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return []

    df["Category"] = df["Category"].str.upper().str.strip()
    category = CATEGORY.upper().strip()
    filtered_df = df[df["Category"] == category]

    if filtered_df.empty:
        return []

    sample_size = max(SAMPLE_SIZE, TOP_N)
    sample_size = min(sample_size, len(filtered_df))
    sampled_df = filtered_df.sample(n=sample_size, random_state=42)

    candidates = []
    for _, row in sampled_df.iterrows():
        score, summary = mock_rate_candidate(row["Resume_str"], category)
        candidates.append({
            "id": row["ID"],
            "score": score,
            "summary": summary,
            "resume": row["Resume_str"]
        })

    top_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:TOP_N]
    return top_candidates

# Streamlit UI
st.title("Top Ranked Candidates")
st.markdown("### Category: Information Technology")

with st.spinner("Ranking candidates..."):
    candidates = get_ranked_candidates()

if not candidates:
    st.warning("No candidates found or an error occurred.")
else:
    candidate_ids = [f"Candidate {i+1} (ID: {c['id']})" for i, c in enumerate(candidates)]
    selected = st.selectbox("Select a candidate to view details:", candidate_ids)

    selected_index = candidate_ids.index(selected)
    candidate = candidates[selected_index]

    st.subheader(f"Candidate ID: {candidate['id']}")
    st.markdown(f"**Score:** {candidate['score']}")
    st.markdown(f"**Summary:** {candidate['summary']}")
    with st.expander("📄 Full Resume"):
        st.text(candidate["resume"])

    # Debug output
    st.markdown("---")
    st.markdown("### Debug Info")
    st.json(candidate)
    st.markdown("This is a mock implementation for testing purposes. In a real application, replace the `mock_rate_candidate` function with the actual LLM scoring logic.") 
# Note: This code is designed to run in a Streamlit environment.
# To run it execute `streamlit run app.py` in your terminal.
# Ensure you have the required libraries installed: `streamlit`, `pandas`.
# The CSV file should be present at the specified path for the code to work correctly
# and display the candidates in a web interface.