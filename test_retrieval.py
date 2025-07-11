from tools import create_resume_retrieval_tool

# def format_query_result(summary: str, source_nodes: list) -> str:
#     formatted_results = []
#     for node in source_nodes:
#         metadata = node.metadata if hasattr(node, "metadata") else {}
#         doc_id = metadata.get("id", "No ID")
#         category = metadata.get("category", "No Category")
#         content_snippet = node.text[:200] if hasattr(node, "text") else str(node)[:200]
#         formatted_results.append(
#             f"🧾 Candidate ID: {doc_id} | Category: {category}\n📝 Content: {content_snippet}\n{'-'*80}"
#         )
#     return f"✅ Query Result:\n{summary}\n\n" + "\n".join(formatted_results)

# This script runs queries against the resume retrieval tool and formats the results for display.
def run_queries():
    tool = create_resume_retrieval_tool()

    queries = [
        "List candidates with cybersecurity experience.",
        "Summarize the educational background of candidates.",
        "Find candidates who managed teams.",
    ]

    for query in queries:
        print(f"\n📝 Running query: {query}")
        response = tool.query_engine.query(query)

        summary = str(response)  # Extract the summary string
        source_nodes = response.source_nodes  # These should be nodes with metadata

        formatted_response = format_query_result(summary, source_nodes)
        print(formatted_response)

if __name__ == "__main__":
    run_queries()