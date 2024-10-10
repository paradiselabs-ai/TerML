import click
from . import config

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
            "summarize": self._summarize
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