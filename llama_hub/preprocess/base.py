"""Preprocess Reader."""
from typing import List
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from pypreprocess import Preprocess


class PreprocessReader(BaseReader):
    def __init__(self, api_key: str, *args, **kwargs):
        if api_key is None or api_key == "":
            raise ValueError(
                "Please provide an api key to be used while doing the auth with the system."
            )

        _info = {}
        self._preprocess = Preprocess(api_key)
        self._filepath = None
        self._process_id = None

        for key, value in kwargs.items():
            if key == "filepath":
                self._filepath = value
                self._preprocess.set_filepath(value)
            if key == "process_id":
                self._process_id = value
                self._preprocess.set_process_id(value)
            elif key in [
                "merge",
                "max",
                "min",
                "min_min",
                "table_output",
                "repeat_title",
                "table_header",
                "lamguage",
            ]:
                _info[key] = value
                
        if _info != {}:
            self._preprocess.set_info(_info)

        if self._filepath is None and self._process_id is None:
            raise ValueError(
                "Please provide either filepath or process_id to handle the resutls."
            )

    def load_data(self) -> List[Document]:
        if self._process_id is not None:
            return self._get_data_by_process()

        elif self._filepath is not None:
            return self._get_data_by_filepath()

        else:
            return []

    def get_process_id(self):
        return self._process_id

    def _get_data_by_filepath(self) -> List[Document]:
        documents = []
        pp_response = self._preprocess.chunk()
        if pp_response.status == "OK" and pp_response.success is True:
            self._process_id = pp_response.data["process"]["id"]
            reponse = self._preprocess.wait()
            if reponse.status == "OK" and reponse.success is True:
                for chunk in reponse.data["chunks"]:
                    documents.append(Document(text=chunk))
        return documents

    def _get_data_by_process(self) -> List[Document]:
        documents = []
        reponse = self._preprocess.wait()
        if reponse.status == "OK" and reponse.success is True:
            for chunk in reponse.data["chunks"]:
                documents.append(Document(text=chunk))
        return documents
