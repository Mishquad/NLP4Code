import os
from llm_wrapper import MistralWrapper
import json

def submit_prompts(api_key, input_directory, output_directory):
    mistral_wrapper = MistralWrapper(api_key)

    system_prompt = (
        "You are a professional coder. Your task is to fix the provided Python code. "
        "Ensure that the code runs without errors and follows best practices."
    )

    for filename in os.listdir(input_directory):
        if filename.endswith(".py"):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as file:
                code = file.read()

            prompt = f"Please fix the following Python code:\n\n{code}"
            response = mistral_wrapper.generate_completion(system_prompt + prompt)

            # Save the response to a file
            output_file_path = os.path.join(output_directory, filename)
            with open(output_file_path, "w") as file:
                file.write(response)

if __name__ == "__main__":
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        raise ValueError("Mistral API key is required. Set it in the environment or pass it explicitly.")

    input_directory = "/workspace/input"
    output_directory = "/workspace/results"
    submit_prompts(api_key, input_directory, output_directory)

