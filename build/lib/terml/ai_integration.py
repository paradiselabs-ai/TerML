import anthropic
from . import config

class AIIntegration:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = config.AI_MODEL

    def get_ai_response(self, prompt, system_prompt, max_tokens):
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def explain_output(self, output):
        prompt = f"Explain this terminal output: {output}"
        return self.get_ai_response(prompt, config.EXPLAIN_PROMPT, config.EXPLAIN_MAX_TOKENS)

    def suggest_command(self, history):
        prompt = f"Suggest a command based on this history: {history}"
        return self.get_ai_response(prompt, config.SUGGEST_PROMPT, config.SUGGEST_MAX_TOKENS)

    def debug_command(self, command, output):
        prompt = f"Debug this command and output: Command: {command}, Output: {output}"
        return self.get_ai_response(prompt, config.DEBUG_PROMPT, config.DEBUG_MAX_TOKENS)

    def generate_auto_commands(self, goal, tech_stack):
        prompt = f"Generate commands for: Goal: {goal}, Tech Stack: {tech_stack}"
        return self.get_ai_response(prompt, config.AUTO_PROMPT, config.AUTO_MAX_TOKENS)

    def chat_response(self, user_input):
        return self.get_ai_response(user_input, config.CHAT_PROMPT, config.CHAT_MAX_TOKENS)