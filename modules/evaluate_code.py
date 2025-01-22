import os
import subprocess

def evaluate_code(file_path):
    try:
        result = subprocess.run(['python3', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return 1  # Code ran without errors
        else:
            print(f"Error in {file_path}: {result.stderr}")
            return 0  # Code had errors
    except Exception as e:
        print(f"Exception in {file_path}: {e}")
        return 0  # Code had errors

def evaluate_all_results(directory):
    results = {}
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            file_path = os.path.join(directory, filename)
            results[filename] = evaluate_code(file_path)
    return results

if __name__ == "__main__":
    results_directory = "/workspace/results"
    results = evaluate_all_results(results_directory)
    with open("/workspace/evaluation_results.json", "w") as file:
        json.dump(results, file, indent=4)

