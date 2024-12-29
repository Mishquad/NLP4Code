import json
import subprocess
import tempfile
import traceback

# Path to the model's output JSON file
model_output_path = "model_output.json"  # Adjust the path to your actual output file

def run_code(code):
    """Executes Python code and returns whether it ran successfully."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Run the code using subprocess
        result = subprocess.run([
            "python", temp_file_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check for errors
        if result.returncode == 0:
            return 1  # Success
        else:
            print("Error:", result.stderr.decode())
            return 0  # Failure
    except Exception as e:
        print("Exception while running code:", traceback.format_exc())
        return 0  # Failure

# Metric: Model correctness
def evaluate_model_output(json_path):
    """Evaluate the model's output and calculate correctness."""
    try:
        with open(json_path, "r") as file:
            model_output = json.load(file)

        # Ensure the expected key exists
        if "Corrected Code" not in model_output:
            raise KeyError("The JSON output does not contain the 'Corrected Code' key.")

        corrected_code = model_output["Corrected Code"]
        
        # Run the corrected code and get the correctness score
        correctness = run_code(corrected_code)
        
        # Print and return the metric
        print(f"Model Correctness: {correctness}")
        return correctness

    except Exception as e:
        print("Error evaluating model output:", traceback.format_exc())
        return 0

if __name__ == "__main__":
    # Evaluate the model output
    evaluate_model_output(model_output_path)
