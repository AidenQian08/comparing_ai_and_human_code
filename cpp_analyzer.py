import re

def analyze_cyclomatic_complexity_cpp(code):
    # Basic regex for cyclomatic complexity: count branching keywords
    keywords = ["if", "else if", "for", "while", "case", "switch", "&&", "||", "?", "catch"]
    complexity = 1  # Starts at 1
    for keyword in keywords:
        # Use re.escape to safely escape special characters in keyword
        complexity += len(re.findall(rf'\b{re.escape(keyword)}\b', code))
    return complexity

def count_functions_cpp(code):
    # Matches function definitions (simplified)
    return len(re.findall(r'\b[A-Za-z_]\w*\s+\b[A-Za-z_]\w*\s*\(.*?\)\s*\{', code))

def count_single_line_comments_cpp(code):
    # Single line comments using //
    return len(re.findall(r'//.*', code))

def count_multiline_comments_cpp(code):
    # Multiline comments using /* ... */
    return len(re.findall(r'/\*.*?\*/', code, re.DOTALL))

def count_includes_cpp(code):
    # C++ equivalent of imports: includes
    return len(re.findall(r'#include\s+<.*?>', code))

def extract_variable_names_cpp(code):
    # Extract variable names by looking for basic C++ type declarations
    variable_pattern = r'(?:int|double|float|bool|std::string|char)\s+([A-Za-z_]\w*)'
    return re.findall(variable_pattern, code)

def count_variable_types_cpp(code):
    # Count the number of each type (int, double, bool, string, etc.)
    variable_types = {
        "int": len(re.findall(r'\bint\b', code)),
        "double": len(re.findall(r'\bdouble\b', code)),
        "bool": len(re.findall(r'\bbool\b', code)),
        "std::string": len(re.findall(r'\bstd::string\b', code)),
        "char": len(re.findall(r'\bchar\b', code)),
        "float": len(re.findall(r'\bfloat\b', code)),
    }
    return variable_types

def measure_correctness_cpp(code):
    # A basic check for correctness would involve syntax analysis.
    # For simplicity, we'll assume a valid code block if it has balanced braces, etc.
    braces_open = len(re.findall(r'\{', code))
    braces_close = len(re.findall(r'\}', code))
    if braces_open == braces_close:
        return "Correct"
    else:
        return "Incorrect"

def quantify_approaches_cpp(code):
    # Identify common approaches/algorithms in C++ using keyword matching
    approaches = []
    keywords = {
        'dfs': 'Depth-First Search',
        'bfs': 'Breadth-First Search',
        'sort': 'Sorting Algorithm',
        'dp': 'Dynamic Programming',
        'recursion': 'Recursion',
        'binary_search': 'Binary Search',
        'greedy': 'Greedy Algorithm'
    }
    for keyword, approach in keywords.items():
        if keyword in code:
            approaches.append(approach)
    return approaches

def analyze_raw_metrics_cpp(code):
    # Count lines of code and blank lines
    lines = code.splitlines()
    loc = len(lines)
    blank_lines = len([line for line in lines if line.strip() == ""])
    sloc = len([line for line in lines if line.strip() and not line.strip().startswith("//")])
    return {
        "loc": loc,
        "sloc": sloc,
        "blank": blank_lines
    }

def analyze_code_cpp(code):
    complexity = analyze_cyclomatic_complexity_cpp(code)
    raw_metrics = analyze_raw_metrics_cpp(code)
    num_functions = count_functions_cpp(code)
    num_single_line_comments = count_single_line_comments_cpp(code)
    num_multiline_comments = count_multiline_comments_cpp(code)
    num_includes = count_includes_cpp(code)
    variable_names = extract_variable_names_cpp(code)
    variable_types = count_variable_types_cpp(code)
    correctness = measure_correctness_cpp(code)
    approaches = quantify_approaches_cpp(code)
    
    analysis = {
        "complexity": complexity,
        "loc": raw_metrics["loc"],
        "sloc": raw_metrics["sloc"],
        "num_functions": num_functions,
        "num_single_line_comments": num_single_line_comments,
        "num_multiline_comments": num_multiline_comments,
        "comments": num_single_line_comments + num_multiline_comments,
        "blank_lines": raw_metrics["blank"],
        "num_includes": num_includes,
        "variable_names": variable_names,
        "variable_types": variable_types,
        "correctness": correctness,
        "approaches": approaches
    }
    
    return analysis

def read_and_analyze_solutions_cpp(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    solutions = content.split("\n\nNew Solution\n\n")
    
    for i, solution in enumerate(solutions):
        solution = solution.strip()
        if solution:
            analysis = analyze_code_cpp(solution)
            print(f"Solution {i + 1}: {analysis}")

if __name__ == "__main__":
    input_file_path = "your_path.txt"  # Replace with your actual file path. Ex. human solutions/human_easy_common.txt
    read_and_analyze_solutions_cpp(input_file_path)
    print()
