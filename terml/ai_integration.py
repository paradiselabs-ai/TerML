import anthropic
import os
from . import config

class AIIntegration:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = config.AI_MODEL

    def get_ai_response(self, prompt, system_prompt, max_tokens):
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def explain_output(self, output):
        prompt = f"Explain this terminal output in simple terms: {output}"
        return self.get_ai_response(prompt, config.EXPLAIN_PROMPT, config.EXPLAIN_MAX_TOKENS)

    def suggest_command(self, history):
        prompt = f"Based on this command history, suggest a helpful next command: {history}"
        return self.get_ai_response(prompt, config.SUGGEST_PROMPT, config.SUGGEST_MAX_TOKENS)

    def debug_command(self, command, output):
        prompt = f"Debug this command and its output. Explain what might have gone wrong and suggest a correction:\nCommand: {command}\nOutput: {output}"
        return self.get_ai_response(prompt, config.DEBUG_PROMPT, config.DEBUG_MAX_TOKENS)

    def generate_auto_commands(self, goal, tech_stack):
        prompt = f"Generate a command to help set up a project with the following goal: '{goal}' and tech stack: '{tech_stack}'. Provide the command and a detailed explanation of what it does."
        return self.get_ai_response(prompt, config.AUTO_PROMPT, config.AUTO_MAX_TOKENS)

    def chat_response(self, user_input):
        prompt = f"Respond to this user query about terminal usage or programming: {user_input}"
        return self.get_ai_response(prompt, config.CHAT_PROMPT, config.CHAT_MAX_TOKENS)

    def summarize_contents(self, path):
        if os.path.isfile(path):
            with open(path, 'r') as file:
                content = file.read()
            prompt = f"Summarize the contents of this file:\n\n{content}"
        elif os.path.isdir(path):
            files = os.listdir(path)
            prompt = f"Summarize the contents of this directory:\n\n{', '.join(files)}"
        else:
            return "Error: The specified path is neither a file nor a directory."

        return self.get_ai_response(prompt, config.SUMMARIZE_PROMPT, config.SUMMARIZE_MAX_TOKENS)

    def suggest_code_improvements(self, analysis_summary):
        prompt = f"Based on the following code analysis summary, suggest improvements and best practices:\n\n{analysis_summary}"
        return self.get_ai_response(prompt, config.CODE_IMPROVEMENT_PROMPT, config.CODE_IMPROVEMENT_MAX_TOKENS)

    def suggest_test_improvements(self, project_path):
        test_files = [f for f in os.listdir(project_path) if f.startswith('test_') and f.endswith('.py')]
        test_contents = ""
        for test_file in test_files:
            with open(os.path.join(project_path, test_file), 'r') as f:
                test_contents += f"File: {test_file}\n{f.read()}\n\n"
        
        prompt = f"Analyze the following test files and suggest improvements for better test coverage and quality:\n\n{test_contents}"
        return self.get_ai_response(prompt, config.TEST_IMPROVEMENT_PROMPT, config.TEST_IMPROVEMENT_MAX_TOKENS)