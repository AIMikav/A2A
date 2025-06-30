## ADK Agent

This sample uses the Agent Development Kit (ADK) to create a simple "Activity Tracker" agent that is hosted as an A2A server.

This agent takes text requests from the client to track activities. It can add new activities with details like work item, due date, and progress. It can also save the tracked activities into an Excel file.

## Prerequisites

- Python 3.9 or higher
- [UV](https://docs.astral.sh/uv/)
- Access to an LLM and API Key


## Running the Sample

1. Navigate to the samples directory:
    ```bash
    cd samples/python/agents/google_adk
    ```
2. Create an environment file with your API key:

   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

4. Run an agent:
    ```bash
    uv run .
    ```

5. In a separate terminal, run the A2A client:
    ```
    # Connect to the agent (specify the agent URL with correct port)
    uv run hosts/cli --agent http://localhost:10002

    # If you changed the port when starting the agent, use that port instead
    # uv run hosts/cli --agent http://localhost:YOUR_PORT
    ```
