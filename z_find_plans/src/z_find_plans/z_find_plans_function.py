import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import EmbedderRef
from aiq.builder.framework_enum import LLMFrameworkEnum
import os

logger = logging.getLogger(__name__)


class ZFindPlansFunctionConfig(FunctionBaseConfig, name="z_find_plans"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    # parameter: str = Field(default="default_value", description="Notional description for this parameter")
    ingest_glob: str
    description: str
    chunk_size: int = 1024
    embedder_name: EmbedderRef = "nvidia/nv-embedqa-e5-v5"


@register_function(config_type=ZFindPlansFunctionConfig)
async def z_find_plans_function(
    config: ZFindPlansFunctionConfig, builder: Builder
):
    #  Core functionality implemented in this space
    from langchain.tools.retriever import create_retriever_tool
    from langchain_community.document_loaders import DirectoryLoader
    from langchain_community.document_loaders import TextLoader
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.embeddings import Embeddings


    embeddings: Embeddings = await builder.get_embedder(config.embedder_name, wrapper_type=LLMFrameworkEnum.LANGCHAIN)

    logger.info("Ingesting documents matching for the webpage: %s", config.ingest_glob)
    (ingest_dir, ingest_glob) = os.path.split(config.ingest_glob)
    loader = DirectoryLoader(ingest_dir, glob=ingest_glob, loader_cls=TextLoader)

    docs = [document async for document in loader.alazy_load()]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, separators=["#", "\n"])
    documents = text_splitter.split_documents(docs)
    vector = await FAISS.afrom_documents(documents, embeddings)

    retriever = vector.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "text_file_ingest",
        config.description,
    )

    # Implement your function logic here
    async def _response_fn(query: str) -> str:
        return await retriever_tool.arun(query)

    try:
        yield FunctionInfo.from_fn(_response_fn, description=config.description)
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up z_find_plans workflow.")