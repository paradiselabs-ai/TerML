from . import config

class CommandExecutor:
    def __init__(self, terminal_handler, ai_integration):
        self.terminal_handler = terminal_handler
        self.ai_integration = ai_integration

    def execute(self, command):
        parts = command.split()
        if not parts or parts[0].lower() != config.TERML_PREFIX:
            output, error = self.terminal_handler.execute_command(command)
            print(output)
            if error:
                print(f"Error: {error}")
            return

        subcommand = parts[1].lower() if len(parts) > 1 else ""
        args = parts[2:]

        if subcommand == "explain":
            self._explain()
        elif subcommand == "suggest":
            self._suggest()
        elif subcommand == "chat":
            self._chat(args)
        elif subcommand == "debug":
            self._debug()
        elif subcommand == "auto":
            self._auto(args)
        else:
            print(f"Unknown TerML command. Type '{config.TERML_PREFIX} help' for available commands.")

    def _explain(self):
        last_output = self.terminal_handler.get_last_output()
        explanation = self.ai_integration.explain_output(last_output)
        print(explanation)

    def _suggest(self):
        history = self.terminal_handler.get_formatted_history()
        suggestion = self.ai_integration.suggest_command(history)
        print(f"Suggested command: {suggestion}")

    def _chat(self, args):
        if not args or args[0] != "-q":
            print(f"Error: The chat command requires the -q (quick) argument.")
            return
        print("Entering quick chat mode. Type ':q' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == ':q':
                print("Exiting chat mode.")
                break
            response = self.ai_integration.chat_response(user_input)
            print(f"TerML: {response}")

    def _debug(self):
        last_command = self.terminal_handler.get_last_command()
        last_output = self.terminal_handler.get_last_output()
        debug_info = self.ai_integration.debug_command(last_command, last_output)
        print(debug_info)

    def _auto(self, args):
        if not args or args[0] != "--with-user":
            print(f"Error: The auto command requires the --with-user argument for safety.")
            return
        print("Entering auto mode. TerML will suggest commands.")
        goal = input("What are you trying to achieve? ")
        tech_stack = input("What tech stack are you using? ")
        while True:
            suggestion = self.ai_integration.generate_auto_commands(goal, tech_stack)
            user_approval = input(f"TerML suggests: {suggestion}\nExecute this command? [y/N]: ")
            if user_approval.lower() == 'y':
                output, error = self.terminal_handler.execute_command(suggestion)
                print(output)
                if error:
                    print(f"Error: {error}")
            else:
                print("Command skipped.")
            if input("Continue auto mode? [y/N]: ").lower() != 'y':
                print("Exiting auto mode.")
                break