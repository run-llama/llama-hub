from typing import Optional, List, Any
from tqdm.asyncio import tqdm_asyncio
from llama_index.query_engine import BaseQueryEngine
from llama_index.llama_dataset import BaseLlamaDataset, BaseLlamaPredictionDataset
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.evaluation.base import EvaluationResult
import tqdm
from llama_index.llms import OpenAI, LLM
from llama_index import ServiceContext
from llama_index.evaluation import (
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    SemanticSimilarityEvaluator,
    EvaluationResult,
)
import json
import pandas as pd
from llama_index.evaluation.notebook_utils import (
    get_eval_results_df,
)
import pandas as pd
from collections import deque
from openai import RateLimitError
import warnings


class RagEvaluatorPack(BaseLlamaPack):
    """A pack for performing evaluation with your own RAG pipeline.

    Args:
        query_engine: The RAG pipeline to evaluate.
        rag_dataset: The BaseLlamaDataset to evaluate on.
        judge_llm: The LLM to use as the evaluator.
    """

    def __init__(
        self,
        query_engine: BaseQueryEngine,
        rag_dataset: BaseLlamaDataset,
        judge_llm: Optional[LLM] = None,
        batch_size: int = 25,
    ):
        self.query_engine = query_engine
        self.rag_dataset = rag_dataset
        if judge_llm is None:
            self.judge_llm = OpenAI(temperature=0, model="gpt-4")
        else:
            assert isinstance(judge_llm, LLM)
            self.judge_llm = judge_llm
        self._batch_size = batch_size
        self.evals = {
            "correctness": [],
            "relevancy": [],
            "faithfulness": [],
            "context_similarity": [],
        }
        self.eval_queue = deque(range(len(rag_dataset.examples)))
        self.prediction_dataset = None
        if batch_size > 50:
            warnings.warn(
                "You've set a large batch_size (>50). If using OpenAI GPT-4 as "
                " `judge_llm` (which is the default judge_llm),"
                " you may experience a RateLimitError. Previous successful eval "
                " responses are cached per batch. So hitting a RateLimitError"
                " would mean you'd lose all of the current batches successful "
                " GPT-4 calls."
            )

    async def _amake_predictions(self):
        """Async make predictions with query engine."""
        self.prediction_dataset: BaseLlamaPredictionDataset = (
            await self.rag_dataset.amake_predictions_with(
                query_engine=self.query_engine, show_progress=True
            )
        )

    def _make_predictions(self):
        """Sync make predictions with query engine."""
        self.prediction_dataset: BaseLlamaPredictionDataset = (
            self.rag_dataset.make_predictions_with(
                query_engine=self.query_engine, show_progress=True
            )
        )

    def _prepare_judges(self):
        """Construct the evaluators."""
        judges = {}
        judges["correctness"] = CorrectnessEvaluator(
            service_context=ServiceContext.from_defaults(
                llm=self.judge_llm,
            )
        )
        judges["relevancy"] = RelevancyEvaluator(
            service_context=ServiceContext.from_defaults(
                llm=self.judge_llm,
            )
        )
        judges["faithfulness"] = FaithfulnessEvaluator(
            service_context=ServiceContext.from_defaults(
                llm=self.judge_llm,
            )
        )
        judges["semantic_similarity"] = SemanticSimilarityEvaluator(
            service_context=ServiceContext.from_defaults()
        )
        return judges

    async def _areturn_null_eval_result(self, query) -> EvaluationResult:
        """A dummy async method that returns None.

        NOTE: this is used to handle case when creating async tasks for evaluating
        predictions where contexts do not exist.
        """
        return EvaluationResult(
            query=query,
        )

    def _return_null_eval_result(self, query) -> EvaluationResult:
        """A dummy async method that returns None.

        NOTE: this is used to handle case when creating async tasks for evaluating
        predictions where contexts do not exist.
        """
        return EvaluationResult(
            query=query,
        )

    def _create_async_evaluate_example_prediction_tasks(
        self, judges, example, prediction
    ):
        """Collect the co-routines."""
        correctness_task = judges["correctness"].aevaluate(
            query=example.query,
            response=prediction.response,
            reference=example.reference_answer,
        )

        relevancy_task = judges["relevancy"].aevaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        faithfulness_task = judges["faithfulness"].aevaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        if example.reference_contexts and prediction.contexts:
            semantic_similarity_task = judges["semantic_similarity"].aevaluate(
                query=example.query,
                response="\n".join(prediction.contexts),
                reference="\n".join(example.reference_contexts),
            )
        else:
            semantic_similarity_task = self._areturn_null_eval_result(
                query=example.query
            )

        return (
            correctness_task,
            relevancy_task,
            faithfulness_task,
            semantic_similarity_task,
        )

    def _evaluate_example_prediction(self, judges, example, prediction):
        """Collect the co-routines."""
        correctness_result = judges["correctness"].evaluate(
            query=example.query,
            response=prediction.response,
            reference=example.reference_answer,
        )

        relevancy_result = judges["relevancy"].evaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        faithfulness_result = judges["faithfulness"].evaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        if example.reference_contexts and prediction.contexts:
            semantic_similarity_result = judges["semantic_similarity"].evaluate(
                query=example.query,
                response="\n".join(prediction.contexts),
                reference="\n".join(example.reference_contexts),
            )
        else:
            semantic_similarity_result = self._return_null_eval_result(
                query=example.query
            )

        return (
            correctness_result,
            relevancy_result,
            faithfulness_result,
            semantic_similarity_result,
        )

    def _save_evaluations(self):
        """Save evaluation json object."""
        # saving evaluations
        evaluations_objects = {
            "context_similarity": [e.dict() for e in self.evals["context_similarity"]],
            "correctness": [e.dict() for e in self.evals["correctness"]],
            "faithfulness": [e.dict() for e in self.evals["faithfulness"]],
            "relevancy": [e.dict() for e in self.evals["relevancy"]],
        }

        with open("_evaluations.json", "w") as json_file:
            json.dump(evaluations_objects, json_file)

    def _prepare_and_save_benchmark_results(self):
        """Get mean score across all of the evaluated examples-predictions."""
        _, mean_correctness_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["correctness"]),
            self.evals["correctness"],
            metric="correctness",
        )
        _, mean_relevancy_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["relevancy"]),
            self.evals["relevancy"],
            metric="relevancy",
        )
        _, mean_faithfulness_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["faithfulness"]),
            self.evals["faithfulness"],
            metric="faithfulness",
        )
        _, mean_context_similarity_df = get_eval_results_df(
            ["base_rag"] * len(self.evals["context_similarity"]),
            self.evals["context_similarity"],
            metric="context_similarity",
        )

        mean_scores_df = pd.concat(
            [
                mean_correctness_df.reset_index(),
                mean_relevancy_df.reset_index(),
                mean_faithfulness_df.reset_index(),
                mean_context_similarity_df.reset_index(),
            ],
            axis=0,
            ignore_index=True,
        )
        mean_scores_df = mean_scores_df.set_index("index")
        mean_scores_df.index = mean_scores_df.index.set_names(["metrics"])

        # save mean_scores_df
        mean_scores_df.to_csv("benchmark.csv")
        return mean_scores_df

    def _make_evaluations(self):
        """Sync make evaluations."""
        judges = self._prepare_judges()

        for example, prediction in tqdm.tqdm(
            zip(self.rag_dataset.examples, self.prediction_dataset.predictions)
        ):
            (
                correctness_result,
                relevancy_result,
                faithfulness_result,
                semantic_similarity_result,
            ) = self._evaluate_example_prediction(
                judges=judges, example=example, prediction=prediction
            )

            self.evals["correctness"].append(correctness_result)
            self.evals["relevancy"].append(relevancy_result)
            self.evals["faithfulness"].append(faithfulness_result)
            self.evals["context_similarity"].append(semantic_similarity_result)

        self._save_evaluations()
        benchmark_df = self._prepare_and_save_benchmark_results()
        return benchmark_df

    def _batch_examples_and_preds(
        self,
        examples: List[Any],
        predictions: List[Any],
        batch_size: int = 20,
        start_position: int = 0,
    ):
        """Batches examples and predictions with a given batch_size."""
        assert len(examples) == len(predictions)
        num_examples = len(examples)
        for ndx in range(start_position, num_examples, batch_size):
            yield examples[ndx : min(ndx + batch_size, num_examples)], predictions[
                ndx : min(ndx + batch_size, num_examples)
            ]

    async def _amake_evaluations(self):
        """Async make evaluations."""
        judges = self._prepare_judges()

        start_ix = self.eval_queue[0]
        for batch in self._batch_examples_and_preds(
            self.rag_dataset.examples,
            self.prediction_dataset.predictions,
            batch_size=self._batch_size,
            start_position=start_ix
        ):
            examples, predictions = batch
            tasks = []
            tqdm_iterator = tqdm.tqdm(zip(examples, predictions))
            for example, prediction in tqdm_iterator:
                (
                    correctness_task,
                    relevancy_task,
                    faithfulness_task,
                    semantic_similarity_task,
                ) = self._create_async_evaluate_example_prediction_tasks(
                    judges=judges, example=example, prediction=prediction
                )

                tasks += [
                    correctness_task,
                    relevancy_task,
                    faithfulness_task,
                    semantic_similarity_task,
                ]

            # do this in batches to avoid RateLimitError
            try:
                eval_results: List[EvaluationResult] = await tqdm_asyncio.gather(*tasks)
            except RateLimitError as err:
                tqdm_iterator.close()
                raise ValueError(
                    "You've hit rate limits on your OpenAI subscription. This"
                    " `RagEvaluatorPack` maintains state of evaluations. Simply"
                    " re-invoke .arun() in order to continue from where you left"
                    " off."
                ) from err
            # store in memory
            # since final result of eval_results respects order of inputs
            # just take appropriate slices
            self.evals["correctness"] += eval_results[::4]
            self.evals["relevancy"] += eval_results[1::4]
            self.evals["faithfulness"] += eval_results[2::4]
            self.evals["context_similarity"] += eval_results[3::4]
            # update queue
            for _ in range(self._batch_size):
                if self.eval_queue:
                    self.eval_queue.popleft()

        self._save_evaluations()
        benchmark_df = self._prepare_and_save_benchmark_results()
        return benchmark_df

    def run(self):
        if self.prediction_dataset is None:
            self._make_predictions()
        benchmark_df = self._make_evaluations()
        return benchmark_df

    async def arun(self):
        if self.prediction_dataset is None:
            await self._amake_predictions()
        print(f"queue start position: {self.eval_queue[0]}", flush=True)
        benchmark_df = await self._amake_evaluations()
        return benchmark_df
