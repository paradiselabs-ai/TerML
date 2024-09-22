import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# AI Model Configuration
AI_MODEL = "claude-3.5-sonnet-20240620"
MAX_TOKENS = 1000

# TerML Configuration
MAX_HISTORY = 100
TERML_PREFIX = "terml"

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("Warning: ANTHROPIC_API_KEY environment variable is not set. Using a dummy key for testing.")
    ANTHROPIC_API_KEY = "dummy_api_key_for_testing"

# Logging Configuration
LOG_LEVEL = "INFO"

# Command-specific Configuration
EXPLAIN_MAX_TOKENS = 500
SUGGEST_MAX_TOKENS = 300
CHAT_MAX_TOKENS = 1000
DEBUG_MAX_TOKENS = 800
AUTO_MAX_TOKENS = 1000
SUMMARIZE_MAX_TOKENS = 800
CODE_IMPROVEMENT_MAX_TOKENS = 1000
TEST_IMPROVEMENT_MAX_TOKENS = 1000

# System Prompts
BASE_PROMPT = "You are TerML, an AI assistant for terminal users. Provide clear, concise, and helpful responses."
EXPLAIN_PROMPT = BASE_PROMPT + " Explain the given terminal output in simple terms, focusing on what it means and why it's important."
SUGGEST_PROMPT = BASE_PROMPT + " Suggest a helpful next command based on the given command history. Explain why this command would be useful."
DEBUG_PROMPT = BASE_PROMPT + " Analyze the given command and its output. Explain what might have gone wrong and suggest a correction or improvement."
AUTO_PROMPT = BASE_PROMPT + " Generate a command to set up a project based on the given goal and tech stack. Provide a detailed explanation of what the command does and why it's appropriate."
CHAT_PROMPT = BASE_PROMPT + " Respond to user questions about terminal usage, command-line interfaces, or programming concepts. Provide helpful and educational answers."
SUMMARIZE_PROMPT = BASE_PROMPT + " Summarize the contents of the given file or directory. For files, focus on the main points and structure. For directories, provide an overview of the contained files and their purposes."
CODE_IMPROVEMENT_PROMPT = BASE_PROMPT + " Analyze the given code analysis summary and suggest improvements. Focus on best practices, code organization, and potential optimizations."
TEST_IMPROVEMENT_PROMPT = BASE_PROMPT + " Analyze the given test files and suggest improvements for better test coverage and quality. Focus on test completeness, edge cases, and best practices in unit testing."

# Error Messages
API_KEY_ERROR = "Error: Anthropic API key not found. Please set the ANTHROPIC_API_KEY environment variable."
COMMAND_ERROR = "Error: Unknown TerML command. Use 'terml --help' for available commands."