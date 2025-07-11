import asyncio
from tools import get_all_tools
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.memory import ChatMemoryBuffer

# Initialize LLM
llm = OpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=0.2,
    system_prompt="You are a helpful and concise assistant. Respond in 2–3 sentences only."
)

async def test_agent():
    tools = get_all_tools()

    memory = ChatMemoryBuffer.from_defaults()

    agent = FunctionAgent(
        tools=tools,
        llm=llm,
        memory=memory,
        verbose=True,
    )

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            # ✅ Use await to run asynchronously
            response = await agent.run(user_input)

            print(f"\n🧠 Agent: {response}")
        except KeyboardInterrupt:
            print("\n🛑 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(test_agent())