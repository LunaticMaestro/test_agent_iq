import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

logger = logging.getLogger(__name__)


class ZjokeFunctionConfig(FunctionBaseConfig, name="zjoke"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    # parameter: str = Field(default="default_value", description="Notional description for this parameter")
    description: str = Field(default="This function tells a joke", description="Change the purpose of the function")

@register_function(config_type=ZjokeFunctionConfig)
async def zjoke_function(
    config: ZjokeFunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(input_message: str) -> str:
        # Process the input_message and generate output
        return "A good joke be like the liar told the truth."

    try:
        yield FunctionInfo.from_fn(
            _response_fn,
            description=config.description
        )
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up zjoke workflow.")