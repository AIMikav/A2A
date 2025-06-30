## Sample Agents

All the agents in this directory are samples built on different frameworks highlighting different capabilities. Each agent runs as a standalone A2A server. 

Each agent can be run as its own A2A server with the instructions on its README. By default, each will run on a separate port on localhost (you can use command line arguments to override).

To interact with the servers, use an A2AClient in a host app (such as the CLI). See [Host Apps](/samples/python/hosts/README.md) for details.

* [**Google ADK**](/samples/python/agents/google_adk/README.md)  
Sample agent to track activities. It can add new activities with details like work item, due date, and progress and save them to an Excel file. Showcases multi-turn interactions through A2A.

* [**LangGraph**](/samples/python/agents/langgraph/README.md)  
Sample agent which can track your calendar and act as a day planner. Showcases multi-turn interactions, streaming updates and Google Calendar API tool usage. 

