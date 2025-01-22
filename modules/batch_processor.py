# batch_processor.py

import os
from sender import send_file_to_mistral
from evaluation import evaluate_generated_files

def process_files(input_dir, output_dir):
    """
    Send each Python file in the input directory to Mistral,
    save the output to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".py"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, f"generated_{file_name}")
            print(f"Processing {file_name}...")
            send_file_to_mistral(input_path, output_path, api_key="1TNjHnTyCxWE0K4zUfNyeGt1oMYSDCPV")

def main():
    # Define directories
    input_dir = "./input_files"    # Directory with input .py files
    output_dir = "./generated_files"  # Directory to save generated files
    
    # Step 1: Process all .py files
    print("Starting file processing...")
    process_files(input_dir, output_dir)
    print("File processing complete.")
    
    # Step 2: Evaluate the generated files
    print("Starting evaluation...")
    success_rate = evaluate_generated_files(output_dir)
    print(f"Evaluation complete. Success rate: {success_rate:.2%}")

if __name__ == "__main__":
    main()
