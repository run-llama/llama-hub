from typing import Optional
from llama_index.query_engine import BaseQueryEngine
from llama_index.llama_dataset import BaseLlamaDataset, BaseLlamaPredictionDataset
from llama_index.llama_pack.base import BaseLlamaPack
import tqdm
from llama_index.llms import OpenAI, LLM
from llama_index import ServiceContext
from llama_index.evaluation import (
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    SemanticSimilarityEvaluator,
)
import json
import pandas as pd
from llama_index.evaluation.notebook_utils import (
    get_eval_results_df,
)

import pandas as pd
import nest_asyncio


class RagEvaluatorPack(BaseLlamaPack):
    """A pack for performing evaluation with your own RAG pipeline."""

    def __init__(
        self,
        query_engine: BaseQueryEngine,
        rag_dataset: BaseLlamaDataset,
        judge_llm: Optional[LLM] = None,
    ):
        nest_asyncio.apply()
        self.query_engine = query_engine
        self.rag_dataset = rag_dataset
        if judge_llm is None:
            self.judge_llm = OpenAI(temperature=0, model="gpt-4")
        else:
            assert isinstance(judge_llm, LLM)
            self.judge_llm = judge_llm

    async def _make_predictions(self):
        self.prediction_dataset: BaseLlamaPredictionDataset = await self.rag_dataset.amake_predictions_with(
            query_engine=self.query_engine, show_progress=True
        )

    def _prepare_judges(self):
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

    async def _evaluate_example_prediction(self, judges, example, prediction):
        correctness_result = await judges["correctness"].aevaluate(
            query=example.query,
            response=prediction.response,
            reference=example.reference_answer,
        )

        relevancy_result = await judges["relevancy"].aevaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        faithfulness_result = await judges["faithfulness"].aevaluate(
            query=example.query,
            response=prediction.response,
            contexts=prediction.contexts,
        )

        semantic_similarity_result = await judges["semantic_similarity"].aevaluate(
            query=example.query,
            response="\n".join(prediction.contexts),
            reference="\n".join(example.reference_contexts),
        )
        return (
            correctness_result,
            relevancy_result,
            faithfulness_result,
            semantic_similarity_result,
        )

    def _save_evaluations(self, evals):
        # saving evaluations
        evaluations_objects = {
            "context_similarity": [e.dict() for e in evals["context_similarity"]],
            "correctness": [e.dict() for e in evals["correctness"]],
            "faithfulness": [e.dict() for e in evals["faithfulness"]],
            "relevancy": [e.dict() for e in evals["relevancy"]],
        }

        with open("_evaluations.json", "w") as json_file:
            json.dump(evaluations_objects, json_file)

    def _prepare_and_save_benchmark_results(self, evals):
        _, mean_correctness_df = get_eval_results_df(
            ["base_rag"] * len(evals["correctness"]),
            evals["correctness"],
            metric="correctness",
        )
        _, mean_relevancy_df = get_eval_results_df(
            ["base_rag"] * len(evals["relevancy"]),
            evals["relevancy"],
            metric="relevancy",
        )
        _, mean_faithfulness_df = get_eval_results_df(
            ["base_rag"] * len(evals["faithfulness"]),
            evals["faithfulness"],
            metric="faithfulness",
        )
        _, mean_context_similarity_df = get_eval_results_df(
            ["base_rag"] * len(evals["context_similarity"]),
            evals["context_similarity"],
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

    async def _make_evaluations(self):
        judges = self._prepare_judges()

        evals = {
            "correctness": [],
            "relevancy": [],
            "faithfulness": [],
            "context_similarity": [],
        }

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

            evals["correctness"].append(correctness_result)
            evals["relevancy"].append(relevancy_result)
            evals["faithfulness"].append(faithfulness_result)
            evals["context_similarity"].append(semantic_similarity_result)

        self._save_evaluations(evals=evals)
        benchmark_df = self._prepare_and_save_benchmark_results(evals=evals)
        return benchmark_df

    async def run(self):
        await self._make_predictions()
        benchmark_df = await self._make_evaluations()
        return benchmark_df
