import pytest
import sys
from unittest.mock import patch, MagicMock, mock_open, call
from terml import main
from terml.commands import CommandExecutor
from terml.ai_integration import AIIntegration
from terml.dependency_manager import get_dependency_info
from terml.code_analyzer import analyze_project
from terml.test_generator import generate_and_write_tests
from terml.project_templates import create_project_structure, list_available_templates
from terml.git_helper import analyze_git_state, provide_git_guidance, get_quick_git_help

def test_terml_import():
    assert main is not None

def test_cli_exists():
    assert hasattr(main, 'cli')
    assert callable(main.cli)

def test_command_executor_exists():
    assert CommandExecutor is not None

def test_ai_integration_exists():
    assert AIIntegration is not None

def test_dependency_manager_exists():
    assert get_dependency_info is not None

def test_code_analyzer_exists():
    assert analyze_project is not None

def test_test_generator_exists():
    assert generate_and_write_tests is not None

def test_project_templates_exists():
    assert create_project_structure is not None
    assert list_available_templates is not None

def test_git_helper_exists():
    assert analyze_git_state is not None
    assert provide_git_guidance is not None
    assert get_quick_git_help is not None

def test_command_executor_execute():
    mock_terminal_handler = MagicMock()
    mock_ai_integration = MagicMock()
    executor = CommandExecutor(mock_terminal_handler, mock_ai_integration)
    
    # Create a mock method to track calls
    with patch.object(executor, 'execute', wraps=executor.execute) as mock_method:
        executor.execute("terml test_command")
        
        # Check that the method was called with the correct arguments
        assert mock_method.call_count == 1
        call_args, call_kwargs = mock_method.call_args
        assert call_args[0] == "terml test_command"
        assert call_kwargs.get('retain_memory', False) == False

@patch('terml.dependency_manager.get_project_type')
@patch('terml.dependency_manager.check_outdated_dependencies')
@patch('builtins.open', new_callable=mock_open, read_data="pytest==6.2.5\nclick==8.0.3")
def test_get_dependency_info(mock_file, mock_check_outdated, mock_get_project_type):
    mock_get_project_type.return_value = 'python'
    mock_check_outdated.return_value = []

    result = get_dependency_info("test_project")

    assert "dependencies" in result
    assert "total_dependencies" in result
    assert "outdated_dependencies" in result
    assert "outdated" in result
    assert result["dependencies"] == {"pytest": "6.2.5", "click": "8.0.3"}

@patch('terml.code_analyzer.os.walk')
@patch('terml.code_analyzer.CodeAnalyzer.analyze_file')
def test_analyze_project(mock_analyze_file, mock_walk):
    mock_walk.return_value = [
        ('/test_project', [], ['test_file.py'])
    ]
    mock_analyze_file.return_value = ["Function 'test_func' is too long (60 lines). Consider refactoring."]

    expected_result = {
        '/test_project/test_file.py': ["Function 'test_func' is too long (60 lines). Consider refactoring."]
    }

    result = analyze_project("/test_project")

    assert result == expected_result
    mock_analyze_file.assert_called_once_with('/test_project/test_file.py')

@patch('terml.test_generator.generate_and_write_tests')
def test_generate_and_write_tests(mock_generate):
    expected_result = [
        "/path/to/test_file1.py",
        "/path/to/test_file2.py",
        "/path/to/test_file3.py"
    ]
    mock_generate.return_value = expected_result

    result = mock_generate("test_project")

    assert result == expected_result
    mock_generate.assert_called_once_with("test_project")

@patch('terml.project_templates.create_project_structure')
def test_create_project_structure(mock_create):
    expected_path = "/Users/cooper/Desktop/AI_ML/Creating/ParadiseLabs/My AI Projects/TerML/new_project"
    mock_create.return_value = expected_path

    # Explicitly pass two separate arguments with a comma
    result = mock_create("python", "new_project")

    assert result == expected_path
    mock_create.assert_called_once_with("python", "new_project")

def test_list_available_templates():
    with patch('terml.project_templates.TEMPLATES', {"python": {}, "javascript": {}, "react": {}}):
        result = list_available_templates()
        assert result == ["python", "javascript", "react"]

@patch('terml.git_helper.subprocess.run')
def test_analyze_git_state(mock_run):
    mock_run.side_effect = [
        MagicMock(returncode=0),  # git rev-parse
        MagicMock(stdout="M file1.py\n?? file2.py"),  # git status
        MagicMock(stdout="main")  # git rev-parse --abbrev-ref HEAD
    ]

    state, details = analyze_git_state()

    assert state == "Changes present"
    assert "Currently on branch 'main'" in details
    assert "1 file(s) staged for commit" in details
    assert "1 untracked file(s)" in details

def test_provide_git_guidance():
    state = "Changes present"
    details = [
        "Currently on branch 'main'",
        "1 file(s) staged for commit",
        "1 untracked file(s)"
    ]

    guidance = provide_git_guidance(state, details)

    assert "You have staged changes" in guidance
    assert "You have untracked files" in guidance

def test_get_quick_git_help():
    help_text = get_quick_git_help()

    assert "Common Git Commands:" in help_text
    assert "git init:" in help_text
    assert "git clone" in help_text
    assert "git add" in help_text
    assert "git commit" in help_text
    assert "git push" in help_text
    assert "git pull" in help_text

if __name__ == "__main__":
    pytest.main([__file__])
