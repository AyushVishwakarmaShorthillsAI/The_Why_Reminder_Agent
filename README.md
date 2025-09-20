## Goal Achiever Helper

An agentic CLI app built with Google ADK that helps users set and manage weekly goals, capture daily notes, and stay motivated by reconnecting with their "Why". It uses Gemini models via the Google AI API.

### Features
- **Root agent (`goal_achiever_helper`)**: Routes user intents to specialized subagents.
- **Subagents**
  - `user_greeter_agent`: Greets, collects `user_name` and `the_Why` via `Info_Collector(name, the_why)`.
  - `weekly_goal_manager_agent`: Manages weekly goals via `Add_goal(goal_description)`, `Show_goals()`, `Delete_goal(index)`.
  - `daily_note_taker_agent`: Saves notes via `Daily_Reflection_Taker(notes)` and displays them via `Show_All_Daily_Notes()`.
  - `why_reminder_agent`: Reminds users of their motivation (routes on negative sentiment).

### Requirements
- Python 3.11+
- A Google AI (Gemini) API key

Recommended packages (if you are setting up from scratch):
```bash
pip install google-adk google-generativeai python-dotenv
```

### Configure the Gemini API key
1. Create a `.env` file in the project root with:
```bash
GEMINI_API_KEY=YOUR_API_KEY_HERE
```
2. The app reads `GEMINI_API_KEY` and configures the client in `main.py` using `google.generativeai.configure(...)`.

### Run the app
```bash
python main.py
```

Type messages at the `You:` prompt. To end, press Ctrl+C or send EOF depending on your shell.

### Quickstart flow (example)
1) Introduce yourself and your "Why":
```
My name is Ayush and I want to upskill to get a better job
```
2) Add weekly goals:
```
Add goal: Learn Python programming
Add goal: Build a portfolio website
show my goals
```
3) Take and view daily notes:
```
take a daily note
Today I started learning Python basics and completed 3 exercises
show my daily notes
```
4) Delete a goal:
```
delete goal 2
show goals
```

### Project structure (key files)
- `main.py`: App entrypoint; configures Gemini; creates session; runs the loop.
- `utils.py`: Helpers for calling the agent, printing state, and saving interaction history.
- `goal_achiever_helper/agent.py`: Root agent and routing.
- `goal_achiever_helper/subagents/*`: Subagent definitions and their tools.
  - `user_greeter_agent/tools.py`: `Info_Collector` stores `user_name` and `the_Why`.
  - `weekly_goal_manager_agent/tools.py`: `Add_goal`, `Show_goals`, `Delete_goal`.
  - `daily_note_taker_agent/tools.py`: `Daily_Reflection_Taker`, `Show_All_Daily_Notes`.

### Troubleshooting
- **Missing key inputs argument (API key)**: Ensure `.env` has `GEMINI_API_KEY` and it’s non-empty.
- **Pydantic validation errors**: Agent names must be valid identifiers; tools must be callable (pass function refs, not strings).
- **State not updating**: After modifying nested structures (lists/dicts) in tools, update `tool_context.actions.state_delta[...]` with the new value.
- **Async/await issues**: Await all `session_service` calls and any async utilities.
- **EOFError when piping input**: Normal if the process reaches end of piped input; provide enough lines or run interactively.

### License
This project is provided as-is for learning and experimentation.

