import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import json
from terml.lesson_system import LessonCategory, LessonProgress, Lesson, LessonManager

# Test data
SAMPLE_LESSON = {
    'title': 'Test Lesson',
    'description': 'Test Description',
    'prerequisites': [],
    'steps': [
        {
            'title': 'Step 1',
            'content': 'Step content',
            'exercise': 0
        }
    ],
    'exercises': [
        {
            'question': 'Test question?',
            'answer': 'test',
            'explanation': 'Test explanation'
        }
    ]
}

def test_lesson_category_validation():
    """Test lesson category validation"""
    # Valid categories
    assert LessonCategory.is_valid_category('git')
    assert LessonCategory.is_valid_category('shell')
    assert LessonCategory.is_valid_category('network')
    assert LessonCategory.is_valid_category('tools')
    
    # Invalid categories
    assert not LessonCategory.is_valid_category('invalid')
    assert not LessonCategory.is_valid_category('')
    assert not LessonCategory.is_valid_category(None)

def test_lesson_category_names():
    """Test lesson category names and descriptions"""
    categories = LessonCategory.get_categories()
    
    assert 'git' in categories
    assert 'shell' in categories
    assert 'network' in categories
    assert 'tools' in categories
    
    assert 'Git' in categories['git']['name']
    assert 'Shell' in categories['shell']['name']
    assert 'Network' in categories['network']['name']
    assert 'Package' in categories['tools']['name']

@pytest.fixture
def mock_progress_file(tmp_path):
    """Create a temporary progress file"""
    progress_file = tmp_path / "progress.json"
    return progress_file

def test_lesson_progress_new(mock_progress_file):
    """Test creating new progress tracking"""
    progress = LessonProgress(mock_progress_file)
    assert progress.data == {}
    
    # Mark a lesson as completed
    progress.mark_completed('git', '01_basics')
    assert progress.is_completed('git', '01_basics')
    assert not progress.is_completed('git', 'nonexistent')
    
    # Verify saved data
    assert mock_progress_file.exists()
    saved_data = json.loads(mock_progress_file.read_text())
    assert saved_data['git']['01_basics']['completed']

def test_lesson_progress_existing(mock_progress_file):
    """Test loading existing progress"""
    # Create existing progress file
    initial_data = {
        'git': {'01_basics': {'completed': True}},
        'shell': {'01_navigation': {'completed': False}}
    }
    mock_progress_file.write_text(json.dumps(initial_data))
    
    progress = LessonProgress(mock_progress_file)
    assert progress.is_completed('git', '01_basics')
    assert not progress.is_completed('shell', '01_navigation')
    assert not progress.is_completed('nonexistent', 'lesson')

def test_lesson_initialization():
    """Test lesson initialization and properties"""
    lesson = Lesson('git', '01_basics', SAMPLE_LESSON)
    
    assert lesson.category == 'git'
    assert lesson.lesson_id == '01_basics'
    assert lesson.title == 'Test Lesson'
    assert lesson.description == 'Test Description'
    assert len(lesson.steps) == 1
    assert len(lesson.exercises) == 1
    assert lesson.current_step == 0
    assert not lesson.completed

def test_lesson_progression():
    """Test lesson step progression"""
    lesson = Lesson('git', '01_basics', SAMPLE_LESSON)
    
    # Get first step
    step = lesson.get_next_step()
    assert step['title'] == 'Step 1'
    assert lesson.current_step == 1
    
    # No more steps
    assert lesson.get_next_step() is None
    assert lesson.completed

def test_lesson_answer_validation():
    """Test exercise answer validation"""
    lesson = Lesson('git', '01_basics', SAMPLE_LESSON)
    
    # Correct answer
    is_correct, feedback = lesson.validate_answer(0, 'test')
    assert is_correct
    assert feedback == 'Test explanation'
    
    # Wrong answer
    is_correct, feedback = lesson.validate_answer(0, 'wrong')
    assert not is_correct
    assert feedback == 'Test explanation'
    
    # Case insensitive
    is_correct, feedback = lesson.validate_answer(0, 'TEST')
    assert is_correct
    
    # Invalid step index
    is_correct, feedback = lesson.validate_answer(999, 'test')
    assert not is_correct
    assert "No exercise in this step" in feedback

@pytest.fixture
def mock_lesson_files(tmp_path):
    """Create mock lesson files"""
    lessons_dir = tmp_path / "lessons"
    lessons_dir.mkdir()
    
    # Create git lessons directory
    git_dir = lessons_dir / "git"
    git_dir.mkdir()
    
    # Create a lesson file
    lesson_file = git_dir / "01_basics.json"
    lesson_file.write_text(json.dumps(SAMPLE_LESSON))
    
    return lessons_dir

def test_lesson_manager(mock_lesson_files):
    """Test lesson manager functionality"""
    manager = LessonManager(str(mock_lesson_files))
    
    # Test getting available lessons
    lessons = manager.get_available_lessons()
    assert 'git' in lessons
    assert len(lessons['git']) == 1
    assert lessons['git'][0]['id'] == '01_basics'
    
    # Test loading specific lesson
    lesson = manager.load_lesson('git', '01_basics')
    assert lesson is not None
    assert lesson.title == 'Test Lesson'
    
    # Test invalid category/lesson
    assert manager.load_lesson('invalid', '01_basics') is None
    assert manager.load_lesson('git', 'nonexistent') is None

def test_lesson_manager_progress_tracking(mock_lesson_files):
    """Test lesson progress tracking in manager"""
    manager = LessonManager(str(mock_lesson_files))
    
    # Initially not completed
    lessons = manager.get_available_lessons()
    assert not lessons['git'][0]['completed']
    
    # Mark as completed through manager
    manager.progress.mark_completed('git', '01_basics')
    
    # Check updated status
    lessons = manager.get_available_lessons()
    assert lessons['git'][0]['completed']

if __name__ == '__main__':
    pytest.main([__file__])
