# test_retrieval.py
from tools import create_resume_retrieval_tool

def run_queries():
    tool = create_resume_retrieval_tool()

    if tool is None:
        print("❌ Failed to create tool!")
        return

    queries = [
        "List candidates with cybersecurity experience.",
        "Summarize the educational background of candidates.",
        "Find candidates who managed teams.",
    ]

    for query in queries:
        print(f"\n📝 Running query: {query}")
        response = tool.query_engine.query(query)

        print("✅ Query Result:")
        print(response)

if __name__ == "__main__":
    run_queries()