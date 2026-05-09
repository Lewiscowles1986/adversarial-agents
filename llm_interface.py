from typing import Protocol, runtime_checkable

@runtime_checkable
class LLMInterface(Protocol):
    cli_type: str

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates a response from the LLM.
        
        Args:
            system_prompt: The instructions for the AI.
            user_prompt: The user's input/request.
            
        Returns:
            The generated text response.
        """
        ...
