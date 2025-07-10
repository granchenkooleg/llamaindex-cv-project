from tools import create_resume_retrieval_tool, query_tool

def test_query():
    try:
        print("⏳ Creating the retrieval tool...")
        tool = create_resume_retrieval_tool()
        print("🔍 Tool created successfully!")

        query = "List candidates with cybersecurity experience."
        print(f"📝 Running query: {query}")
        
        response = query_tool(tool, query)
        
        if response:
            print("✅ Query Result:")
            print(response)
        else:
            print("❌ No response received from the tool.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_query()