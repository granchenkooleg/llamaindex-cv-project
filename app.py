
import streamlit as st
from summarize import summarize_candidates
from main import load_resumes, build_index

# Configuration
SAMPLE_SIZE = 5

# Load resumes and build index
@st.cache_resource(show_spinner=True)
def load_and_summarize():
    documents = load_resumes(SAMPLE_SIZE)
    index = build_index(documents)
    return documents, index

# Streamlit UI
st.set_page_config(page_title="Candidate Viewer", layout="wide")
st.title("🧑‍💼 Candidate Profiles")
st.markdown("Browse through the list of candidates and view their resume and summary.")

documents, index = load_and_summarize()

# Sidebar: Candidate selector
candidate_ids = [f"Candidate {i+1} (ID: {doc.metadata['id']})" for i, doc in enumerate(documents)]
selected = st.sidebar.selectbox("Select a candidate:", candidate_ids)
selected_index = candidate_ids.index(selected)
selected_doc = documents[selected_index]

# Main content
st.subheader(f"Candidate ID: {selected_doc.metadata['id']}")
st.markdown(f"**Category:** {selected_doc.metadata['category']}")

with st.expander("📄 Full Resume"):
    st.text(selected_doc.text)

# Generate and display summary
st.markdown("### 📝 Summary")
summary = summarize_candidates(index, [selected_doc])[0]
st.markdown(summary)





# import streamlit as st
# import pandas as pd
# from rank_candidates import rate_candidate
# from gen_engine_llm import GenerativeEngineLLM
# from main import load_resumes, build_index, summarize_candidates

# # Configuration
# CSV_PATH = "archive/Resume/Resume.csv"
# CATEGORY = "INFORMATION-TECHNOLOGY"
# TOP_N = 5
# SAMPLE_SIZE = 5

# @st.cache_data(show_spinner=True)
# def get_ranked_candidates():
#     df = pd.read_csv(CSV_PATH)
#     df["Category"] = df["Category"].str.upper().str.strip()
#     category = CATEGORY.upper().strip()
#     filtered_df = df[df["Category"] == category]

#     if filtered_df.empty:
#         return []

#     sample_size = max(SAMPLE_SIZE, TOP_N)
#     sample_size = min(sample_size, len(filtered_df))
#     sampled_df = filtered_df.sample(n=sample_size, random_state=42)

#     llm = GenerativeEngineLLM()
#     candidates = []
#     for _, row in sampled_df.iterrows():
#         score, summary = rate_candidate(llm, row["Resume_str"], category)
#         candidates.append({
#             "id": row["ID"],
#             "score": score,
#             "summary": summary,
#             "resume": row["Resume_str"]
#         })

#     top_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:TOP_N]
#     return top_candidates

# @st.cache_data(show_spinner=True)
# def get_summaries():
#     documents = load_resumes(SAMPLE_SIZE)
#     index = build_index(documents)
#     return summarize_candidates(index, documents)

# # Streamlit UI
# st.title("Top Ranked Candidates")
# st.markdown("### Category: Information Technology")

# with st.spinner("Ranking candidates..."):
#     candidates = get_ranked_candidates()

# with st.spinner("Generating summaries..."):
#     summaries = get_summaries()

# if not candidates:
#     st.warning("No candidates found or an error occurred.")
# else:
#     candidate_ids = [f"Candidate {i+1} (ID: {c['id']})" for i, c in enumerate(candidates)]
#     selected = st.selectbox("Select a candidate to view details:", candidate_ids)

#     selected_index = candidate_ids.index(selected)
#     candidate = candidates[selected_index]

#     st.subheader(f"Candidate ID: {candidate['id']}")
#     st.markdown(f"**Score:** {candidate['score']}")
#     st.markdown(f"**Summary:** {candidate['summary']}")

#     if summaries and selected_index < len(summaries):
#         st.markdown(f"**LLM Summary:** {summaries[selected_index]}")

#     with st.expander("📄 Full Resume"):
#         st.text(candidate["resume"])






# import streamlit as st
# import pandas as pd
# from rank_candidates import rank_top_candidates, rate_candidate
# from gen_engine_llm import GenerativeEngineLLM

# # Configuration
# CSV_PATH = "archive/Resume/Resume.csv"
# CATEGORY = "INFORMATION-TECHNOLOGY"
# TOP_N = 5
# SAMPLE_SIZE = 5

# # Run ranking logic
# @st.cache_data(show_spinner=True)
# def get_ranked_candidates():
#     df = pd.read_csv(CSV_PATH)
#     df["Category"] = df["Category"].str.upper().str.strip()
#     category = CATEGORY.upper().strip()
#     filtered_df = df[df["Category"] == category]

#     if filtered_df.empty:
#         return []

#     sample_size = max(SAMPLE_SIZE, TOP_N)
#     sample_size = min(sample_size, len(filtered_df))
#     sampled_df = filtered_df.sample(n=sample_size, random_state=42)

#     llm = GenerativeEngineLLM()
#     candidates = []

#     for _, row in sampled_df.iterrows():
#         score, summary = rate_candidate(llm, row["Resume_str"], category)
#         candidates.append({
#             "id": row["ID"],
#             "score": score,
#             "summary": summary,
#             "resume": row["Resume_str"]
#         })

#     top_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:TOP_N]
#     return top_candidates

# # Streamlit UI
# st.title("Top Ranked Candidates")
# st.markdown("### Category: Information Technology")

# candidates = get_ranked_candidates()

# if not candidates:
#     st.warning("No candidates found for the selected category.")
# else:
#     candidate_ids = [f"Candidate {i+1} (ID: {c['id']})" for i, c in enumerate(candidates)]
#     selected = st.selectbox("Select a candidate to view details:", candidate_ids)

#     selected_index = candidate_ids.index(selected)
#     candidate = candidates[selected_index]

#     st.subheader(f"Candidate ID: {candidate['id']}")
#     st.markdown(f"**Score:** {candidate['score']}")
#     st.markdown(f"**Summary:** {candidate['summary']}")
#     with st.expander("📄 Full Resume"):
#         st.text(candidate["resume"])
