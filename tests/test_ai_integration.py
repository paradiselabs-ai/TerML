import pytest
from unittest.mock import patch, MagicMock
from terml.ai_integration import AIIntegration
from terml import config

@pytest.fixture
def ai_integration():
    return AIIntegration()

def test_ai_integration_initialization(ai_integration):
    assert isinstance(ai_integration, AIIntegration)
    assert ai_integration.model == config.AI_MODEL

@patch('terml.ai_integration.anthropic.Anthropic')
def test_get_ai_response(mock_anthropic, ai_integration):
    mock_client = MagicMock()
    mock_messages = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Mocked AI response"
    mock_messages.create.return_value = mock_message
    mock_client.messages = mock_messages
    mock_anthropic.return_value = mock_client

    # Replace the client in the AIIntegration instance
    ai_integration.client = mock_client

    prompt = "Test prompt"
    system_prompt = "Test system prompt"
    max_tokens = 100
    response = ai_integration.get_ai_response(prompt, system_prompt, max_tokens)

    assert response == "Mocked AI response"
    mock_messages.create.assert_called_once_with(
        model=config.AI_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

def test_explain_output(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response:
        mock_get_ai_response.return_value = "Mocked explanation"
        output = "Test output"
        explanation = ai_integration.explain_output(output)
        assert explanation == "Mocked explanation"
        mock_get_ai_response.assert_called_once()

def test_suggest_command(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response:
        mock_get_ai_response.return_value = "ls -la"
        command_history = ["cd /home", "mkdir test_dir"]
        suggestion = ai_integration.suggest_command(command_history)
        assert suggestion == "ls -la"
        mock_get_ai_response.assert_called_once()

def test_debug_command(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response:
        mock_get_ai_response.return_value = "The command failed due to insufficient permissions."
        command = "rm -rf /root"
        error_output = "Permission denied"
        debug_info = ai_integration.debug_command(command, error_output)
        assert debug_info == "The command failed due to insufficient permissions."
        mock_get_ai_response.assert_called_once()

def test_generate_auto_commands(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response:
        mock_get_ai_response.return_value = "npm init -y"
        goal = "Initialize a Node.js project"
        tech_stack = "Node.js, Express"
        auto_command = ai_integration.generate_auto_commands(goal, tech_stack)
        assert auto_command == "npm init -y"
        mock_get_ai_response.assert_called_once()

def test_chat_response(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response:
        mock_get_ai_response.return_value = "To list files in a directory, use the 'ls' command."
        user_input = "How do I list files in a directory?"
        response = ai_integration.chat_response(user_input)
        assert response == "To list files in a directory, use the 'ls' command."
        mock_get_ai_response.assert_called_once()

def test_summarize_contents(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response, \
         patch('os.path.isfile') as mock_isfile, \
         patch('os.path.isdir') as mock_isdir, \
         patch('builtins.open', create=True) as mock_open:
        mock_get_ai_response.return_value = "This is a summary of the file contents."
        mock_isfile.return_value = True
        mock_isdir.return_value = False
        mock_open.return_value.__enter__.return_value.read.return_value = "File contents"
        
        summary = ai_integration.summarize_contents("/path/to/file")
        assert summary == "This is a summary of the file contents."
        mock_get_ai_response.assert_called_once()

def test_suggest_code_improvements(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response:
        mock_get_ai_response.return_value = "Consider adding error handling to improve robustness."
        analysis_summary = "Function lacks error handling"
        suggestions = ai_integration.suggest_code_improvements(analysis_summary)
        assert suggestions == "Consider adding error handling to improve robustness."
        mock_get_ai_response.assert_called_once()

def test_suggest_test_improvements(ai_integration):
    with patch.object(AIIntegration, 'get_ai_response') as mock_get_ai_response, \
         patch('os.listdir') as mock_listdir, \
         patch('builtins.open', create=True) as mock_open:
        mock_get_ai_response.return_value = "Add more edge case tests to improve coverage."
        mock_listdir.return_value = ["test_module.py"]
        mock_open.return_value.__enter__.return_value.read.return_value = "def test_function(): pass"
        
        suggestions = ai_integration.suggest_test_improvements("/path/to/project")
        assert suggestions == "Add more edge case tests to improve coverage."
        mock_get_ai_response.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])