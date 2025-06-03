import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import LLMRef, FunctionRef
from aiq.builder.framework_enum import LLMFrameworkEnum

logger = logging.getLogger(__name__)


class Zlanggraph2FunctionConfig(FunctionBaseConfig, name="zlanggraph2"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    # parameter: str = Field(default="default_value", description="Notional description for this parameter")
    llm: LLMRef

@register_function(config_type=Zlanggraph2FunctionConfig)
async def zlanggraph2_function(
    config: Zlanggraph2FunctionConfig, builder: Builder
):
    
    llm = await builder.get_llm(config.llm, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    from langchain_core.tools import tool

    @tool
    def joke() -> str:
        """Tells you a joke"""
        return "A good joke be like the liar told the truth."

    llm_w_tools = llm.bind_tools([joke])

    # Implement your function logic here
    async def _response_fn(input_message: str) -> str:
        # Process the input_message and generate output
        # output_message = f"Hello from zlanggraph2 workflow! You said: {input_message}"
        response = await llm_w_tools.ainvoke(input_message)
        for tool_call in response.tool_calls:
            selected_tool = {"joke": joke,}[tool_call["name"].lower()]
            tool_msg = selected_tool.invoke(tool_call)

        return tool_msg.content

    try:
        yield FunctionInfo.create(single_fn=_response_fn)
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up zlanggraph2 workflow.")