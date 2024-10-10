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

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=self.current_directory)
            self.history.append(command)
            self.last_command = command
            self.last_output = result.stdout + result.stderr
            return result.stdout, result.stderr
        except Exception as e:
            error_message = str(e)
            self.last_output = error_message
            return "", error_message

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