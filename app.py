
# import streamlit as st
# from summarize import summarize_candidates
# from main import load_resumes, build_index

# # Configuration
# SAMPLE_SIZE = 5

# # Load resumes and build index
# @st.cache_resource(show_spinner=True)
# def load_and_summarize():
#     documents = load_resumes(SAMPLE_SIZE)
#     index = build_index(documents)
#     return documents, index

# # Streamlit UI
# st.set_page_config(page_title="Candidate Viewer", layout="wide")
# st.title("🧑‍💼 Candidate Profiles")
# st.markdown("Browse through the list of candidates and view their resume and summary.")

# documents, index = load_and_summarize()

# # Sidebar: Candidate selector
# candidate_ids = [f"Candidate {i+1} (ID: {doc.metadata['id']})" for i, doc in enumerate(documents)]
# selected = st.sidebar.selectbox("Select a candidate:", candidate_ids)
# selected_index = candidate_ids.index(selected)
# selected_doc = documents[selected_index]

# # Main content
# st.subheader(f"Candidate ID: {selected_doc.metadata['id']}")
# st.markdown(f"**Category:** {selected_doc.metadata['category']}")

# with st.expander("📄 Full Resume"):
#     st.text(selected_doc.text)

# # Generate and display summary
# st.markdown("### 📝 Summary")
# summary = summarize_candidates(index, [selected_doc])[0]
# st.markdown(summary)





import streamlit as st
from main import load_resumes, build_index
from rank_candidates import rank_top_candidates_with_index

# Configuration
SAMPLE_SIZE = 5

# Load resumes and build index
@st.cache_resource(show_spinner=True)
def load_and_index():
    documents = load_resumes(SAMPLE_SIZE)
    index = build_index(documents)
    return documents, index

# Streamlit UI
st.set_page_config(page_title="Candidate Ranking", layout="wide")
st.title("🔍 Candidate Ranking Tool")

documents, index = load_and_index()

# Sidebar inputs
st.sidebar.header("Ranking Criteria")
category = st.sidebar.text_input("Enter job category (e.g., Data Science):", "")
top_n = st.sidebar.slider("Number of top candidates to show:", 1, 10, 3)
custom_question = st.sidebar.text_area(
    "Optional: Custom evaluation question (leave blank to use default):",
    height=150
)

# Button to trigger ranking
if st.sidebar.button("Rank Candidates"):
    if not category:
        st.warning("Please enter a job category.")
    else:
        st.subheader(f"Top {top_n} Candidates for Category: {category}")
        with st.spinner("Evaluating candidates..."):
            rank_top_candidates_with_index(index, documents, category, top_n, custom_question)
