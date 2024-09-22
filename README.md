# TerML - AI-powered Terminal Assistant

TerML is an AI-powered terminal assistant that integrates seamlessly with your command-line interface. It provides explanations, suggestions, and assistance for various terminal tasks, helping users better understand and utilize their terminal environment. Recently updated to enhance compatibility and performance, TerML now offers even more robust AI-powered features.

## Features

- **Explain**: Get clear explanations of terminal outputs
- **Suggest**: Receive helpful command suggestions based on your command history
- **Debug**: Analyze and debug command execution issues
- **Chat**: Quick chat sessions for terminal and programming-related questions
- **Auto**: Automated command suggestions for project setup with user approval
- **Summarize**: Get a summary of the contents of a file or directory
- **Generate**: Create new project structures with predefined templates
- **Analyze**: Perform code analysis and receive AI-powered improvement suggestions
- **Test**: Generate unit tests for your project
- **Deps**: Manage project dependencies
- **AI Integration**: Enhanced AI capabilities for more accurate and helpful responses

## Installation

To install TerML, make sure you have Python 3.7+ installed, then run:

```shell
  pip install terml
```

## Configuration

TerML requires an Anthropic API key to function. Set your API key as an environment variable:

```shell
  export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

TerML integrates into your existing terminal workflow. Here are the main commands:

- `terml explain`: Explain the last command output

```shell
  $ ls -la
  [output]
  $ terml explain
  TerML: [Explanation of the 'ls -la' command output]
```

- `terml suggest`: Get a suggestion for the next command

```shell
  $ terml suggest
  TerML suggests: [Suggested command based on your command history]
```

- `terml debug`: Debug the last command execution

```shell

  $ [command with error]
  [error output]
  $ terml debug
  TerML: [Analysis of the error and suggested fix]
```

- `terml chat -q`: Start a quick chat session with TerML

```shell
  $ terml chat -q
  TerML: Welcome to quick chat mode. Type 'exit' to leave.
  You: How do I find files larger than 1GB?
  TerML: [Explanation of how to find large files]
  You: exit
  TerML: Exiting chat mode.
```

- `terml auto --with-user`: Automatically suggest and run commands with user approval

```shell
  $ terml auto --with-user
  TerML: What are you trying to achieve?
  You: Set up a new React project
  TerML: [Suggests a series of commands to set up a React project, asking for approval before each]
```

- `terml summarize [path]`: Get a summary of the contents of a file or directory

```shell
  $ terml summarize /path/to/file.py
  TerML Summary: [Summary of the contents of file.py]

  $ terml summarize /path/to/directory
  TerML Summary: [Overview of the files and their purposes in the directory]
```

- `terml generate [project_type] [project_name]`: Generate a new project structure

```shell
  $ terml generate python my_new_project
  Project 'my_new_project' of type 'python' has been generated at: /path/to/my_new_project
```

- `terml analyze [path]`: Analyze code and get improvement suggestions

```shell  
  $ terml analyze /path/to/project
  [Code analysis summary]
  TerML AI Suggestions: [AI-powered suggestions for code improvements]
```

- `terml test [path]`: Generate unit tests for your project

```shell
  $ terml test /path/to/project
  Generated 5 test files:
    - /path/to/project/tests/test_module1.py
    - /path/to/project/tests/test_module2.py
    ...
  TerML AI Test Improvement Suggestions: [AI-powered suggestions for test improvements
  ```

- `terml deps [subcommand] [args]`: Manage project dependencies
  
```shell
  $ terml deps list
  [List of current dependencies and their versions]

  $ terml deps update
  [Update all dependencies to their latest versions]

  $ terml deps add requests
  [Add the 'requests' library to the project]

  $ terml deps remove requests
  [Remove the 'requests' library from the project]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

## Recent Updates

- Enhanced compatibility with the latest versions of httpx and httpcore
- Improved AI integration for more accurate and helpful responses
- Updated project structure and dependencies
- All tests passing with the latest changes
- Improved error handling and logging
- Updated documentation to reflect recent changes
- Refactored code for better maintainability and performance
- Enhanced test coverage for core functionalities
- Implemented more robust input validation and error handling
- Optimized AI model interactions for faster response times

## Roadmap

We're constantly working to improve TerML. Here are some features we're planning to implement:

- Integration with more AI models for enhanced capabilities
- Support for custom project templates
- Enhanced code analysis and refactoring suggestions
- Improved test generation with coverage analysis
- Integration with popular version control systems
- Expansion of language support for code analysis and generation
- Implementation of a plugin system for community-contributed features
- Enhanced natural language processing for more intuitive interactions
- A possible environment for prompt engineering and fine-tuning other AI models.

Stay tuned for these exciting updates!

## Changelog

For a detailed list of changes in each version, please refer to the [CHANGELOG.md](CHANGELOG.md) file.

## Security

We take the security of TerML seriously. If you discover any security-related issues, please email <paradiselabs.ai@gmail.com> and in the subject line please put "TerML Security" instead of using the issue tracker.

## Acknowledgements

TerML wouldn't be possible without the amazing open-source community. We'd like to thank all the contributors and maintainers of the libraries we use.

Special thanks to Anthropic for providing the powerful AI models that drive TerML's intelligence.

## Paradise Labs

Paradise Labs is a pre-seed AI Startup building next-gen AI applications. We have no shortage of ideas and our flagship product has not even been revealed, only hinted at on X/twitter [https://x.com/paradiselabs_ai] and our github is [http://github.com/paradiselabs_ai]  *yes, that is me*, is currently looking for a co-founder, and has a chance to win a huge hackathon with OpenAI's newest models o1 series. The winner will recieve a fast track for making their startup a reality and finding funding, customers, a community, etc.

I am building a new framework sort of like the web development version of langchain + autogen and wrapped it in a GUI as a for getting autonomous multi-agent groups of AI to collaborate on, and create, and even maintain and keep updated on the backend (or even suggest frontend changes!) websites for small to big companies, to enterprises. (there will be a tiered price for features and enterprise features).

Forget about those Wix and WordPress AI site template builders. This new framework (which should get an MVP release within the next couple of days) will build a website for you literally by using advanced NLP and prompt engineering all streamlined in an easily usable, uncomplicated GUI, for describing each feature to the Agents as they go. You will watch your ideas quickly come to life from an inkling of an idea to a fully deployed, unique and purposeful, not to mention practical, website. You can scale it's autonomy and creativity, and they are trained on making a passive income from the site as a priority and using best SEO, Marketing Analytics, Predictive models, and more! There will be hosting options, domain names, self hosting, and everything in between!

Please reach out to [paradiselabs.ai@gmail.com] if you are interested in joining me at ParadiseLabs and making my startup a reality! At the very least, if interested in joinging this hackathon on my team, you an do so [https://lablab.ai/event/strawberry-reasoning-with-o1/paradiselabs] (I will have a legitimate website up in a few days as well)
