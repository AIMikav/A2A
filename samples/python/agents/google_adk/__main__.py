from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from common.utils.push_notification_auth import PushNotificationSenderAuth
from task_manager import AgentTaskManager
from agent import ActivityTrackerAgent
import click
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=10002)
def main(host, port):
    try:
        if not os.getenv("GOOGLE_API_KEY"):
                raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")
        
        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="track_activity",
            name="Track Activity Tool",
            description="Helps with tracking activities and saving them to an Excel file.",
            tags=["activity", "tracker", "excel"],
            examples=["Can you add a new task for me?", "Save my activities to a file."],
        )
        agent_card = AgentCard(
            name="Activity Tracker Agent",
            description="This agent helps track your activities and save them to an Excel file.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=ActivityTrackerAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=ActivityTrackerAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        notification_sender_auth = PushNotificationSenderAuth()
        notification_sender_auth.generate_jwk()
        
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=ActivityTrackerAgent(), notification_sender_auth=notification_sender_auth),
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

