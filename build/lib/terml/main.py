import sys
import os
import click
from dotenv import load_dotenv
from .terminal_handler import TerminalHandler
from .ai_integration import AIIntegration
from .commands import CommandExecutor
from . import config

class TerML:
    def __init__(self):
        load_dotenv()
        self.terminal_handler = TerminalHandler(max_history=config.MAX_HISTORY)
        self.ai_integration = AIIntegration()
        self.command_executor = CommandExecutor(self.terminal_handler, self.ai_integration)

    def run_command(self, command):
        return self.command_executor.execute(command)

def print_welcome_message():
    click.echo(f"Welcome to TerML - Your AI-powered Terminal Assistant!")
    click.echo(f"Type '{config.TERML_PREFIX} help' to see available commands.")
    click.echo(f"Type 'exit' to quit TerML.")

@click.command()
@click.argument('command', nargs=-1)
def cli(command):
    """TerML - AI-powered Terminal Assistant"""
    terml = TerML()
    
    if not command:
        print_welcome_message()
        while True:
            try:
                user_input = click.prompt("TerML", prompt_suffix="> ")
                if user_input.lower() == 'exit':
                    click.echo("Goodbye!")
                    break
                result = terml.run_command(user_input)
                if result:
                    click.echo(result)
            except click.exceptions.Abort:
                click.echo("\nGoodbye!")
                break
            except Exception as e:
                click.echo(f"An error occurred: {str(e)}")
    else:
        result = terml.run_command(' '.join(command))
        if result:
            click.echo(result)

if __name__ == "__main__":
    cli()