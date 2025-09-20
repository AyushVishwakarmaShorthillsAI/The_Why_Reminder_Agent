from google.adk.agents import LlmAgent
from .tools import Why_Reminder

why_reminder_agent = LlmAgent(
    name="why_reminder_agent",
    description="An agent that reminds users of their 'Why' behind their goals and motivates them",
    model="gemini-2.0-flash",
    instruction="""
    Your role is to periodically (after a set interval, say 10 conversations) remind users of their initial motivation (the "Why") for starting this journey. Use this to boost morale and encourage persistence. 
    If the user feels demotivated or is behind their goals deadline, present them with a motivational quote along with their 'Why'. Use the provided tool to fetch the 'Why' from the session state and present it to the user. 
    Always be polite and encouraging to support the user's goal-achieving journey.

    If you can't find any tool/subagent for a respective task, then delegate the task to root_agent.
    """,
    tools=[
        Why_Reminder
    ]
)