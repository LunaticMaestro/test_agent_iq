import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import LLMRef
from aiq.builder.framework_enum import LLMFrameworkEnum
from langchain_core.messages import AIMessage
import pandas as pd 
from pydantic import BaseModel
import numpy as np

logger = logging.getLogger(__name__)


class PandasExpressionGeneratorFunctionConfig(FunctionBaseConfig, name="pandas_expression_generator"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    # parameter: str = Field(default="default_value", description="Notional description for this parameter")
    llm: LLMRef
    csv_file: str
    csv_metafile: str
    description: str = Field(default="A dataset query engine", description="Describe for which data the engine is used for")

@register_function(config_type=PandasExpressionGeneratorFunctionConfig)
async def pandas_expression_generator_function(
    config: PandasExpressionGeneratorFunctionConfig, builder: Builder
):
    df: pd.DataFrame = pd.read_excel(config.csv_file)
    with open(config.csv_metafile, "r", encoding="utf-8") as f:
        df_meta: str = f.read()


    def extract_bracket_content(text):
        start = text.find('[')
        end = text.rfind(']') + 1  # include the last ']'
        if start == -1 or end == -1 or start >= end:
            return ""  # return empty if brackets not found properly
        return text[start:end]

    import ast
    def expression_executor(input_exp: str, df=None) -> tuple:
        # Convert the input string to a list
        try:
            commands = ast.literal_eval(input_exp)
            print(input_exp)
            local_vars:dict = dict([list(map(str.strip, command.split('=', 1))) for command in commands])

            # Dictionary to simulate local scope
            local_vars.update({'df': df, 'pd': pd, 'np': np})
            # local_vars = {}
            for command in commands:
                exec(command, globals(), local_vars)

        except Exception as e: 
            logger.error("Error evaluating expression")
            logger.error(e)
        return (local_vars.get("output", None), local_vars.get("output_verbal"))


    # Implement your function logic here
    async def _response_fn(input_query: str) -> str:

        # Create LLM 
        llm_ = await builder.get_llm(config.llm, wrapper_type=LLMFrameworkEnum.LANGCHAIN)

        # Prompt
        prompt_ = f'''You are a python expression generator. 
        
        Given the dataframe `df` and pandas import as `pd` which has the following metadata

        CSV Meta
        ---
        {df_meta}
        
        Generate python expression to solve the query:
        {input_query}

        You must generate list of python expressions output format must as follows:

        [
            "key_var = df[...]"                 // intermediate step 
            "key_var2 = key_var[df[...]...]"    // intermediate step 

                                                // reset the index of df if requrired
                                                // convert the grouped dataframe to dictionaries
                                                // 
                                                // the second last step should always assign output to the variable `output`
                                                // never use 'print' in the expression
                                                // be careful when using grouped dataframe in subsequent steps, you may need intermediate steps to handle them
            "output" = str.  Have the string as list (records) of dictionaries (columns). Ensure to reset index if required
            "output_verbal" = "constant string" // this is the last step
                                                // Always write here your explaination what the `output` variable is all about 
                                                // Also write that whats more that you can provide data (from the columns) on what is not included here.
        ]


        Certain template questions and expected approach from you
        1. When user wants to what is present in the data
        > you should respond back with names of columns 

        Dont write reasoning; just list of strings which has python expressions
        The list should not have markdown fencing.
        '''

        # just var declaration
        df 

        try:
            ai_message: AIMessage = await llm_.ainvoke(prompt_)
            logger.info("[Following Should just be structured list of string]")
            logger.info(ai_message)
            structured_text_str = extract_bracket_content(ai_message.content)
            out_, out_verbal = expression_executor(structured_text_str, df)
            
        except Exception as e: 
            logger.error(str(e))
            logger.info("Retrying...")
            out_verbal = "Unable to serve the request."
            out_ = ''
            # output_message = f"Hello from pandas_expression_generator workflow! You said: {input_message}"

        return f"Followin is the data of {out_verbal}: {out_}"

    try:
        yield FunctionInfo.from_fn(
            _response_fn,
            description=config.description
        )
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up pandas_expression_generator workflow.")