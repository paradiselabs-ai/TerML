import subprocess
from collections import deque
import os
from . import config

class TerminalHandler:
    def __init__(self, max_history=config.MAX_HISTORY):
        self.history = deque(maxlen=max_history)
        self.last_output = ""
        self.last_command = ""
        self.current_directory = os.getcwd()
        self.last_auto_command = None
        self.last_auto_command_output = None

    def execute_command(self, command, is_auto_mode=False):
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=self.current_directory)
            self.history.append(command)
            self.last_command = command
            self.last_output = result.stdout + result.stderr
            
            # Track auto mode commands separately
            if is_auto_mode:
                self.last_auto_command = command
                self.last_auto_command_output = self.last_output
            
            return result.stdout, result.stderr
        except Exception as e:
            error_message = str(e)
            self.last_output = error_message
            return "", error_message

    def revert_last_auto_command(self):
        if not self.last_auto_command:
            return False, "No auto command to revert"

        # Analyze the last auto command to determine revert action
        command = self.last_auto_command.strip()
        
        try:
            # Handle different types of commands
            if command.startswith('mkdir'):
                # For directory creation, remove the directory
                dir_name = command.split()[-1]
                if os.path.exists(dir_name):
                    os.rmdir(dir_name)
                return True, f"Reverted directory creation: {dir_name}"
            
            elif command.startswith('touch'):
                # For file creation, remove the file
                file_name = command.split()[-1]
                if os.path.exists(file_name):
                    os.remove(file_name)
                return True, f"Reverted file creation: {file_name}"
            
            elif command.startswith('npm install') or command.startswith('pip install'):
                # For package installation, uninstall the package
                package = command.split()[-1]
                if command.startswith('npm'):
                    result = subprocess.run(f'npm uninstall {package}', shell=True, text=True, capture_output=True)
                else:
                    result = subprocess.run(f'pip uninstall -y {package}', shell=True, text=True, capture_output=True)
                return True, f"Reverted package installation: {package}"
            
            elif command.startswith('git'):
                # For git commands, handle specially
                if 'add' in command:
                    files = command.split()[2:]
                    subprocess.run('git reset HEAD ' + ' '.join(files), shell=True)
                    return True, f"Reverted git add for: {' '.join(files)}"
                elif 'commit' in command:
                    subprocess.run('git reset --soft HEAD^', shell=True)
                    return True, f"Reverted last git commit"
            
            # Add more command type handlers as needed
            
            return False, f"Unable to automatically revert command: {command}"
            
        except Exception as e:
            return False, f"Error while reverting: {str(e)}"

    def get_history(self, limit=10):
        return list(self.history)[-limit:]

    def get_last_output(self):
        return self.last_output

    def get_last_command(self):
        return self.last_command

    def get_formatted_history(self, limit=10):
        return "\n".join(self.get_history(limit))

    def get_current_directory(self):
        return self.current_directory

    def update_current_directory(self):
        self.current_directory = os.getcwd()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def list_directory(self, path='.'):
        try:
            items = os.listdir(os.path.join(self.current_directory, path))
            for item in items:
                full_path = os.path.join(self.current_directory, path, item)
                item_type = "[DIR]" if os.path.isdir(full_path) else "[FILE]"
                print(f"{item_type} {item}")
        except Exception as e:
            print(f"Error listing directory: {str(e)}")

    def get_file_content(self, filepath):
        try:
            with open(os.path.join(self.current_directory, filepath), 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, filepath, content):
        try:
            with open(os.path.join(self.current_directory, filepath), 'w') as file:
                file.write(content)
            return f"File {filepath} written successfully."
        except Exception as e:
            return f"Error writing file: {str(e)}"
