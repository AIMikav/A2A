import json
import random
import pandas as pd
from typing import Any, AsyncIterable, Dict, List, Optional
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Local cache of created request_ids for demo purposes.
request_ids = set()

activities = []


def add_activity(
    work_item: str, details: str, due_date: str, progress: str
) -> dict[str, Any]:
  """
    Adds a new activity to the tracker.

    Args:
        work_item (str): What you are working on.
        details (str): Additional details about the work item.
        due_date (str): When the work item is expected to be completed.
        progress (str): The current progress of the work item.

    Returns:
        dict[str, Any]: A dictionary containing the status of the operation.
    """
  activities.append(
      {
          "Work Item": work_item,
          "Details": details,
          "Due Date": due_date,
          "Progress": progress,
      }
  )
  return {"status": "Activity added successfully."}


def save_activities_to_excel(file_path: str) -> dict[str, Any]:
  """
    Saves all tracked activities to an Excel file.

    Args:
        file_path (str): The path to save the Excel file to.

    Returns:
        dict[str, Any]: A dictionary containing the status of the operation.
    """
  if not activities:
    return {"status": "No activities to save."}

  df = pd.DataFrame(activities)
  df.to_excel(file_path, index=False)
  return {"status": f"Activities saved to {file_path}"}


class ActivityTrackerAgent:
  """An agent that handles tracking activities."""

  SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

  def __init__(self):
    self._agent = self._build_agent()
    self._user_id = "remote_agent"
    self._runner = Runner(
        app_name=self._agent.name,
        agent=self._agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )

  def invoke(self, query, session_id) -> str:
    session = self._runner.session_service.get_session(
        app_name=self._agent.name, user_id=self._user_id, session_id=session_id
    )
    content = types.Content(
        role="user", parts=[types.Part.from_text(text=query)]
    )
    if session is None:
      session = self._runner.session_service.create_session(
          app_name=self._agent.name,
          user_id=self._user_id,
          state={},
          session_id=session_id,
      )
    events = list(
        self._runner.run(
            user_id=self._user_id, session_id=session.id, new_message=content
        )
    )
    if not events or not events[-1].content or not events[-1].content.parts:
      return ""
    return "\n".join([p.text for p in events[-1].content.parts if p.text])

  async def stream(self, query, session_id) -> AsyncIterable[Dict[str, Any]]:
    session = self._runner.session_service.get_session(
        app_name=self._agent.name, user_id=self._user_id, session_id=session_id
    )
    content = types.Content(
        role="user", parts=[types.Part.from_text(text=query)]
    )
    if session is None:
      session = self._runner.session_service.create_session(
          app_name=self._agent.name,
          user_id=self._user_id,
          state={},
          session_id=session_id,
      )
    async for event in self._runner.run_async(
        user_id=self._user_id, session_id=session.id, new_message=content
    ):
      if event.is_final_response():
        response = ""
        if event.content and event.content.parts and event.content.parts[0].text:
          response = "\n".join([p.text for p in event.content.parts if p.text])
        elif (
            event.content
            and event.content.parts
            and any(True for p in event.content.parts if p.function_response)
        ):
          response = next(
              (p.function_response.model_dump() for p in event.content.parts)
          )
        yield {
            "is_task_complete": True,
            "content": response,
        }
      else:
        yield {
            "is_task_complete": False,
            "updates": "Processing the activity tracking request...",
        }

  def _build_agent(self) -> LlmAgent:
    """Builds the LLM agent for the activity tracker agent."""
    return LlmAgent(
        model="gemini-1.5-flash",
        name="activity_tracker_agent",
        description=(
            "This agent helps track your activities and save them to an Excel"
            " file."
        ),
        instruction="""
    You are an agent that helps me track my activities.

    When I tell you about an activity, you should use the `add_activity` tool to record it. You'll need to ask me for the following information if I don't provide it:
      1. 'Work Item': What I am working on.
      2. 'Details': Any additional details.
      3. 'Due Date': When I expect to complete it.
      4. 'Progress': The current progress.

    When I want to save my activities, you should use the `save_activities_to_excel` tool. You will need to ask me for the file path to save the Excel file.

    Always be helpful and ask clarifying questions if you need more information.
    """,
        tools=[
            add_activity,
            save_activities_to_excel,
        ],
    )

