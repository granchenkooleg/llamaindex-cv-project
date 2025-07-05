from llama_index.core.llms import LLM, CompletionResponse, LLMMetadata
from gen_engine_client import invoke_llm

class GenerativeEngineLLM(LLM):
    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        response = invoke_llm(prompt)
        if not response:
            return CompletionResponse(text="❌ No response from Capgemini LLM")
        return CompletionResponse(text=response.get("content", ""))


    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            model_name="capgemini-nova-lite",
            is_chat_model=False,
            is_function_calling_model=False,
        )

    def chat(self, messages, **kwargs):
        raise NotImplementedError("Chat not implemented")

    def stream_chat(self, messages, **kwargs):
        raise NotImplementedError("Stream chat not implemented")

    def stream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Stream complete not implemented")

    def acomplete(self, prompt: str, **kwargs):
        raise NotImplementedError("Async complete not implemented")

    def achat(self, messages, **kwargs):
        raise NotImplementedError("Async chat not implemented")

    def astream_chat(self, messages, **kwargs):
        raise NotImplementedError("Async stream chat not implemented")

    def astream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Async stream complete not implemented")
