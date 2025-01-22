# evaluation.py

import os
import subprocess

def evaluate_generated_files(directory):
    """
    Evaluate Python files in the directory.
    Returns the success rate of file execution.
    """
    total_files = 0
    successful_runs = 0

    for file in os.listdir(directory):
        if file.endswith(".py"):
            total_files += 1
            file_path = os.path.join(directory, file)
            try:
                subprocess.run(
                    ["python", file_path],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                successful_runs += 1
            except subprocess.CalledProcessError:
                print(f"Error executing {file}")
    
    if total_files == 0:
        print("No Python files found for evaluation.")
        return 0

    success_rate = successful_runs / total_files
    print(f"Success rate: {success_rate:.2%}")
    return success_rate

# Example usage
if __name__ == "__main__":
    directory_to_evaluate = "./generated_files"
    evaluate_generated_files(directory_to_evaluate)
