import os
from . import config
from .llm_providers import LLMProvider
from .llm_providers.openrouter import OpenRouterProvider
from .llm_providers.huggingface import HuggingFaceProvider

class AIIntegration:
    def __init__(self):
        # Dynamically select the LLM provider
        self.provider = self._get_provider()
        self.conversation_history = []

    def _get_provider(self) -> LLMProvider:
        """Select the appropriate LLM provider based on configuration"""
        provider_map = {
            "anthropic": self._get_anthropic_provider,
            "openrouter": self._get_openrouter_provider,
            "huggingface": self._get_huggingface_provider
        }
        
        provider_func = provider_map.get(config.LLM_PROVIDER.lower(), 
                                         self._get_anthropic_provider)
        return provider_func()

    def _get_anthropic_provider(self):
        """Import and instantiate Anthropic provider"""
        import anthropic
        class AnthropicProvider(LLMProvider):
            def __init__(self):
                self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
                self.model = config.AI_MODEL
                self.conversation_history = []

            def get_response(self, messages, system_prompt, max_tokens):
                try:
                    message = self.client.messages.create(
                        model=self.model,
                        max_tokens=max_tokens,
                        messages=[{"role": "system", "content": system_prompt}] + messages
                    )
                    return message.content[0].text
                except Exception as e:
                    return f"Error: {str(e)}"

            def get_chat_response(self, user_input, conversation_history):
                self.conversation_history.append({"role": "user", "content": user_input})
                
                response = self.get_response(
                    messages=self.conversation_history,
                    system_prompt=config.CHAT_PROMPT,
                    max_tokens=config.CHAT_MAX_TOKENS
                )
                
                self.conversation_history.append({"role": "assistant", "content": response})
                return response

            def clear_chat_history(self):
                self.conversation_history = []

            def supports_streaming(self):
                return False

        return AnthropicProvider()

    def _get_openrouter_provider(self):
        """Get OpenRouter provider"""
        return OpenRouterProvider()

    def _get_huggingface_provider(self):
        """Get HuggingFace provider"""
        return HuggingFaceProvider()

    def get_ai_response(self, prompt, system_prompt, max_tokens):
        """Generic method to get AI response"""
        messages = [{"role": "user", "content": prompt}]
        return self.provider.get_response(messages, system_prompt, max_tokens)

    def explain_output(self, output):
        """Explain terminal output"""
        prompt = f"Explain this terminal output in simple terms: {output}"
        return self.get_ai_response(prompt, config.EXPLAIN_PROMPT, config.EXPLAIN_MAX_TOKENS)

    def suggest_command(self, history):
        """Suggest next command based on history"""
        prompt = f"Based on this command history, suggest a helpful next command: {history}"
        return self.get_ai_response(prompt, config.SUGGEST_PROMPT, config.SUGGEST_MAX_TOKENS)

    def debug_command(self, command, output):
        """Debug command and output"""
        prompt = f"Debug this command and its output. Explain what might have gone wrong and suggest a correction:\nCommand: {command}\nOutput: {output}"
        return self.get_ai_response(prompt, config.DEBUG_PROMPT, config.DEBUG_MAX_TOKENS)

    def generate_auto_commands(self, goal, tech_stack):
        """Generate auto commands for project setup"""
        prompt = f"Generate a command to help set up a project with the following goal: '{goal}' and tech stack: '{tech_stack}'. Provide the command and a detailed explanation of what it does."
        return self.get_ai_response(prompt, config.AUTO_PROMPT, config.AUTO_MAX_TOKENS)

    def chat_response(self, user_input, retain_memory=False):
        """Get chat response"""
        if retain_memory:
            return self.provider.get_chat_response(user_input, self.conversation_history)
        else:
            return self.get_ai_response(
                user_input, 
                config.CHAT_PROMPT, 
                config.CHAT_MAX_TOKENS
            )

    def clear_chat_history(self):
        """Clear chat history"""
        self.provider.clear_chat_history()
        self.conversation_history = []

    def summarize_contents(self, path):
        """Summarize file or directory contents"""
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
        """Suggest code improvements"""
        prompt = f"Based on the following code analysis summary, suggest improvements and best practices:\n\n{analysis_summary}"
        return self.get_ai_response(prompt, config.CODE_IMPROVEMENT_PROMPT, config.CODE_IMPROVEMENT_MAX_TOKENS)

    def suggest_test_improvements(self, project_path):
        """Suggest test improvements"""
        test_files = [f for f in os.listdir(project_path) if f.startswith('test_') and f.endswith('.py')]
        test_contents = ""
        for test_file in test_files:
            with open(os.path.join(project_path, test_file), 'r') as f:
                test_contents += f"File: {test_file}\n{f.read()}\n\n"
        
        prompt = f"Analyze the following test files and suggest improvements for better test coverage and quality:\n\n{test_contents}"
        return self.get_ai_response(prompt, config.TEST_IMPROVEMENT_PROMPT, config.TEST_IMPROVEMENT_MAX_TOKENS)
