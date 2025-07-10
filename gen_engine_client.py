import os
import requests
import json
import uuid
from dotenv import load_dotenv
load_dotenv()


# API configuration
API_URL = "https://api.generative.engine.capgemini.com/v2/llm/invoke"
API_KEY = os.getenv("CAPGEMINI_API_KEY")


def invoke_llm(prompt, temperature=0.6, max_tokens=512):
    import os
    import uuid
    import json
    import requests

    session_id = str(uuid.uuid4())

    payload = {
        "action": "run",
        "modelInterface": "langchain",
        "data": {
            "mode": "chain",
            "text": prompt,
            "files": [],
            "modelName": "amazon.nova-lite-v1:0",
            "provider": "bedrock",
            "sessionId": session_id,
            "modelKwargs": {
                "maxTokens": max_tokens,
                "temperature": temperature,
                "streaming": False,
                "topP": 0.9
            }
        }
    }

    headers = {
        "x-api-key": os.getenv("API_KEY"),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        print("📡 Sending request to Capgemini LLM...")
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("✅ Capgemini LLM response received")
            return response.json()
        else:
            print(f"❌ Capgemini API error: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Exception during LLM call: {str(e)}")
        return None
