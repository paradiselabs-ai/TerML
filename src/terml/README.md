# TerML - AI-powered Terminal Assistant

TerML is an AI-powered terminal assistant that integrates seamlessly with your command-line interface. It provides explanations, suggestions, and assistance for various terminal tasks, helping users better understand and utilize their terminal environment.

## Features

- **Explain**: Get clear explanations of terminal outputs
- **Suggest**: Receive helpful command suggestions based on your command history
- **Debug**: Analyze and debug command execution issues
- **Chat**: Quick chat sessions for terminal and programming-related questions
- **Auto**: Automated command suggestions for project setup with user approval
- **Summarize**: Get a summary of the contents of a file or directory

## Installation

To install TerML, make sure you have Python 3.7+ installed, then run:

```
pip install terml
```

## Configuration

TerML requires an Anthropic API key to function. Set your API key as an environment variable:

```
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

TerML integrates into your existing terminal workflow. Here are the main commands:

- `terml explain`: Explain the last command output
  ```
  $ ls -la
  [output]
  $ terml explain
  TerML: [Explanation of the 'ls -la' command output]
  ```

- `terml suggest`: Get a suggestion for the next command
  ```
  $ terml suggest
  TerML suggests: [Suggested command based on your command history]
  ```

- `terml debug`: Debug the last command execution
  ```
  $ [command with error]
  [error output]
  $ terml debug
  TerML: [Analysis of the error and suggested fix]
  ```

- `terml chat -q`: Start a quick chat session with TerML
  ```
  $ terml chat -q
  TerML: Welcome to quick chat mode. Type 'exit' to leave.
  You: How do I find files larger than 1GB?
  TerML: [Explanation of how to find large files]
  You: exit
  TerML: Exiting chat mode.
  ```

- `terml auto --with-user`: Automatically suggest and run commands with user approval
  ```
  $ terml auto --with-user
  TerML: What are you trying to achieve?
  You: Set up a new React project
  TerML: [Suggests a series of commands to set up a React project, asking for approval before each]
  ```

- `terml summarize [path]`: Get a summary of the contents of a file or directory
  ```
  $ terml summarize /path/to/file.py
  TerML Summary: [Summary of the contents of file.py]

  $ terml summarize /path/to/directory
  TerML Summary: [Overview of the files and their purposes in the directory]
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.