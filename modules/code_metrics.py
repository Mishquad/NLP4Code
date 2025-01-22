# File: code_evaluation.py

import os
import ast
import time
import statistics
from tabulate import tabulate

class CodeEvaluator:
    def __init__(self, directory):
        self.directory = directory
        self.results = []

    def evaluate_directory(self):
        py_files = [f for f in os.listdir(self.directory) if f.endswith(".py")]
        for file in py_files:
            file_path = os.path.join(self.directory, file)
            self.results.append(self.evaluate_file(file_path))
        return self.generate_report()

    def evaluate_file(self, file_path):
        metrics = {
            "file_name": os.path.basename(file_path),
            "functional_correctness": self.check_functional_correctness(file_path),
            "syntactic_closeness": self.check_syntactic_closeness(file_path),
            "semantic_accuracy": self.check_semantic_accuracy(file_path),
            "completion_rate": 1,  # If the file is processed, it’s considered completed.
            "execution_accuracy": self.check_execution_accuracy(file_path),
            "efficiency_metrics": self.check_efficiency_metrics(file_path),
            "natural_language_understanding": self.check_natural_language_understanding(file_path),
            "generalization_to_new_domains": self.check_generalization(file_path),
        }
        return metrics

    def check_functional_correctness(self, file_path):
        """Mock correctness by trying to import and run the script."""
        try:
            exec(open(file_path).read(), {})
            return 1
        except Exception:
            return 0

    def check_syntactic_closeness(self, file_path):
        """Check the complexity of the AST as a proxy for syntactic similarity."""
        try:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())
            return len(list(ast.walk(tree)))  # Number of AST nodes
        except Exception:
            return 0

    def check_semantic_accuracy(self, file_path):
        """Look for docstrings and expected outputs."""
        try:
            with open(file_path, "r") as f:
                content = f.read()
            if '"""' in content or "'''" in content:  # Check for docstrings
                return 1
            return 0
        except Exception:
            return 0

    def check_execution_accuracy(self, file_path):
        """Test if the file runs without crashing."""
        try:
            exec(open(file_path).read(), {})
            return 1
        except Exception:
            return 0

    def check_efficiency_metrics(self, file_path):
        """Measure execution time."""
        try:
            start_time = time.time()
            exec(open(file_path).read(), {})
            elapsed_time = time.time() - start_time
            return max(0, 1 - elapsed_time)  # Higher is better
        except Exception:
            return 0

    def check_natural_language_understanding(self, file_path):
        """Count docstring usage as a proxy for understanding."""
        try:
            with open(file_path, "r") as f:
                content = f.read()
            docstring_count = content.count('"""') + content.count("'''")
            return 1 if docstring_count > 0 else 0
        except Exception:
            return 0

    def check_generalization(self, file_path):
        """Mock generalization by assigning a score based on diversity in directory."""
        other_files = os.listdir(self.directory)
        if len(other_files) > 5:
            return 1
        return 0

    def generate_report(self):
        """Generate a summary table."""
        summary = []
        for metric in self.results:
            summary.append([
                metric["file_name"],
                metric["functional_correctness"],
                metric["syntactic_closeness"],
                metric["semantic_accuracy"],
                metric["completion_rate"],
                metric["execution_accuracy"],
                metric["efficiency_metrics"],
                metric["natural_language_understanding"],
                metric["generalization_to_new_domains"],
            ])
        headers = [
            "File Name",
            "Functional Correctness",
            "Syntactic Closeness",
            "Semantic Accuracy",
            "Completion Rate",
            "Execution Accuracy",
            "Efficiency Metrics",
            "NL Understanding",
            "Generalization",
        ]
        print(tabulate(summary, headers=headers, tablefmt="grid"))
        return summary


if __name__ == "__main__":
    # Change 'your_directory_path' to the directory containing your .py files
    directory = "your_directory_path"
    evaluator = CodeEvaluator(directory)
    evaluator.evaluate_directory()
