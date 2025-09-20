from google.adk.tools import ToolContext
from datetime import datetime

def Add_goal(goal_description: str, tool_context: ToolContext):
    """
    Tool to add a new goal to the user's list of goals in session state.
    Each goal will have a description and a start_date.
    """

    # Initialize goals list if not present
    if "weekly_goals" not in tool_context.state:
        tool_context.state["weekly_goals"] = []

    # Create structured goal
    new_goal = {
        "description": goal_description,
        "start_date": datetime.now().strftime("%Y-%m-%d")
    }

    # Append the new goal
    tool_context.state["weekly_goals"].append(new_goal)

    # Explicitly update the state delta to ensure persistence
    tool_context.actions.state_delta["weekly_goals"] = tool_context.state["weekly_goals"]

    return (
        f"Your goal has been added:\n"
        f"📌 {goal_description}\n"
        f"🗓️ Start Date: {new_goal['start_date']}"
    )

def Show_goals(tool_context: ToolContext):
    """
    Tool to display the user's current week's goals.
    """

    goals = tool_context.state.get("weekly_goals", [])

    if not goals:
        return "You don’t have any goals yet. Try adding one!"

    response = ["Here are your current goals:"]
    for idx, goal in enumerate(goals, start=1):
        response.append(
            f"{idx}. 📌 {goal['description']} (Started on {goal['start_date']})"
        )

    return "\n".join(response)


def Delete_goal(index: int, tool_context: ToolContext):
    """
    Tool to delete a goal by its index from the user's list of goals.
    """

    goals = tool_context.state.get("weekly_goals", [])

    if not goals:
        return "You don’t have any goals to delete."

    if index < 1 or index > len(goals):
        return f"Invalid index. Please provide a number between 1 and {len(goals)}."

    # Remove the selected goal
    removed_goal = goals.pop(index - 1)
    tool_context.state["weekly_goals"] = goals  # update state
    
    # Explicitly update the state delta to ensure persistence
    tool_context.actions.state_delta["weekly_goals"] = goals

    return f"Goal '{removed_goal['description']}' (started on {removed_goal['start_date']}) has been deleted."
