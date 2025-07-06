from gen_engine_llm import GenerativeEngineLLM

def summarize_candidates(index, documents):
    llm = GenerativeEngineLLM()
    query_engine = index.as_query_engine(llm=llm)

    for doc in documents:
        print(f"\n🧑 Candidate ID: {doc.metadata['id']}")
        print(f"📂 Category: {doc.metadata['category']}")
        query = f"Summarize the professional experience and key skills of this candidate:\n\n{doc.text[:1000]}"
        response = query_engine.query(query)
        print("📝 Summary:")
        print(response)
