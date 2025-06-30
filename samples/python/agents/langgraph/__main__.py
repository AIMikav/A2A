from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from common.utils.push_notification_auth import PushNotificationSenderAuth
from agents.langgraph.task_manager import AgentTaskManager
from agents.langgraph.agent import CalendarAgent
import click
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=10000)
def main(host, port):
    """Starts the Calendar Agent server."""
    try:
        # No API key check needed for Google Calendar local OAuth, but keep for future extensibility
        # if not os.getenv("GOOGLE_API_KEY"):
        #     raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")

        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="calendar_tracking",
            name="Calendar & Day Planner",
            description="Helps you track, view, and summarize your Google Calendar events and daily schedule.",
            tags=["calendar", "day planner", "schedule", "events"],
            examples=["What are my events today?", "Show my next 10 meetings.", "What's on my calendar tomorrow?"],
        )
        agent_card = AgentCard(
            name="Calendar Agent",
            description="Helps you track and plan your day using your Google Calendar.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=CalendarAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=CalendarAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        notification_sender_auth = PushNotificationSenderAuth()
        notification_sender_auth.generate_jwk()
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=CalendarAgent(), notification_sender_auth=notification_sender_auth),
            host=host,
            port=port,
        )

        server.app.add_route(
            "/.well-known/jwks.json", notification_sender_auth.handle_jwks_endpoint, methods=["GET"]
        )

        logger.info(f"Starting server on {host}:{port}")
        server.start()
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()
