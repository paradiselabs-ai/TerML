import os
import subprocess
import json

def get_project_type(project_path):
    if os.path.exists(os.path.join(project_path, 'package.json')):
        return 'nodejs'
    elif os.path.exists(os.path.join(project_path, 'requirements.txt')):
        return 'python'
    else:
        return 'unknown'

def get_dependencies(project_path):
    project_type = get_project_type(project_path)
    if project_type == 'nodejs':
        with open(os.path.join(project_path, 'package.json'), 'r') as f:
            package_json = json.load(f)
        return package_json.get('dependencies', {})
    elif project_type == 'python':
        with open(os.path.join(project_path, 'requirements.txt'), 'r') as f:
            return dict(line.strip().split('==') for line in f if '==' in line)
    else:
        return {}

def update_dependencies(project_path):
    project_type = get_project_type(project_path)
    if project_type == 'nodejs':
        subprocess.run(['npm', 'update'], cwd=project_path, check=True)
    elif project_type == 'python':
        subprocess.run(['pip', 'install', '--upgrade', '-r', 'requirements.txt'], cwd=project_path, check=True)
    else:
        raise ValueError(f"Unsupported project type in {project_path}")

def add_dependency(project_path, dependency, version=None):
    project_type = get_project_type(project_path)
    if project_type == 'nodejs':
        cmd = ['npm', 'install', dependency]
        if version:
            cmd[-1] += f'@{version}'
        subprocess.run(cmd, cwd=project_path, check=True)
    elif project_type == 'python':
        cmd = ['pip', 'install', dependency]
        if version:
            cmd[-1] += f'=={version}'
        subprocess.run(cmd, cwd=project_path, check=True)
        # Update requirements.txt
        subprocess.run(['pip', 'freeze', '>', 'requirements.txt'], cwd=project_path, shell=True, check=True)
    else:
        raise ValueError(f"Unsupported project type in {project_path}")

def remove_dependency(project_path, dependency):
    project_type = get_project_type(project_path)
    if project_type == 'nodejs':
        subprocess.run(['npm', 'uninstall', dependency], cwd=project_path, check=True)
    elif project_type == 'python':
        subprocess.run(['pip', 'uninstall', '-y', dependency], cwd=project_path, check=True)
        # Update requirements.txt
        subprocess.run(['pip', 'freeze', '>', 'requirements.txt'], cwd=project_path, shell=True, check=True)
    else:
        raise ValueError(f"Unsupported project type in {project_path}")

def check_outdated_dependencies(project_path):
    project_type = get_project_type(project_path)
    if project_type == 'nodejs':
        result = subprocess.run(['npm', 'outdated', '--json'], cwd=project_path, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    elif project_type == 'python':
        result = subprocess.run(['pip', 'list', '--outdated', '--format=json'], cwd=project_path, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    else:
        raise ValueError(f"Unsupported project type in {project_path}")

def get_dependency_info(project_path):
    dependencies = get_dependencies(project_path)
    outdated = check_outdated_dependencies(project_path)
    
    info = {
        "total_dependencies": len(dependencies),
        "outdated_dependencies": len(outdated),
        "dependencies": dependencies,
        "outdated": outdated
    }
    
    return info