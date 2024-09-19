import os

# AI Model Configuration
AI_MODEL = "claude-3.5-sonnet-20240620"
MAX_TOKENS = 1000

# TerML Configuration
MAX_HISTORY = 100
TERML_PREFIX = "terml"

# File Paths
PID_FILE = '/tmp/terml.pid'
LOG_FILE = '/tmp/terml.log'

# API Keys
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# Logging Configuration
LOG_LEVEL = "INFO"

# Background Process Configuration
BACKGROUND_TASK_INTERVAL = 60  # seconds

# Feature Flags
IMAGE_GENERATION_ENABLED = False
WEB_SEARCH_ENABLED = False

# Command-specific Configuration
EXPLAIN_MAX_TOKENS = 500
SUGGEST_MAX_TOKENS = 300
CHAT_MAX_TOKENS = 1000
DEBUG_MAX_TOKENS = 800
AUTO_MAX_TOKENS = 1000

# System Prompts
BASE_PROMPT = "You are TerML, an AI assistant for terminal users. Provide clear, concise explanations."
EXPLAIN_PROMPT = BASE_PROMPT + " Explain the given terminal output."
SUGGEST_PROMPT = BASE_PROMPT + " Suggest a helpful next command based on history."
DEBUG_PROMPT = BASE_PROMPT + " Debug the given command and its output."
AUTO_PROMPT = BASE_PROMPT + " Generate commands to set up a project."
CHAT_PROMPT = BASE_PROMPT + " Respond to user questions about terminal usage."