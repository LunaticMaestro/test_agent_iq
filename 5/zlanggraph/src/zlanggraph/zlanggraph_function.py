import logging

from pydantic import BaseModel, Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import LLMRef, FunctionRef
from aiq.builder.framework_enum import LLMFrameworkEnum

logger = logging.getLogger(__name__)


class ZlanggraphFunctionConfig(FunctionBaseConfig, name="zlanggraph"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    llm: LLMRef
    tool_names: list[FunctionRef]


@register_function(config_type=ZlanggraphFunctionConfig)
async def zlanggraph_function(
    config: ZlanggraphFunctionConfig, builder: Builder
):
    
    from langchain.chat_models import init_chat_model
    from langgraph.prebuilt import create_react_agent
    from typing_extensions import TypedDict
    from typing import Annotated
    from langgraph.graph.message import add_messages
    from langgraph.graph import StateGraph, START, END


    import json
    from langchain_core.messages import ToolMessage
    from langgraph.prebuilt import ToolNode, tools_condition
    from langchain_core.tools import tool


    llm = await builder.get_llm(config.llm, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    from langgraph.prebuilt import create_react_agent


    class State(TypedDict):
        messages: Annotated[list, add_messages]


    graph_builder = StateGraph(State)


    tools = builder.get_tools(tool_names=config.tool_names, wrapper_type=LLMFrameworkEnum.LANGCHAIN)

    tool_node = ToolNode(tools=tools)

    llm_with_tools = llm.bind_tools(tools)

    async def chatbot(state: State):
        # Inspect HERE: Uncomment one of the lines to observe the difference
        # return {"messages": [await llm.ainvoke(state["messages"])]}
        return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}



    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")
    graph = graph_builder.compile()    

    async def _response_fn(input_message: str) -> str:
        # Process the input_message and generate output

        response = await graph.ainvoke(
            {"messages": [{"role": "user", "content": input_message}]}
        )
        
        # Issue 1: Response must be a string 
        # return response

        # Fix 
        return response['messages'][-1].content

    try:
        yield FunctionInfo.create(single_fn=_response_fn)
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up zlanggraph workflow.")