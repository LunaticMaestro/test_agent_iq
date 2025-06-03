# SPDX-FileCopyrightText: Copyright (c) 2024-2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from pydantic import Field

logger = logging.getLogger(__name__)


class InequalityToolConfig(FunctionBaseConfig, name="calculator_inequality"):
    pass


@register_function(config_type=InequalityToolConfig)
async def calculator_inequality(tool_config: InequalityToolConfig, builder: Builder):

    import re

    async def _calculator_inequality(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        a = int(numbers[0])
        b = int(numbers[1])

        if a > b:
            return f"First number {a} is greater than the second number {b}"
        if a < b:
            return f"First number {a} is less than the second number {b}"

        return f"First number {a} is equal to the second number {b}"

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_inequality,
        description=("This is a mathematical tool used to perform an inequality comparison between two numbers. "
                     "It takes two numbers as an input and determines if one is greater or are equal."))


class MultiplyToolConfig(FunctionBaseConfig, name="calculator_multiply"):
    pass


@register_function(config_type=MultiplyToolConfig)
async def calculator_multiply(config: MultiplyToolConfig, builder: Builder):

    import re

    async def _calculator_multiply(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        a = int(numbers[0])
        b = int(numbers[1])

        return f"The product of {a} * {b} is {a * b}"

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_multiply,
        description=("This is a mathematical tool used to multiply two numbers together. "
                     "It takes 2 numbers as an input and computes their numeric product as the output."))


class DivisionToolConfig(FunctionBaseConfig, name="calculator_divide"):
    pass


@register_function(config_type=DivisionToolConfig)
async def calculator_divide(config: DivisionToolConfig, builder: Builder):

    import re

    async def _calculator_divide(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        a = int(numbers[0])
        b = int(numbers[1])

        # return f"The result of {a} / {b} is {a / b}"
        return eval("2+3")

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_divide,
        description=("This is a mathematical tool used to divide one number by another. "
                     "It takes 2 numbers as an input and computes their numeric quotient as the output."))


class SubtractToolConfig(FunctionBaseConfig, name="calculator_subtract"):
    pass


@register_function(config_type=SubtractToolConfig)
async def calculator_subtract(config: SubtractToolConfig, builder: Builder):

    import re

    async def _calculator_subtract(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        a = int(numbers[0])
        b = int(numbers[1])

        return f"The result of {a} - {b} is {a - b}"

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_subtract,
        description=("This is a mathematical tool used to subtract one number from another. "
                     "It takes 2 numbers as an input and computes their numeric difference as the output."))



class PythonExpressionE6rConfig(FunctionBaseConfig, name="python_expression_executor"):
    pass


@register_function(config_type=PythonExpressionE6rConfig)
async def calculator_subtract(config: PythonExpressionE6rConfig, builder: Builder):

    import re

    async def _python_expression_run(text: str) -> str:
        return eval(text)

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _python_expression_run,
        description=("This is a mathematical tool used to perform bodmas oeprations"
                     "It takes the bodmas express as input. "
                     "The expression must contain parenthesis."
                     "Examples: (2+(3/10))"))



from datetime import datetime
from zoneinfo import ZoneInfo
import time  # used to get the system's timezone name


class CurrentTimeToolConfig(FunctionBaseConfig, name="current_datetime"):
    """
    Simple tool which returns the current system time in human-readable format, including the system's timezone.
    """
    pass


@register_function(config_type=CurrentTimeToolConfig)
async def current_time(config: CurrentTimeToolConfig, builder: Builder):

    async def _get_current_time(unused: str) -> str:

        
        from datetime import datetime, timedelta, timezone
        offset = timezone(timedelta(hours=5, minutes=30))
        now = datetime.now(offset)
        now_human_readable = now.strftime("%Y-%m-%d %H:%M:%S %Z")

        return f"The current system time is {now_human_readable}"

    yield FunctionInfo.from_fn(
        _get_current_time,
        description="Returns the current system time including timezone, in human-readable format."
    )


from pydantic import BaseModel
class MyInput(BaseModel):
    library: str = Field(default="scikitlearn", description="name of the library to call")
    code_expression: str = Field(description="code expression that of that must be executed")

class MyOutput(BaseModel): 
    agent_output: str = Field(default="code executed. The output is a dictionary with keys name and age")
    memory: dict = {}

class LibraryCodeExecutionConfig(FunctionBaseConfig, name="library_code_execution"):
    pass 

@register_function(config_type=LibraryCodeExecutionConfig)
async def library_code_execute(config: LibraryCodeExecutionConfig, builder: Builder):
    

    async def _response_fn(input_: MyInput) -> MyOutput: 
        '''Use this function when requested to code certain library
        '''
        a = builder.get_function("current_datetime")
        b =  await a.ainvoke("something")
        print(b)
        out_ = MyOutput(memory={"name": "rahul", "age": 23})
        return out_
    
    yield FunctionInfo.from_fn(
        _response_fn,
        description="Use this function when requested to code certain library"
    )


from aiq.data_models.component_ref import EmbedderRef

class WebQueryTool(FunctionBaseConfig, name="webquery_tool"):
    webpage_url: str 
    description: str 
    chunk_size: int = 1024 
    embedder_name: EmbedderRef = "nvidia/nv-embedqa-e5-v5"

@register_function(config_type=WebQueryTool)
async def webquery_tool(config: WebQueryTool, builder: Builder):

    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import WebBaseLoader
    from langchain_core.embeddings import Embeddings
    from aiq.builder.framework_enum import LLMFrameworkEnum
    from langchain.tools.retriever import create_retriever_tool


    loader = WebBaseLoader(config.webpage_url)
    
    logger.info("Generating docs from webpages")
    embeddings: Embeddings = await builder.get_embedder(config.embedder_name, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    # download 
    docs = [ document async for document in loader.alazy_load()]

    # Chunk and store 
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=config.chunk_size,
        chunk_overlap=20,
        is_separator_regex=False,
    )
    documents = text_splitter.split_documents(docs) 
    vector = await FAISS.afrom_documents(documents, embeddings)

    retriever = vector.as_retriever() 

    retriever_tool = create_retriever_tool(
        retriever,
        "webpage_search",
        config.description
    )

    async def _inner(query: str) -> str: 
        return await retriever_tool.arun(query)
    
    yield FunctionInfo.from_fn(_inner, description=config.description)