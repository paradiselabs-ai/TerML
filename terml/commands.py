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

    def execute(self, command, retain_memory=False):
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
            command_map[subcommand](args, retain_memory)
        else:
            click.echo(f"Unknown TerML command. Use 'terml --help' for available commands.")

    # ... (other methods remain unchanged)

    def _auto(self, args, retain_memory=False):
        with_user = "--with-user" in args
        quick_mode = "-q" in args

        if not with_user and not quick_mode:
            click.echo("Error: The auto command requires either --with-user or -q argument for safety.")
            return

        if not with_user:
            click.echo("CAUTION! This can be dangerous and may damage your project or even your operating system!")
            click.echo("ParadiseLabs and Anthropic will not be responsible for any potential damage.")
            click.echo("Please use caution and keep watch over TerML in auto mode.")
            click.echo("Use CTRL + C to exit auto mode instantly at any time.")
            click.echo("Note: 'terml auto revert' will only revert the last command ran by TerML in auto mode.")
            if not click.confirm("Do you want to proceed?"):
                return

        click.echo("TerML: Entering auto mode. I'll suggest commands to help you set up your project.")
        goal = click.prompt("What are you trying to achieve?")
        tech_stack = click.prompt("What tech stack are you using?")

        if quick_mode:
            suggestions = self.ai_integration.generate_auto_commands(goal, tech_stack, max_commands=5)
            for suggestion in suggestions:
                click.echo(f"TerML suggests: {suggestion}")
                click.echo("This command will: [explanation of what the command does]")
                if with_user:
                    if not click.confirm("Would you like to proceed?"):
                        continue
                output, error = self.terminal_handler.execute_command(suggestion)
                click.echo(output)
                if error:
                    click.echo(f"Error: {error}")
            click.echo("TerML: Quick auto mode completed.")
        else:
            while True:
                suggestion = self.ai_integration.generate_auto_commands(goal, tech_stack, max_commands=1)[0]
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

    # ... (other methods remain unchanged)
