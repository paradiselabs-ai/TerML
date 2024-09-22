import ast
import os

class CodeAnalyzer:
    def __init__(self):
        self.issues = []

    def analyze_file(self, file_path):
        self.issues = []
        with open(file_path, 'r') as file:
            content = file.read()
        tree = ast.parse(content)
        self.visit(tree)
        return self.issues

    def visit(self, node):
        for child in ast.iter_child_nodes(node):
            method = getattr(self, f'visit_{child.__class__.__name__}', None)
            if method:
                method(child)
            self.visit(child)

    def visit_FunctionDef(self, node):
        if len(node.body) > 50:
            self.issues.append(f"Function '{node.name}' is too long ({len(node.body)} lines). Consider refactoring.")

    def visit_ClassDef(self, node):
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        if len(methods) > 10:
            self.issues.append(f"Class '{node.name}' has too many methods ({len(methods)}). Consider splitting it.")

    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname:
                self.issues.append(f"Consider using 'from {alias.name} import {alias.asname}' instead of 'import {alias.name} as {alias.asname}'")

def analyze_project(project_path):
    analyzer = CodeAnalyzer()
    all_issues = {}

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                issues = analyzer.analyze_file(file_path)
                if issues:
                    all_issues[file_path] = issues

    return all_issues

def get_analysis_summary(issues):
    total_issues = sum(len(file_issues) for file_issues in issues.values())
    affected_files = len(issues)
    
    summary = f"Code Analysis Summary:\n"
    summary += f"Total issues found: {total_issues}\n"
    summary += f"Affected files: {affected_files}\n\n"
    
    for file_path, file_issues in issues.items():
        summary += f"File: {file_path}\n"
        for issue in file_issues:
            summary += f"  - {issue}\n"
        summary += "\n"
    
    return summary