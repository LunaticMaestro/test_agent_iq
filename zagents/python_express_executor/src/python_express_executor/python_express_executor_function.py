import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

logger = logging.getLogger(__name__)


class PythonExpressExecutorFunctionConfig(FunctionBaseConfig, name="python_express_executor"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    pass

@register_function(config_type=PythonExpressExecutorFunctionConfig)
async def python_express_executor_function(
    config: PythonExpressExecutorFunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(input_expression: str) -> str:
        # Process the input_message and generate output
        try: 
            output = str(eval(input_expression)) # TODO
        except Exception as e: 
            output = (f"Failed to execute the expression {input_expression}")
        return output

    try:
        yield FunctionInfo.create(single_fn=_response_fn)
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up python_express_executor workflow.")