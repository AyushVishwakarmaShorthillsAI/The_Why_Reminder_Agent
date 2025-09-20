import asyncio
# Runner
from google.adk.runners import Runner
# agent
from goal_achiever_helper.agent import root_agent
# Session
from google.adk.sessions import InMemorySessionService
# Dotenv
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini API
import google.generativeai as genai
import os

# Get the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please add it to your .env file.")

# Configure the Gemini API with the API key
genai.configure(api_key=GEMINI_API_KEY)

# utils functions
from utils import call_agent_async, add_user_query_to_history

import random
# Generate a random integer between 1 and 100000 (inclusive) for user_id
USER_ID = str(random.randint(1, 100000))

# Create a session to maintain context across interactions
session_service = InMemorySessionService()

# step 1
# define the initial state for the session
initial_state = {
    "greeted": False,
    "user_name": "",
    "daily_notes": [],
    "weekly_goals": [],
    "the_Why": ""
}

async def main_async():   
    # step 2
    # Create a temporary session with the initial state
    temp_session=await session_service.create_session(
        app_name="Goal Achiever Helper",
        user_id=USER_ID,
        state=initial_state
    )

    print(f"session created with ID: {temp_session.id}")
    APP_NAME = "Goal Achiever Helper"
    SESSION_ID = temp_session.id

    # step 3
    # Create a Runner with Root agent and the session
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # step 4
    # Interactive Conversation Loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the application, Gooodbye!")
            break

        # Update interaction history with the user's query
        await add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

         # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

        # ===== PART 6: State Examination =====
        # Show final session state
        final_session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print("\nFinal Session State:")
        for key, value in final_session.state.items():
            print(f"{key}: {value}")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

