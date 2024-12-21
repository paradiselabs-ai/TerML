import pytest
from unittest.mock import patch, MagicMock, mock_open
import subprocess
from terml.git_helper import (
    analyze_git_state,
    provide_git_guidance,
    get_quick_git_help,
    GitLearningSession
)

# Mock subprocess responses
GIT_REPO_EXISTS = MagicMock(returncode=0)
GIT_REPO_NOT_EXISTS = MagicMock(side_effect=subprocess.CalledProcessError(128, 'git'))
GIT_CLEAN_STATUS = MagicMock(stdout="")
GIT_MODIFIED_STATUS = MagicMock(stdout=" M file1.py\nM  file2.py\n?? file3.py")
GIT_BRANCH_MAIN = MagicMock(stdout="main")

def test_analyze_git_state_not_repo():
    """Test analyzing a non-git repository"""
    with patch('subprocess.run', return_value=GIT_REPO_NOT_EXISTS):
        state, details = analyze_git_state()
        assert state == "Not a git repository"
        assert len(details) == 1
        assert "not a git repository" in details[0].lower()

def test_analyze_git_state_clean():
    """Test analyzing a clean git repository"""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = [GIT_REPO_EXISTS, GIT_CLEAN_STATUS, GIT_BRANCH_MAIN]
        state, details = analyze_git_state()
        assert state == "Clean"
        assert len(details) == 2
        assert "clean" in details[1].lower()
        assert "main" in details[0]

def test_analyze_git_state_changes():
    """Test analyzing a git repository with changes"""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = [GIT_REPO_EXISTS, GIT_MODIFIED_STATUS, GIT_BRANCH_MAIN]
        state, details = analyze_git_state()
        assert state == "Changes present"
        assert len(details) == 4  # branch + modified + staged + untracked
        assert any("modified" in d.lower() for d in details)
        assert any("staged" in d.lower() for d in details)
        assert any("untracked" in d.lower() for d in details)

def test_provide_git_guidance_not_repo():
    """Test guidance for non-git repository"""
    guidance = provide_git_guidance("Not a git repository", ["Not a git repository"])
    assert "git init" in guidance.lower()

def test_provide_git_guidance_clean():
    """Test guidance for clean repository"""
    guidance = provide_git_guidance("Clean", ["Working directory clean"])
    assert "clean" in guidance.lower()
    assert any(cmd in guidance.lower() for cmd in ["pull", "branch", "checkout"])

def test_provide_git_guidance_changes():
    """Test guidance for repository with changes"""
    details = [
        "Currently on branch 'main'",
        "2 file(s) modified",
        "1 file(s) staged for commit",
        "1 untracked file(s)"
    ]
    guidance = provide_git_guidance("Changes present", details)
    assert "git add" in guidance.lower()
    assert "git commit" in guidance.lower()
    assert "status" in guidance.lower()

def test_get_quick_git_help():
    """Test quick git help generation"""
    help_text = get_quick_git_help()
    common_commands = ["init", "clone", "add", "commit", "push", "pull", "branch", "status"]
    for cmd in common_commands:
        assert cmd in help_text.lower()

class TestGitLearningSession:
    """Test GitLearningSession functionality"""
    
    @pytest.fixture
    def session(self):
        """Create a GitLearningSession instance"""
        return GitLearningSession()

    def test_initialization(self, session):
        """Test session initialization"""
        assert session.lesson_manager is not None
        assert session.common_questions is not None
        assert len(session.common_questions) > 0

    @patch('click.echo')
    def test_start_lesson(self, mock_echo, session):
        """Test starting a lesson"""
        with patch.object(session.lesson_manager, 'start_interactive_session') as mock_start:
            session.start_lesson()
            mock_start.assert_called_once_with('git', '01_basics')
            
            # Test with specific lesson
            session.start_lesson('02_advanced')
            mock_start.assert_called_with('git', '02_advanced')

    @patch('click.echo')
    def test_show_available_lessons(self, mock_echo, session):
        """Test showing available lessons"""
        with patch.object(session.lesson_manager, 'show_category_progress') as mock_show:
            session.show_available_lessons()
            mock_show.assert_called_once_with('git')

    @patch('click.echo')
    @patch('click.prompt')
    def test_start_quick_qa(self, mock_prompt, mock_echo, session):
        """Test quick Q&A session"""
        # Test exit command
        mock_prompt.return_value = 'exit'
        session.start_quick_qa()
        assert mock_echo.call_count >= 2  # Start message + end message
        
        # Test git command question
        mock_prompt.side_effect = ['init', 'exit']
        session.start_quick_qa()
        echo_calls = [call[0][0] for call in mock_echo.call_args_list]
        assert any('init' in str(call).lower() for call in echo_calls)
        
        # Test status question with repository context
        with patch('terml.git_helper.analyze_git_state') as mock_analyze:
            mock_analyze.return_value = ("Changes present", ["2 files modified"])
            mock_prompt.side_effect = ['status', 'exit']
            session.start_quick_qa()
            echo_calls = [call[0][0] for call in mock_echo.call_args_list]
            assert any('modified' in str(call).lower() for call in echo_calls)

    def test_verify_task(self, session):
        """Test task verification"""
        # Test git init verification
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = GIT_REPO_EXISTS
            assert session.verify_task('init', '')
            
            mock_run.side_effect = subprocess.CalledProcessError(128, 'git')
            assert not session.verify_task('init', '')
        
        # Test git add verification
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = GIT_MODIFIED_STATUS
            assert session.verify_task('add', '')
            
            mock_run.return_value = GIT_CLEAN_STATUS
            assert not session.verify_task('add', '')
        
        # Test git commit verification
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(stdout="Initial commit")
            assert session.verify_task('commit', '')
            
            mock_run.side_effect = subprocess.CalledProcessError(128, 'git')
            assert not session.verify_task('commit', '')

if __name__ == '__main__':
    pytest.main([__file__])
