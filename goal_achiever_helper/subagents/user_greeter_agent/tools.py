from google.adk.tools import ToolContext


def initial_greeter():
    """
    Greets the user and provides an overview of the goal-setting process.
    Asks the user for their 'Name' and the 'Why' behind their goals.
    """
    return (
        "Hello! I'm your Goal Achiever Helper. I'm here to assist you in setting and achieving your goals. "
        "To get started, may I know your name and the reason why you want to achieve your goals(meaning 'The Why' behind everything for this new journey)?"
    )    

def Info_Collector(name: str, the_why: str, tool_context: ToolContext):
    """
    Tool to collect and store the user's name and the 'Why' behind their goals.
    The values are stored in the session state so they can be reused later.
    """

    # Store values into state
    tool_context.state["user_name"] = name
    tool_context.state["the_Why"] = the_why
    
    # Explicitly update the state delta to ensure persistence
    tool_context.actions.state_delta["user_name"] = name
    tool_context.actions.state_delta["the_Why"] = the_why

    return (
        f"Thank you, {name}! It's great to meet you. "
        f"Remember, your 'Why' is a powerful motivator. "
        f"Keep it in mind as we work together to achieve your goals: {the_why}"
    )