import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

logger = logging.getLogger(__name__)


class Zagent0FunctionConfig(FunctionBaseConfig, name="execute_pandas"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    pass
    # Add your custom configuration parameters here
    # parameter: str = Field(default="default_value", description="Notional description for this parameter")


@register_function(config_type=Zagent0FunctionConfig)
async def zagent0_function(
    config: Zagent0FunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(input_expression: str) -> str:
        # Process the input_message and generate output
        # output_message = f"Hello You said to execute: {input_message}"

        try: 
            output = str(eval(input_expression))
        except Exception as e: 
            print(f"Failed to execute the expression {input_expression}")
        return output

    try:
        yield FunctionInfo.from_fn(
            _response_fn,
            description="Helps execute python expressions."
        )
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up zagent0 workflow.")