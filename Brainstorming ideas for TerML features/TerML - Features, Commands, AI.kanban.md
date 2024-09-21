## Features
- Explain - get clear explanation of terminal outputs  
- Suggest - Receive helpful command suggestions based on your command history.  
- Debug - Output returned an error? Analyze and debug whether you entered the command right, or if there is a deeper issue with your system.  
- Chat - Quick chat sessions for termainal and programming related questions. “What is the command for <Action>?” Or “How can I create multiple files in different directories in a single command?"  
- Auto - Automated command suggestions for project setups, or other tedious tasks needed to be done, asks for human approval before executing commands.  
- Summarize - Get a summary of the contents of a file or directory, or files in a directory, etc.  
- Generate - Create new project structures with predefined templates  
- Analyze - Perform code analysis and receive AI- Powered improvement suggestions.  
- Test - Generate unit tests for your project  
- Deps - Let AI manage your project dependencies  
- AI integration - TerML is made to be installed into your global PATH for terminal usage, to be able to continue to help you after creating different virtual environmemnts, however you can choose to only install it in a single venv.  

## Commands
- $ terml explain  
- $ terml suggest  
- $ terml debug  
- $ terml chat -q  
- $ terml auto —with-user  
- $ terml summarize [path]  
- $ terml generate [project_type] [project_name]  
- $ terml analyze [/path/to/project]  
- $ terml test [path/to/project]  
- $ terml deps [subcommand] [args]  
  $ terml deps list - list of current dependencies and their versions]
  $ terml deps update - updates all dependences to their latest versions
  $ terml deps add [name of dependency] - installs a dependency library to the project
  $ terml deps remove [name of dependency] - removes a depencendy library from the project 

## AI Assistance Roadmap
- Currently created to natively use Anthropic Claude 3.5 Sonnet (current version) via API key.  
- Would like to expand AI options, openrouter, huggingface, mistral, etc.  
- Possible submission for the OpenAI strawberry o1 model hackathon  