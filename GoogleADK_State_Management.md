## Google ADK – Sessions, State, and Interaction History

This document explains how sessions are created, how state is saved/updated, and how interaction history is recorded in this project. Examples use code from this repo.

### 1) Sessions
Google ADK manages conversations via sessions (user+session_id). We use the in-memory session service.

Creation happens in `main.py` when the app starts:

```python
# Simplified
temp_session = await session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,        # must be a string
    session_id=None,        # let ADK assign an ID
    state={                 # initial state
        "greeted": False,
        "daily_notes": [],
        "weekly_goals": [],
        "the_Why": "",
    },
)
SESSION_ID = temp_session.id
```

Retrieval uses `await session_service.get_session(app_name, user_id, session_id)`.

### 2) State – Reading, Writing, Persisting
Each session has a `state` (a dict). Tools and agents read from it to decide what to do. When you modify state in a tool, you must persist changes by writing to `tool_context.actions.state_delta`.

Why? Because ADK uses a delta-based persistence model; mutating a nested object (like appending to a list) does not automatically persist unless you set the corresponding key in `state_delta`.

#### Example A: Append to a list (Daily Notes)
`goal_achiever_helper/subagents/daily_note_taker_agent/tools.py`
```python
def Daily_Reflection_Taker(notes: str, tool_context: ToolContext):
    date_str = datetime.now().strftime("%Y-%m-%d")
    if "daily_notes" not in tool_context.state:
        tool_context.state["daily_notes"] = []
    tool_context.state["daily_notes"].append({"date": date_str, "note": notes})
    # CRITICAL: persist the updated list
    tool_context.actions.state_delta["daily_notes"] = tool_context.state["daily_notes"]
    return f"Your reflection for {date_str} has been saved."
```

#### Example B: Add/Delete items (Weekly Goals)
`goal_achiever_helper/subagents/weekly_goal_manager_agent/tools.py`
```python
def Add_goal(goal_description: str, tool_context: ToolContext):
    if "weekly_goals" not in tool_context.state:
        tool_context.state["weekly_goals"] = []
    tool_context.state["weekly_goals"].append({
        "description": goal_description,
        "start_date": datetime.now().strftime("%Y-%m-%d"),
    })
    # persist
    tool_context.actions.state_delta["weekly_goals"] = tool_context.state["weekly_goals"]

def Delete_goal(index: int, tool_context: ToolContext):
    goals = tool_context.state.get("weekly_goals", [])
    if 1 <= index <= len(goals):
        del goals[index - 1]
        tool_context.actions.state_delta["weekly_goals"] = goals
        return "Deleted."
    return "No goal at that index."
```

#### Example C: Save scalar values (User name and Why)
`goal_achiever_helper/subagents/user_greeter_agent/tools.py`
```python
def Info_Collector(name: str, the_why: str, tool_context: ToolContext):
    tool_context.state["user_name"] = name
    tool_context.state["the_Why"] = the_why
    # persist scalars
    tool_context.actions.state_delta["user_name"] = name
    tool_context.actions.state_delta["the_Why"] = the_why
    return "Saved your name and motivation."
```

### When to write to state vs. state_delta?
- Read values from `tool_context.state`.
- After you change something (especially nested types: list/dict), ALWAYS mirror the final value into `tool_context.actions.state_delta["key"]` for persistence.
- For scalars (str/int/bool), also set `state_delta["key"] = new_value` to persist.

## Two persistence paths (important)
There are two valid ways to persist state changes, used in different places:

- Inside tools (preferred for tool-side writes): set `tool_context.actions.state_delta["key"] = value`. This is atomic within the tool execution and is how ADK expects tools to persist changes.
- Outside tools (app code): fetch → modify → write back the entire state using `session_service.create_session(app_name, user_id, session_id, state=updated_state)`. With the in-memory session service, calling `create_session` again with the same `session_id` acts like an upsert and replaces the stored state for that session (it does not start a new conversation because the `session_id` is unchanged).

Note on concurrency: the fetch-modify-write pattern can race if multiple writers act concurrently. Using `state_delta` inside a single tool run avoids that within the scope of that run.

### 3) Interaction History – What, Where, How
We keep a running history of user queries and agent responses in `state["interaction_history"]` for transparency and debugging.

Where is it saved? In `utils.py` via async helpers:
```python
async def update_interaction_history(session_service, app_name, user_id, session_id, entry):
    session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    interaction_history = session.state.get("interaction_history", [])
    entry.setdefault("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    interaction_history.append(entry)
    updated_state = session.state.copy()
    updated_state["interaction_history"] = interaction_history
    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id, state=updated_state)
```

How is it used?
- When a user sends input, we call `add_user_query_to_history(...)`.
- After the agent yields a final response, we call `add_agent_response_to_history(...)`.

Examples:
```python
await add_user_query_to_history(session_service, app_name, user_id, session_id, query)
...
await add_agent_response_to_history(session_service, app_name, user_id, session_id, agent_name, final_response_text)
```

### 4) Tool Signatures and Context
Google ADK injects `ToolContext` automatically into tools when the parameter is named `tool_context` and typed as `ToolContext`:
```python
def MyTool(arg1: str, tool_context: ToolContext):
    ...
```
This gives you access to `tool_context.state` and `tool_context.actions.state_delta`.

### 5) Practical Playbook
- To save a note: call `Daily_Reflection_Taker(notes)`.
- To list notes: call `Show_All_Daily_Notes()`.
- To add a goal: call `Add_goal(goal_description)`.
- To delete a goal: call `Delete_goal(index)`.
- To persist any changes: set `tool_context.actions.state_delta["key"] = updated_value`.

### 6) Common Pitfalls
- Mutating lists/dicts without updating `state_delta` → changes won’t persist.
- Passing tool names as strings in agents → pass function references.
- Agent names must be valid identifiers (no spaces).
- Missing `await` on async calls to session service → stale state/errors.

With these patterns, you can confidently read, save, and modify session state and track the full interaction history.

