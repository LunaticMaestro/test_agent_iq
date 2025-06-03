import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

# Custom 
from aiq.data_models.component_ref import LLMRef
import pandas as pd

# [END] Custom

logger = logging.getLogger(__name__)

from langgraph.store.memory import InMemoryStore


class ZTableAgentFunctionConfig(FunctionBaseConfig, name="z_table_agent"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    llm: LLMRef
    csv_file: str
    csv_metafile: str
    description: str = Field(default="A dataset query engine", description="Describe for which data the engine is used for")
    is_chat_agent: bool = Field(default=False, description="If its the final agent then the response is going to be conversation way." )

@register_function(config_type=ZTableAgentFunctionConfig)
async def z_table_agent_function(
    config: ZTableAgentFunctionConfig, builder: Builder
):
    # [Start] Custo 
    df: pd.DataFrame = pd.read_excel(config.csv_file)
    with open(config.csv_metafile, "r", encoding="utf-8") as f:
        df_meta: str = f.read()

    fn = builder.get_function("z_mem")

    # Implement your function logic here
    async def _response_fn(input_message: str) -> str:

        # Take input 
        # Decide the plann
        # Return the list of statements to execute 
        # Call the Executor 
        # Fomulate return response 

        # Process the input_message and generate output
        output_message = f"Hello from z_table_agent workflow! You said: {input_message}"
        return output_message

    try:
        # use `is_chat_agent`
        yield FunctionInfo.from_fn(single_fn=_response_fn)
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up z_table_agent workflow.")