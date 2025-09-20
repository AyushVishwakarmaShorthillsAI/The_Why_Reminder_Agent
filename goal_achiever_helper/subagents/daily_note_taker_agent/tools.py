from google.adk.tools import ToolContext
from datetime import datetime

def Daily_Reflection_Taker(notes: str, tool_context: ToolContext):
    """
    Tool to store the user's daily reflections and notes in session state.
    """

    date_str = datetime.now().strftime("%Y-%m-%d")

    # Initialize daily_notes if not present
    if "daily_notes" not in tool_context.state:
        tool_context.state["daily_notes"] = []

    # Append today's note
    tool_context.state["daily_notes"].append({
        "date": date_str,
        "note": notes
    })
    
    # Explicitly update the state delta to ensure persistence
    tool_context.actions.state_delta["daily_notes"] = tool_context.state["daily_notes"]

    return f"Your reflection for {date_str} has been saved. Thank you for sharing!"

def Show_All_Daily_Notes(tool_context: ToolContext):
    """
    Tool to display all the user's daily notes and reflections.
    """
    
    # Get daily notes from state
    daily_notes = tool_context.state.get("daily_notes", [])
    
    if not daily_notes:
        return "You haven't recorded any daily notes yet. Start by sharing your thoughts and reflections!"
    
    # Format the notes for display
    response = "📝 **Your Daily Notes & Reflections:**\n\n"
    
    for i, note_entry in enumerate(daily_notes, 1):
        date = note_entry.get("date", "Unknown date")
        note = note_entry.get("note", "No content")
        response += f"{i}. **{date}:**\n   {note}\n\n"
    
    response += f"Total notes recorded: {len(daily_notes)}"
    
    return response
