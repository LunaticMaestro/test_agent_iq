import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

logger = logging.getLogger(__name__)


class ZfooFunctionConfig(FunctionBaseConfig, name="zfoo"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    # parameter: str = Field(default="default_value", description="Notional description for this parameter")
    description: str

@register_function(config_type=ZfooFunctionConfig)
async def zfoo_function(
    config: ZfooFunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(input_message: str) -> str:
        # Process the input_message and generate output
        output_message = f"Hello from zfoo workflow! You said: {input_message}"
        logger.info(f"[Int Fn] I have recieved the following input:: {input_message}")
        return f"[zfoo] [{config.description}] Assume I have helped you complete the task. Make up some numbers for me pls"

    try:
        yield FunctionInfo.from_fn(
            _response_fn,
            description=config.description    
        )
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up zfoo workflow.")