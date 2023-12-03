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
