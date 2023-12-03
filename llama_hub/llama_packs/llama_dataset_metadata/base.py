from llama_index.llama_pack.base import BaseLlamaPack
from llama_hub.llama_packs.llama_dataset_metadata.card import DatasetCard
from llama_hub.llama_packs.llama_dataset_metadata.readme import Readme
import json


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
