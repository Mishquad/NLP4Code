# sender.py

import os
from mistral_wrapper import MistralWrapper

def send_file_to_mistral(input_file, output_file, api_key):
    """
    Read a .py file as text, send its content to the Mistral API,
    and save the output as a .txt file for debugging.
    """
    # Step 1: Read the .py file as raw text
    with open(input_file, 'r') as infile:
        code_content = infile.read()
    
    # Step 2: Initialize the MistralWrapper
    mistral = MistralWrapper(api_key=api_key)

    # Step 3: Send the raw text to the API
    generated_code = mistral.generate_completion(prompt=str(code_content))  # Explicit cast to string
    
    # Step 4: Save the API response as a .txt file
    if generated_code:
        with open(output_file, 'w') as outfile:
            outfile.write(generated_code)
        print(f"Output saved to {output_file}")
    else:
        print("Failed to generate output from Mistral.")
