from gen_engine_client import invoke_llm

# ANSI escape codes for colors
class Colors:
    PROMPT = '\033[96m'     # Cyan
    RESPONSE = '\033[92m'   # Green
    RESET = '\033[0m'       # Reset to default

if __name__ == "__main__":
    while True:
        prompt = input(f"\n{Colors.PROMPT}Enter your prompt (or type 'exit' to quit): {Colors.RESET}")
        if prompt.lower() == "exit":
            break
        result = invoke_llm(prompt)
        if result:
            print(f"\n{Colors.RESPONSE}Model Response:{Colors.RESET}")
            print(result.get("content", "No content found"))



