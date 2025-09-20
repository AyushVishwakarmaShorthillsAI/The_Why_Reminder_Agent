from google.adk.tools import ToolContext
from google.adk.tools import google_search
import random


async def Why_Reminder(tool_context: ToolContext):
    """
    Reminds the user of their 'Why' behind their goals.
    Motivates them by retrieving a motivational quote via Google Search.
    """

    # Get stored WHY from state
    the_why = tool_context.state.get("the_Why")

    # Use google_search tool to fetch motivational quotes
    # (asks ADK's built-in Google Search tool)
    query = "motivational quotes for success"
    search_results = await google_search.run(query=query, context=tool_context)

    # Extract snippets/text from results (ADK's search returns structured parts)
    quotes = []
    for item in search_results.get("results", []):
        if "snippet" in item:
            quotes.append(item["snippet"])

    # Fallback if no quotes found
    quote = random.choice(quotes) if quotes else "Believe in yourself and all that you are."

    return (
        f"Remember, your 'Why' is a powerful motivator: {the_why}\n\n"
        f"💡 Here’s a motivational quote for you: \"{quote}\""
    )
