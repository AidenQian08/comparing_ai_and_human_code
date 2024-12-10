import ast
import radon.complexity as complexity
import radon.raw as raw
import re

def analyze_cyclomatic_complexity(code):
    analyzed = complexity.cc_visit(code)
    return {item.name: item.complexity for item in analyzed}

def count_functions(tree):
    return sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))

def count_single_line_comments(code):
    return len(re.findall(r'#.*', code))

def count_multiline_comments(tree):
    return sum(isinstance(node, ast.Expr) and isinstance(node.value, ast.Str) for node in ast.walk(tree))

def count_imports(tree):
    return sum(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))

def extract_variable_names(tree):
    # Extract variable names by looking for ast.Name nodes that are not in FunctionDefs or imports
    variable_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variable_names.add(target.id)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                variable_names.add(node.target.id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            variable_names.add(node.id)
    return list(variable_names)

def measure_correctness(code):
    # This function can be extended to actually run the code and check its correctness
    # Here, it's simplified to just check if the code can be parsed (syntactic correctness)
    try:
        compile(code, '<string>', 'exec')  # Basic check for syntax correctness
        return "Correct"  # This can be expanded with more detailed checks
    except SyntaxError:
        return "Incorrect"

def quantify_approaches(code):
    # Identify common approaches/algorithms using keyword matching
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

def analyze_raw_metrics(code):
    return raw.analyze(code)

def analyze_code(code):
    tree = ast.parse(code)
    complexity_scores = analyze_cyclomatic_complexity(code)
    raw_metrics = analyze_raw_metrics(code)
    num_functions = count_functions(tree)
    num_single_line_comments = count_single_line_comments(code)
    num_multiline_comments = count_multiline_comments(tree)
    num_imports = count_imports(tree)
    variable_names = extract_variable_names(tree)
    correctness = measure_correctness(code)
    approaches = quantify_approaches(code)
    
    analysis = {
        "complexity_scores": complexity_scores,
        "loc": raw_metrics.loc,
        "lloc": raw_metrics.lloc,
        "sloc": raw_metrics.sloc,
        "num_functions": num_functions,
        "num_single_line_comments": num_single_line_comments,
        "num_multiline_comments": num_multiline_comments,
        "comments": num_single_line_comments + num_multiline_comments,
        "blank_lines": raw_metrics.blank,
        "num_imports": num_imports,
        "variable_names": variable_names,
        "correctness": correctness,
        "approaches": approaches
    }
    
    return analysis

def read_and_analyze_solutions(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    solutions = content.split("\n\nNew Solution\n\n")
    
    for i, solution in enumerate(solutions):
        solution = solution.strip()
        if solution:
            analysis = analyze_code(solution)
            print(f"Solution {i + 1}: {analysis}")

if __name__ == "__main__":
    input_file_path = "human solutions/human_hard_uncommon.txt"  # Replace with your actual file path
    read_and_analyze_solutions(input_file_path)
    print()
