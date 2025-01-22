from mistralai import Mistral

class MistralWrapper:
    def __init__(self, api_key):
        """
        Initialize the Mistral client with the provided API key.
        """
        self.client = Mistral(api_key=api_key)
        print("Mistral client initialized successfully.")

    def generate_completion(self, prompt, model="codestral-latest", temperature=0, top_p=1):
        """
        Generate a completion using the Mistral API.
        Args:
            prompt (str): The user-provided code or text prompt.
            model (str): The model to use for completion (default: "codestral-latest").
            temperature (float): Sampling temperature for randomness.
            top_p (float): Top-p sampling for response diversity.

        Returns:
            str: The fixed output as plain text.
        """
        # System prompt for context
        system_prompt = (
            "You are a professional Python developer. "
            "Fix the provided code and return the fixed output only as text value!"
            "If no mistakes in provided code, then output initial code."
            "It is important that your output is plain text, not code."
            "Limit your answer to conditions above."
        )
        # Concatenate system prompt and user prompt
        full_prompt = f"{system_prompt}{prompt}"
        
        # Send the prompt to the Mistral API
        response = self.client.fim.complete(
            model=model,
            prompt=full_prompt,
            temperature=temperature,
            top_p=top_p,
        )
        
        # Return the content of the response
        return response.choices[0].message.content.strip()
