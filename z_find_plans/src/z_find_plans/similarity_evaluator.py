import asyncio

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm.asyncio import tqdm

from aiq.eval.evaluator.evaluator_model import EvalInput
from aiq.eval.evaluator.evaluator_model import EvalOutput
from aiq.eval.evaluator.evaluator_model import EvalOutputItem


class SimilarityEvaluator:
    '''Similarity evaluator class'''

    def __init__(self, similarity_type: str, max_concurrency: int):
        self.max_concurrency = max_concurrency
        self.similarity_type = similarity_type
        self.vectorizer = TfidfVectorizer()
        self.semaphore = asyncio.Semaphore(self.max_concurrency)

    async def evaluate(self, eval_input: EvalInput) -> EvalOutput:
        '''Evaluate function'''

        async def process_item(item):
            """Compute cosine similarity for an individual item"""
            question = item.input_obj
            answer = item.expected_output_obj
            generated_answer = item.output_obj

            # Compute TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([answer, generated_answer])

            # Compute cosine similarity score
            similarity_score = round(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0], 2)

            # Provide reasoning for the score
            reasoning = {
                "question": question,
                "answer": answer,
                "generated_answer": generated_answer,
                "similarity_type": "cosine"
            }

            return similarity_score, reasoning

        # Process items concurrently with a limit on concurrency
        results = await tqdm.gather(*[process_item(item) for item in eval_input.eval_input_items])

        # Extract scores and reasonings
        sample_scores, sample_reasonings = zip(*results) if results else ([], [])

        # Compute average score
        avg_score = round(sum(sample_scores) / len(sample_scores), 2) if sample_scores else 0.0

        # Construct EvalOutputItems
        eval_output_items = [
            EvalOutputItem(id=item.id, score=score, reasoning=reasoning)
            for item, score, reasoning in zip(eval_input.eval_input_items, sample_scores, sample_reasonings)
        ]

        return EvalOutput(average_score=avg_score, eval_output_items=eval_output_items)