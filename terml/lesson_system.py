import os
import json
from typing import Dict, List, Optional, Any
import click
from pathlib import Path

class LessonCategory:
    """Defines available lesson categories and their descriptions"""
    CATEGORIES = {
        'git': {
            'name': 'Git Version Control',
            'description': 'Learn Git fundamentals and advanced workflows'
        },
        'shell': {
            'name': 'Shell Basics',
            'description': 'Master command-line navigation and file operations'
        },
        'network': {
            'name': 'Network Tools',
            'description': 'Learn essential networking commands and diagnostics'
        },
        'tools': {
            'name': 'Common Tools',
            'description': 'Explore package managers and system utilities'
        }
    }

    @classmethod
    def get_categories(cls) -> Dict[str, Dict[str, str]]:
        return cls.CATEGORIES

    @classmethod
    def is_valid_category(cls, category: str) -> bool:
        return category in cls.CATEGORIES

class LessonProgress:
    """Manages user progress through lessons"""
    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.data = self._load_progress()

    def _load_progress(self) -> Dict:
        if self.progress_file.exists():
            try:
                return json.loads(self.progress_file.read_text())
            except json.JSONDecodeError:
                return {}
        return {}

    def save_progress(self):
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self.progress_file.write_text(json.dumps(self.data, indent=2))

    def mark_completed(self, category: str, lesson: str):
        if category not in self.data:
            self.data[category] = {}
        self.data[category][lesson] = {'completed': True}
        self.save_progress()

    def is_completed(self, category: str, lesson: str) -> bool:
        return self.data.get(category, {}).get(lesson, {}).get('completed', False)

    def get_progress(self, category: str = None) -> Dict:
        if category:
            return self.data.get(category, {})
        return self.data

class Lesson:
    """Represents a single lesson with its content and state"""
    def __init__(self, category: str, lesson_id: str, content: Dict):
        self.category = category
        self.lesson_id = lesson_id
        self.title = content['title']
        self.description = content['description']
        self.prerequisites = content.get('prerequisites', [])
        self.steps = content['steps']
        self.current_step = 0
        self.exercises = content.get('exercises', [])
        self.practical_tasks = content.get('practical_tasks', [])

    def get_next_step(self) -> Optional[Dict]:
        if self.current_step >= len(self.steps):
            return None
        step = self.steps[self.current_step]
        self.current_step += 1
        return step

    def validate_answer(self, step_idx: int, answer: str) -> tuple[bool, str]:
        if 'exercise' not in self.steps[step_idx]:
            return False, "No exercise in this step"
        
        exercise = self.exercises[self.steps[step_idx]['exercise']]
        is_correct = answer.strip().lower() == exercise['answer'].strip().lower()
        feedback = exercise.get('explanation', '')
        return is_correct, feedback

class LessonManager:
    """Manages lesson loading, tracking, and interaction"""
    def __init__(self, lessons_dir: str = "lessons"):
        self.lessons_dir = Path(lessons_dir)
        self.progress = LessonProgress(self.lessons_dir / "progress.json")
        self.current_lesson = None

    def get_available_lessons(self, category: str = None) -> Dict[str, List[str]]:
        """Get all available lessons, optionally filtered by category"""
        result = {}
        categories = [category] if category else LessonCategory.CATEGORIES.keys()
        
        for cat in categories:
            cat_dir = self.lessons_dir / cat
            if not cat_dir.exists():
                continue
            
            lessons = []
            for lesson_file in cat_dir.glob('*.json'):
                try:
                    content = json.loads(lesson_file.read_text())
                    lessons.append({
                        'id': lesson_file.stem,
                        'title': content['title'],
                        'description': content['description'],
                        'completed': self.progress.is_completed(cat, lesson_file.stem)
                    })
                except (json.JSONDecodeError, KeyError):
                    continue
            
            if lessons:
                result[cat] = sorted(lessons, key=lambda x: x['id'])
        
        return result

    def load_lesson(self, category: str, lesson_id: str) -> Optional[Lesson]:
        """Load a specific lesson"""
        if not LessonCategory.is_valid_category(category):
            return None

        lesson_file = self.lessons_dir / category / f"{lesson_id}.json"
        if not lesson_file.exists():
            return None

        try:
            content = json.loads(lesson_file.read_text())
            self.current_lesson = Lesson(category, lesson_id, content)
            return self.current_lesson
        except (json.JSONDecodeError, KeyError):
            return None

    def start_interactive_session(self, category: str, lesson_id: str):
        """Start an interactive lesson session"""
        lesson = self.load_lesson(category, lesson_id)
        if not lesson:
            click.echo(f"Error: Lesson '{lesson_id}' not found in category '{category}'")
            return

        # Check prerequisites
        for prereq in lesson.prerequisites:
            if not self.progress.is_completed(prereq['category'], prereq['lesson']):
                if not click.confirm(f"⚠️  Prerequisite '{prereq['lesson']}' not completed. Continue anyway?"):
                    return

        click.echo(f"\n=== {lesson.title} ===")
        click.echo(f"Category: {LessonCategory.CATEGORIES[category]['name']}")
        click.echo(f"Description: {lesson.description}\n")

        try:
            while True:
                step = lesson.get_next_step()
                if not step:
                    click.echo("\n🎉 Congratulations! You've completed this lesson!")
                    self.progress.mark_completed(category, lesson_id)
                    break

                click.echo(f"\nStep {lesson.current_step}: {step['title']}")
                click.echo(step['content'])

                if 'exercise' in step:
                    while True:
                        answer = click.prompt("\nYour answer (or 'skip' to continue)")
                        if answer.lower() == 'skip':
                            break
                        
                        is_correct, feedback = lesson.validate_answer(lesson.current_step - 1, answer)
                        if is_correct:
                            click.echo(f"✅ Correct! {feedback}")
                            break
                        click.echo(f"❌ Not quite. {feedback}")

                if not click.confirm("\nContinue to next step?"):
                    click.echo("\nLesson progress saved. You can continue later.")
                    break

        except KeyboardInterrupt:
            click.echo("\nLesson interrupted. Progress saved.")

    def show_category_progress(self, category: str):
        """Display progress for a category"""
        if not LessonCategory.is_valid_category(category):
            click.echo(f"Error: Invalid category '{category}'")
            return

        lessons = self.get_available_lessons(category)
        if not lessons:
            click.echo(f"No lessons found in category '{category}'")
            return

        click.echo(f"\n=== {LessonCategory.CATEGORIES[category]['name']} ===")
        for lesson in lessons[category]:
            status = "✅" if lesson['completed'] else "⭕"
            click.echo(f"{status} {lesson['id']}: {lesson['title']}")
