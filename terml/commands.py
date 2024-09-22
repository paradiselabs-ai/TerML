import click
import os
from . import config
from .project_templates import create_project_structure, list_available_templates
from .code_analyzer import analyze_project, get_analysis_summary
from .test_generator import generate_and_write_tests
from .dependency_manager import get_dependency_info, update_dependencies, add_dependency, remove_dependency

class CommandExecutor:
    def __init__(self, terminal_handler, ai_integration):
        self.terminal_handler = terminal_handler
        self.ai_integration = ai_integration

    def execute(self, command):
        parts = command.split()
        if not parts or parts[0].lower() != config.TERML_PREFIX:
            return

        subcommand = parts[1].lower() if len(parts) > 1 else "help"
        args = parts[2:]

        command_map = {
            "explain": self._explain,
            "suggest": self._suggest,
            "chat": self._chat,
            "debug": self._debug,
            "auto": self._auto,
            "summarize": self._summarize,
            "generate": self._generate_project,
            "analyze": self._analyze_code,
            "test": self._generate_tests,
            "deps": self._manage_dependencies
        }

        if subcommand in command_map:
            command_map[subcommand](args)
        else:
            click.echo(f"Unknown TerML command. Use 'terml --help' for available commands.")

    def _explain(self, args):
        last_output = self.terminal_handler.get_last_output()
        explanation = self.ai_integration.explain_output(last_output)
        click.echo(f"TerML: {explanation}")

    def _suggest(self, args):
        history = self.terminal_handler.get_formatted_history()
        suggestion = self.ai_integration.suggest_command(history)
        click.echo(f"TerML suggests: {suggestion}")

    def _chat(self, args):
        if not args or args[0] != "-q":
            click.echo("Error: The chat command requires the -q (quick) argument.")
            return
        click.echo("TerML: Welcome to quick chat mode. Type 'exit' to leave.")
        while True:
            user_input = click.prompt("You")
            if user_input.lower() == 'exit':
                click.echo("TerML: Exiting chat mode.")
                break
            response = self.ai_integration.chat_response(user_input)
            click.echo(f"TerML: {response}")

    def _debug(self, args):
        last_command = self.terminal_handler.get_last_command()
        last_output = self.terminal_handler.get_last_output()
        debug_info = self.ai_integration.debug_command(last_command, last_output)
        click.echo(f"TerML: {debug_info}")

    def _auto(self, args):
        if not args or args[0] != "--with-user":
            click.echo("Error: The auto command requires the --with-user argument for safety.")
            return
        click.echo("TerML: Entering auto mode. I'll suggest commands to help you set up your project.")
        goal = click.prompt("What are you trying to achieve?")
        tech_stack = click.prompt("What tech stack are you using?")
        while True:
            suggestion = self.ai_integration.generate_auto_commands(goal, tech_stack)
            click.echo(f"TerML suggests: {suggestion}")
            click.echo("This command will: [explanation of what the command does]")
            if click.confirm("Would you like to proceed?"):
                output, error = self.terminal_handler.execute_command(suggestion)
                click.echo(output)
                if error:
                    click.echo(f"Error: {error}")
            else:
                click.echo("Command skipped.")
            if not click.confirm("Continue auto mode?"):
                click.echo("TerML: Exiting auto mode.")
                break

    def _summarize(self, args):
        if not args:
            click.echo("Error: The summarize command requires a path argument.")
            return
        path = args[0]
        summary = self.ai_integration.summarize_contents(path)
        click.echo(f"TerML Summary: {summary}")

    def _generate_project(self, args):
        if len(args) != 2:
            click.echo("Error: The generate command requires two arguments: project type and project name.")
            click.echo(f"Available project types: {', '.join(list_available_templates())}")
            return
        project_type, project_name = args
        try:
            project_path = create_project_structure(project_type, project_name)
            click.echo(f"Project '{project_name}' of type '{project_type}' has been generated at: {project_path}")
        except ValueError as e:
            click.echo(f"Error: {str(e)}")
            click.echo(f"Available project types: {', '.join(list_available_templates())}")

    def _analyze_code(self, args):
        if not args:
            click.echo("Error: The analyze command requires a path argument.")
            return
        path = args[0]
        if not os.path.exists(path):
            click.echo(f"Error: The path '{path}' does not exist.")
            return
        issues = analyze_project(path)
        summary = get_analysis_summary(issues)
        click.echo(summary)
        
        # AI-powered suggestions for improvements
        if issues:
            suggestions = self.ai_integration.suggest_code_improvements(summary)
            click.echo("\nTerML AI Suggestions:")
            click.echo(suggestions)

    def _generate_tests(self, args):
        if not args:
            click.echo("Error: The test command requires a path argument.")
            return
        path = args[0]
        if not os.path.exists(path):
            click.echo(f"Error: The path '{path}' does not exist.")
            return
        if not os.path.isdir(path):
            click.echo(f"Error: The path '{path}' is not a directory.")
            return
        
        generated_tests = generate_and_write_tests(path)
        click.echo(f"Generated {len(generated_tests)} test files:")
        for test_file in generated_tests:
            click.echo(f"  - {test_file}")
        
        # AI-powered suggestions for test improvements
        suggestions = self.ai_integration.suggest_test_improvements(path)
        click.echo("\nTerML AI Test Improvement Suggestions:")
        click.echo(suggestions)

    def _manage_dependencies(self, args):
        if not args:
            click.echo("Error: The deps command requires a subcommand (list, update, add, remove).")
            return
        
        subcommand = args[0]
        project_path = os.getcwd()

        if subcommand == "list":
            dep_info = get_dependency_info(project_path)
            click.echo(f"Total dependencies: {dep_info['total_dependencies']}")
            click.echo(f"Outdated dependencies: {dep_info['outdated_dependencies']}")
            click.echo("\nCurrent dependencies:")
            for dep, version in dep_info['dependencies'].items():
                click.echo(f"  - {dep}: {version}")
            if dep_info['outdated']:
                click.echo("\nOutdated dependencies:")
                for dep in dep_info['outdated']:
                    click.echo(f"  - {dep['name']}: {dep['version']} (Latest: {dep['latest_version']})")

        elif subcommand == "update":
            click.echo("Updating dependencies...")
            update_dependencies(project_path)
            click.echo("Dependencies updated successfully.")

        elif subcommand == "add":
            if len(args) < 2:
                click.echo("Error: Please specify the dependency to add.")
                return
            dependency = args[1]
            version = args[2] if len(args) > 2 else None
            click.echo(f"Adding dependency: {dependency}")
            add_dependency(project_path, dependency, version)
            click.echo(f"Dependency {dependency} added successfully.")

        elif subcommand == "remove":
            if len(args) < 2:
                click.echo("Error: Please specify the dependency to remove.")
                return
            dependency = args[1]
            click.echo(f"Removing dependency: {dependency}")
            remove_dependency(project_path, dependency)
            click.echo(f"Dependency {dependency} removed successfully.")

        else:
            click.echo(f"Unknown deps subcommand: {subcommand}")
            click.echo("Available subcommands: list, update, add, remove")