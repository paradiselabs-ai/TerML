import os
import json

TEMPLATES = {
    "python": {
        "files": {
            "main.py": "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()",
            "requirements.txt": "",
            "README.md": "# Python Project\n\nThis is a basic Python project template.",
            ".gitignore": "*.pyc\n__pycache__/\nvenv/\n.vscode/",
        },
        "directories": ["src", "tests"]
    },
    "javascript": {
        "files": {
            "index.js": "console.log('Hello, World!');",
            "package.json": json.dumps({
                "name": "javascript-project",
                "version": "1.0.0",
                "description": "A basic JavaScript project",
                "main": "index.js",
                "scripts": {
                    "start": "node index.js"
                }
            }, indent=2),
            "README.md": "# JavaScript Project\n\nThis is a basic JavaScript project template.",
            ".gitignore": "node_modules/\n.vscode/",
        },
        "directories": ["src", "test"]
    },
    "react": {
        "files": {
            "src/App.js": "import React from 'react';\n\nfunction App() {\n  return (\n    <div className=\"App\">\n      <h1>Hello, React!</h1>\n    </div>\n  );\n}\n\nexport default App;",
            "src/index.js": "import React from 'react';\nimport ReactDOM from 'react-dom';\nimport App from './App';\n\nReactDOM.render(\n  <React.StrictMode>\n    <App />\n  </React.StrictMode>,\n  document.getElementById('root')\n);",
            "public/index.html": "<!DOCTYPE html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"utf-8\" />\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n    <title>React App</title>\n  </head>\n  <body>\n    <noscript>You need to enable JavaScript to run this app.</noscript>\n    <div id=\"root\"></div>\n  </body>\n</html>",
            "README.md": "# React Project\n\nThis is a basic React project template.",
            ".gitignore": "node_modules/\nbuild/\n.env\n.vscode/",
        },
        "directories": ["src", "public"]
    }
}

def create_project_structure(project_type, project_name):
    if project_type not in TEMPLATES:
        raise ValueError(f"Unsupported project type: {project_type}")

    template = TEMPLATES[project_type]
    project_path = os.path.join(os.getcwd(), project_name)

    # Create project directory
    os.makedirs(project_path, exist_ok=True)

    # Create subdirectories
    for directory in template["directories"]:
        os.makedirs(os.path.join(project_path, directory), exist_ok=True)

    # Create files
    for file_name, content in template["files"].items():
        file_path = os.path.join(project_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

    return project_path

def list_available_templates():
    return list(TEMPLATES.keys())