from langchain_nvidia_ai_endpoints import ChatNVIDIA

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

model_id = "meta/llama-3.1-405b-instruct"
llm = ChatNVIDIA(model=model_id, temperature=0)


client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/workspaces/do_aiq2/zlanggraph/src/zlanggraph/research.py"],
            "transport": "stdio",
        },
    }
)

import asyncio
tools = asyncio.run(client.get_tools())
agent = create_react_agent(llm, tools)
res = asyncio.run(agent.ainvoke({"messages": "Can you search for papers around physics and find just two of them."}))
pass
# math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
# weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})