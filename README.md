**_An open protocol enabling communication and interoperability between AI agents for seamless day-to-day work and life management._**

This project demonstrates a multi-agent system using the Agent2Agent (A2A) protocol to help with daily productivity. It features two specialized agents that work together:

*   **Activity Tracker Agent**: Built with the Google ADK, this agent helps you track tasks, work items, and their progress.
*   **Calendar Agent**: Built with LangGraph, this agent connects to your Google Calendar to manage and report on your schedule.

These agents communicate using the A2A protocol, allowing them to collaborate and be managed from a single client application.

### **Getting Started**

* 🤖 To run the agents, follow the instructions in their respective directories:
    * [**Activity Tracker (Google ADK)**](/samples/python/agents/google_adk/README.md)
    * [**Calendar Agent (LangGraph)**](/samples/python/agents/langgraph/README.md)
* 🎬 Use [samples](/samples) to see A2A in action
    * [Multi-Agent Web App](/demo/README.md) for calendar and activity tracking.
    * CLI ([Python](/samples/python/hosts/cli/README.md))
* 📚 For details on the underlying protocol, read the [technical documentation](https://google.github.io/A2A/#/documentation) and review the [json specification](/specification).

### **Contributing**

We highly value community contributions! Please see our [contributing guide](CONTRIBUTING.md) and join the discussion on [GitHub](httpss://github.com/google/A2A/discussions).

### **About**

A2A Protocol is an open source project run by Google LLC, under [License](LICENSE) and open to contributions from the entire community.

---

## Disclaimer

This repository is not an officially supported Google product. The code is for demonstration purposes only.
Security Notice: When using the Agent-to-Agent (A2A) protocol in production, treat all data from external agents as untrusted. Always validate and sanitize inputs—such as AgentCards, messages, and artifacts—to prevent security risks like prompt injection. Developers are responsible for implementing appropriate security measures to protect their systems and users.
