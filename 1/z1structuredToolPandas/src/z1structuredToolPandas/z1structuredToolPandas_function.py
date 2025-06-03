import ast
import logging

import numpy as np
import pandas as pd
from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import LLMRef
from aiq.builder.framework_enum import LLMFrameworkEnum
from langchain_core.messages import AIMessage

# Self Library import
from .prompts import  ACTION_PROMPT, RESPONSE_PROMPT

logger = logging.getLogger(__name__)


class Z1StructuredtoolpandasFunctionConfig(FunctionBaseConfig, name="z1structuredToolPandas"):
    """
    Handles Excel, CSV files with respect to natural language queries.
    """
    llm: LLMRef
    csv_file: str
    csv_metafile: str
    description: str = Field(default="A dataset query engine", description="Describe for which data the engine is used for")
    max_retries: int = Field(default=2)


@register_function(config_type=Z1StructuredtoolpandasFunctionConfig)
async def z1structuredToolPandas_function(
    config: Z1StructuredtoolpandasFunctionConfig, builder: Builder
):
    # Caching dataframe 
    df: pd.DataFrame = pd.read_excel(config.csv_file)
    df_meta: str = '' # GETS UPDATED
    with open(config.csv_metafile, "r", encoding="utf-8") as f:
        df_meta: str = f.read()

    # Cachine LLM 
    llm = await builder.get_llm(config.llm, wrapper_type=LLMFrameworkEnum.LANGCHAIN)

    # Implement your function logic here
    async def _response_fn(user_query: str) -> str:
        # prompt 
        session_ACTION_PROMPT = ACTION_PROMPT.format(user_query=user_query, df_meta=df_meta)
        
        # Generate Actions via LLM 
        ai_message: AIMessage = await llm.ainvoke(session_ACTION_PROMPT)
        logger.info("[z1structuredToolPandas: ACTION_PROMPT's OUTPUT]")
        logger.info(ai_message.content)

        # Parse and perform actions    
        parsed_pycmds_str :str = extract_bracket_content(ai_message.content)
        expression_dict: dict = expression_executor(parsed_pycmds_str, df)

        # Exctract final content message
        #  This is based on the `ACTION_PROMPT` in which we specifically asked the LLM to have following variables
        #   - `output`
        output_facts: str = expression_dict.get("output", '')
        
        logger.info("[z1structuredToolPandas: ACTION_PROMPT's EXECUTED]")
        logger.debug(output_facts)

        # Response Generation prompt 
        session_RESPONSE_PROMPT = RESPONSE_PROMPT.format(user_query=user_query, retrieved_data=output_facts )
        ai_message: AIMessage = await llm.ainvoke(session_RESPONSE_PROMPT)

        return str(ai_message.content)
    
    try:
        yield FunctionInfo.from_fn(
            _response_fn,
            description=config.description
        )
    except GeneratorExit:
        print("Function exited early!")
    except Exception as e:
        logger.error(e)
    finally:
        print("Cleaning up z1structuredToolPandas workflow.")


def extract_bracket_content(text: str) -> str:
    '''ETL tool, hardcoded parsers that extracts the text between first ans last square brackets
    
    '''
    start = text.find('[')
    end = text.rfind(']') + 1  # include the last ']'
    if start == -1 or end == -1 or start >= end:
        return ""  # return empty if brackets not found properly
    return text[start:end]

def expression_executor(input_exp: str, df=None) -> dict:
    '''Execute python REPL commands; but stores their outputs in key value dictionary

    Kindly note that the variable uses pandas import as `pd`, numpy as `np`

    Returns
    ---
        the dictionary will contain the variables names as key and their values as output of executed commands
        **in case of error** empty dictionary is returned.
    '''
    try:
        # Convert the input string to a list
        commands = ast.literal_eval(input_exp)
        local_vars:dict = dict([list(map(str.strip, command.split('=', 1))) for command in commands])

        # Dictionary to simulate local scope
        local_vars.update({'df': df, 'pd': pd, 'np': np})
        for command in commands:
            exec(command, globals(), local_vars)

        return local_vars  # return all evaluated variables
    except Exception as e:
        logger.error("[expression_executor]", e)
    
    return {} # Just returns the empty dictionary
