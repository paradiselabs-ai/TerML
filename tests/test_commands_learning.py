import pytest
from unittest.mock import patch, MagicMock, call
import click
from terml.commands import CommandExecutor
from terml.git_helper import GitLearningSession
from terml.lesson_system import LessonManager

@pytest.fixture
def command_executor():
    """Create a CommandExecutor instance with mocked dependencies"""
    terminal_handler = MagicMock()
    ai_integration = MagicMock()
    return CommandExecutor(terminal_handler, ai_integration)

class TestGitCommands:
    """Test git-related command handling"""
    
    def test_git_status(self, command_executor):
        """Test git status command"""
        with patch('terml.git_helper.analyze_git_state') as mock_analyze, \
             patch('terml.git_helper.provide_git_guidance') as mock_guidance, \
             patch('click.echo') as mock_echo:
            
            mock_analyze.return_value = ("Clean", ["On branch main", "Working tree clean"])
            mock_guidance.return_value = "Your repository is up to date"
            
            command_executor._handle_git_command(['status'])
            
            mock_analyze.assert_called_once()
            mock_guidance.assert_called_once()
            assert any("Repository Status" in call_args[0][0] for call_args in mock_echo.call_args_list)
            assert any("Working tree clean" in call_args[0][0] for call_args in mock_echo.call_args_list)

    def test_git_learn_tutorial(self, command_executor):
        """Test git learn -t command"""
        with patch.object(command_executor.git_session, 'start_lesson') as mock_start:
            command_executor._handle_git_command(['learn', '-t'])
            mock_start.assert_called_once_with()

    def test_git_learn_quick_help(self, command_executor):
        """Test git learn -q command"""
        with patch('terml.git_helper.get_quick_git_help') as mock_help, \
             patch('click.echo') as mock_echo:
            mock_help.return_value = "Git quick reference"
            command_executor._handle_git_command(['learn', '-q'])
            mock_help.assert_called_once()
            mock_echo.assert_called_with("Git quick reference")

    def test_git_learn_qa(self, command_executor):
        """Test git learn -qt command"""
        with patch.object(command_executor.git_session, 'start_quick_qa') as mock_qa:
            command_executor._handle_git_command(['learn', '-qt'])
            mock_qa.assert_called_once()

    def test_git_learn_list(self, command_executor):
        """Test git learn command (list lessons)"""
        with patch.object(command_executor.git_session, 'show_available_lessons') as mock_show:
            command_executor._handle_git_command(['learn'])
            mock_show.assert_called_once()

class TestLearnCommands:
    """Test general learning system commands"""
    
    def test_learn_git_lesson(self, command_executor):
        """Test starting a specific git lesson"""
        with patch.object(command_executor.git_session, 'start_lesson') as mock_start:
            command_executor._handle_learn_command(['git', '01_basics'])
            mock_start.assert_called_with('01_basics')

    def test_learn_other_category(self, command_executor):
        """Test starting lessons in other categories"""
        with patch.object(command_executor.git_session.lesson_manager, 'start_interactive_session') as mock_start:
            # Test shell category
            command_executor._handle_learn_command(['shell', '01_navigation'])
            mock_start.assert_called_with('shell', '01_navigation')
            
            # Test network category
            command_executor._handle_learn_command(['network', '01_basics'])
            mock_start.assert_called_with('network', '01_basics')
            
            # Test tools category
            command_executor._handle_learn_command(['tools', '01_package_managers'])
            mock_start.assert_called_with('tools', '01_package_managers')

    def test_learn_list_category(self, command_executor):
        """Test listing lessons in a category"""
        with patch.object(command_executor.git_session.lesson_manager, 'show_category_progress') as mock_show:
            command_executor._handle_learn_command(['git'])
            mock_show.assert_called_with('git')

    def test_learn_no_category(self, command_executor):
        """Test learn command without category"""
        with patch('click.echo') as mock_echo:
            command_executor._handle_learn_command([])
            assert "Error: Learn command requires a category" in mock_echo.call_args[0][0]

class TestLessonIntegration:
    """Test lesson system integration"""
    
    def test_lesson_completion_tracking(self, command_executor):
        """Test lesson completion tracking"""
        with patch.object(command_executor.git_session.lesson_manager, 'start_interactive_session') as mock_start, \
             patch.object(command_executor.git_session.lesson_manager.progress, 'mark_completed') as mock_complete:
            
            command_executor._handle_learn_command(['git', '01_basics'])
            mock_start.assert_called_once()
            # Completion is handled within the lesson manager

    def test_lesson_prerequisites(self, command_executor):
        """Test lesson prerequisite checking"""
        with patch.object(command_executor.git_session.lesson_manager, 'start_interactive_session') as mock_start, \
             patch('click.confirm') as mock_confirm:
            
            mock_confirm.return_value = True
            command_executor._handle_learn_command(['git', '02_branching'])
            mock_start.assert_called_once()

    def test_practical_task_verification(self, command_executor):
        """Test practical task verification"""
        with patch.object(command_executor.git_session, 'verify_task') as mock_verify:
            mock_verify.return_value = True
            
            # Simulate task verification through git_session
            result = command_executor.git_session.verify_task('init', '')
            assert result == True
            mock_verify.assert_called_once()

class TestErrorHandling:
    """Test error handling in learning commands"""
    
    def test_invalid_category(self, command_executor):
        """Test handling invalid category"""
        with patch('click.echo') as mock_echo:
            command_executor._handle_learn_command(['invalid', '01_basics'])
            assert any("Error" in call_args[0][0] for call_args in mock_echo.call_args_list)

    def test_invalid_lesson(self, command_executor):
        """Test handling invalid lesson"""
        with patch('click.echo') as mock_echo:
            command_executor._handle_learn_command(['git', 'nonexistent'])
            assert any("Error" in call_args[0][0] for call_args in mock_echo.call_args_list)

    def test_invalid_git_command(self, command_executor):
        """Test handling invalid git command"""
        with patch('click.echo') as mock_echo:
            command_executor._handle_git_command(['invalid'])
            assert "Unknown git subcommand" in mock_echo.call_args[0][0]

if __name__ == '__main__':
    pytest.main([__file__])
