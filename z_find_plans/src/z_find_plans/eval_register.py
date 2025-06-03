from pydantic import Field

from aiq.builder.builder import EvalBuilder
from aiq.builder.evaluator import EvaluatorInfo
from aiq.cli.register_workflow import register_evaluator
from aiq.data_models.evaluator import EvaluatorBaseConfig


class SimilarityEvaluatorConfig(EvaluatorBaseConfig, name="similarity"):
    '''Configuration for custom similarity evaluator'''
    similarity_type: str = Field(description="Similarity type to be computed", default="cosine")


@register_evaluator(config_type=SimilarityEvaluatorConfig)
async def register_similarity_evaluator(config: SimilarityEvaluatorConfig, builder: EvalBuilder):
    '''Register custom evaluator'''
    from .similarity_evaluator import SimilarityEvaluator
    evaluator = SimilarityEvaluator(config.similarity_type, builder.get_max_concurrency())

    yield EvaluatorInfo(config=config, evaluate_fn=evaluator.evaluate, description="Simlaity Evaluator")