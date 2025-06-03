import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

logger = logging.getLogger(__name__)


class ZMemFunctionConfig(FunctionBaseConfig, name="z_mem"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here

from typing import Any
class MemInp:
    key: str 
    value: Any = None

@register_function(config_type=ZMemFunctionConfig)
async def z_mem_function(
    config: ZMemFunctionConfig, builder: Builder
):
    memory: dict = {}
    memory["default"] = "hello world"

    # Implement your function logic here
    async def _response_fn(search: MemInp) -> str:
        # Process the input_message and generate output
        return memory[search.key]
        # return output_message

    try:
        yield FunctionInfo.create(single_fn=_response_fn)
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up z_mem workflow.")