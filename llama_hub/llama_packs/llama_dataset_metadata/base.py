import json

import pandas as pd
from typing import List, Optional

from llama_index.bridge.pydantic import BaseModel
from llama_index.indices.base import BaseIndex
from llama_index.llama_dataset import LabelledRagDataset
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.bridge.pydantic import BaseModel
from llama_index.download.utils import get_file_content
from llama_index.download.module import LLAMA_HUB_URL


class Readme(BaseModel):
    name: str
    _readme_template_path: str = "/llama_datasets/template_README.md"

    def _name_to_title_case(self) -> str:
        return " ".join(el.title() for el in self.name.split(" "))

    def _name_to_camel_case(self) -> str:
        return "".join(el.title() for el in self.name.split(" "))

    def _name_to_snake_case(self) -> str:
        return self.name.replace(" ", "_").lower()

    def _get_readme_str(self) -> str:
        text, _ = get_file_content(LLAMA_HUB_URL, self._readme_template_path)
        return text

    def create_readme(self) -> str:
        readme_str = self._get_readme_str()
        return readme_str.format(
            NAME=self._name_to_title_case(), NAME_CAMELCASE=self._name_to_camel_case()
        )


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class BaseMetadata(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class BaselineConfig(BaseMetadata):
    chunk_size: int
    llm: str
    similarity_top_k: int
    embed_model: str


class BaselineMetrics(BaseMetadata):
    context_similarity: Optional[float]
    correctness: float
    faithfulness: float
    relevancy: float


class Baseline(BaseMetadata):
    name: str
    config: BaselineConfig
    metrics: BaselineMetrics
    code_url: str


class DatasetCard(BaseMetadata):
    name: str
    description: str
    number_observations: int
    contains_examples_by_humans: bool
    contains_examples_by_ai: bool
    source_urls: Optional[List[str]]
    baselines: List[Baseline]

    @staticmethod
    def _format_metric(val: float):
        return float("{:,.3f}".format(val))

    @classmethod
    def from_rag_evaluation(
        cls,
        index: BaseIndex,
        benchmark_df: pd.DataFrame,
        rag_dataset: LabelledRagDataset,
        name: str,
        baseline_name: str,
        description: str,
        source_urls: Optional[List[str]] = None,
        code_url: Optional[str] = None,
    ):

        # extract metadata from rag_dataset
        num_observations = len(rag_dataset.examples)
        contains_examples_by_humans = any(
            (el.query_by.type == "human" or el.reference_answer_by.type == "human")
            for el in rag_dataset.examples
        )
        contains_examples_by_ai = any(
            (el.query_by.type == "ai" or el.reference_answer_by.type == "ai")
            for el in rag_dataset.examples
        )

        # extract baseline config info from index
        llm = index.service_context.llm.model
        embed_model = index.as_retriever().get_service_context().embed_model.model_name
        chunk_size = (
            index.as_retriever().get_service_context().transformations[0].chunk_size
        )
        similarity_top_k = index.as_retriever()._similarity_top_k
        baseline_config = BaselineConfig(
            llm=llm,
            chunk_size=chunk_size,
            similarity_top_k=similarity_top_k,
            embed_model=embed_model,
        )

        # extract baseline metrics from benchmark_df
        baseline_metrics = BaselineMetrics(
            correctness=cls._format_metric(
                benchmark_df.T["mean_correctness_score"].values[0]
            ),
            relevancy=cls._format_metric(
                benchmark_df.T["mean_relevancy_score"].values[0]
            ),
            faithfulness=cls._format_metric(
                benchmark_df.T["mean_faithfulness_score"].values[0]
            ),
            context_similarity=cls._format_metric(
                benchmark_df.T["mean_context_similarity_score"].values[0]
            ),
        )

        # baseline
        if code_url is None:
            code_url = ""
        baseline = Baseline(
            name=baseline_name,
            config=baseline_config,
            metrics=baseline_metrics,
            code_url=code_url,
        )

        if source_urls is None:
            source_urls = []

        return cls(
            name=name,
            description=description,
            source_urls=source_urls,
            number_observations=num_observations,
            contains_examples_by_humans=contains_examples_by_humans,
            contains_examples_by_ai=contains_examples_by_ai,
            baselines=[baseline],
        )


class LlamaDatasetMetadataPack(BaseLlamaPack):
    def run(self, index, benchmark_df, rag_dataset, name, description, baseline_name):
        readme_obj = Readme(name=name)
        card_obj = DatasetCard.from_rag_evaluation(
            index=index,
            benchmark_df=benchmark_df,
            rag_dataset=rag_dataset,
            name=name,
            description=description,
            baseline_name=baseline_name,
        )

        # save card.json
        with open("card.json", "w") as f:
            json.dump(card_obj.dict(), f)

        # save README.md
        with open("README.md", "w") as f:
            f.write(readme_obj.create_readme())
