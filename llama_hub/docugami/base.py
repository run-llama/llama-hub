"""Docugami reader."""

import io
import os
from pathlib import Path

from typing import Dict, List, Mapping, Optional
import requests

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

TABLE_NAME = "{http://www.w3.org/1999/xhtml}table"

XPATH_KEY = "xpath"
DOCUMENT_ID_KEY = "id"
DOCUMENT_NAME_KEY = "name"
STRUCTURE_KEY = "structure"
TAG_KEY = "tag"
PROJECTS_KEY = "projects"

DEFAULT_API_ENDPOINT = "https://api.docugami.com/v1preview1"
DEFAULT_MAX_METADATA_LENGTH = 1024
DEFAULT_MIN_CHUNK_SIZE = 32


class DocugamiReader(BaseReader):
    """Docugami reader.

    Reads Documents as nodes in a Document XML Knowledge Graph, from Docugami.

    """

    api: str = DEFAULT_API_ENDPOINT
    """The Docugami API endpoint to use."""

    access_token: Optional[str] = os.environ.get("DOCUGAMI_API_KEY")
    """The Docugami API access token to use."""

    max_metadata_length = DEFAULT_MAX_METADATA_LENGTH
    """Max length of metadata values."""

    min_chunk_size: int = DEFAULT_MIN_CHUNK_SIZE
    """Threshold under which chunks are appended to next chunk to avoid over-chunking."""

    include_xml_tags: bool = False
    """Set to true for XML tags in chunk output text."""

    sub_chunk_tables: bool = False
    """Set to True to return sub-chunks within tables."""

    whitespace_normalize_text: bool = True
    """Set to False if you want the full whitespace formatting in the original XML doc, including indentation."""

    def _parse_dgml(
        self, document: Mapping, content: bytes, doc_metadata: Optional[Mapping] = None
    ) -> List[Document]:
        """Parse a single DGML document into a list of Documents."""
        try:
            from lxml import etree
        except ImportError:
            raise ValueError(
                "Could not import lxml python package. "
                "Please install it with `pip install lxml`."
            )

        try:
            from dgml_utils.segmentation import get_leaf_structural_chunks
        except ImportError:
            raise ValueError(
                "Could not import from dgml-utils python package. "
                "Please install it with `pip install dgml-utils`."
            )

        # parse the tree and return chunks
        tree = etree.parse(io.BytesIO(content))
        root = tree.getroot()

        framework_chunks: List[Document] = []
        dg_chunks = get_leaf_structural_chunks(
            root,
            min_chunk_size=self.min_chunk_size,
            whitespace_normalize_text=self.whitespace_normalize_text,
            sub_chunk_tables=self.sub_chunk_tables,
            include_xml_tags=self.include_xml_tags,
        )

        for dg_chunk in dg_chunks:
            metadata = {
                XPATH_KEY: dg_chunk.xpath,
                DOCUMENT_ID_KEY: document[DOCUMENT_ID_KEY],
                DOCUMENT_NAME_KEY: document[DOCUMENT_NAME_KEY],
                STRUCTURE_KEY: dg_chunk.structure,
                TAG_KEY: dg_chunk.tag,
            }

            if doc_metadata:
                metadata.update(doc_metadata)

            framework_chunks.append(
                Document(
                    text=dg_chunk.text,
                    metadata=metadata,
                    excluded_llm_metadata_keys=[
                        XPATH_KEY,
                        DOCUMENT_ID_KEY,
                        STRUCTURE_KEY,
                    ],
                )
            )

        return framework_chunks

    def _document_details_for_docset_id(self, docset_id: str) -> List[Dict]:
        """Gets all document details for the given docset ID"""
        url = f"{self.api}/docsets/{docset_id}/documents"
        all_documents = []

        while url:
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            if response.ok:
                data = response.json()
                all_documents.extend(data["documents"])
                url = data.get("next", None)
            else:
                raise Exception(
                    f"Failed to download {url} (status: {response.status_code})"
                )

        return all_documents

    def _project_details_for_docset_id(self, docset_id: str) -> List[Dict]:
        """Gets all project details for the given docset ID"""
        url = f"{self.api}/projects?docset.id={docset_id}"
        all_projects = []

        while url:
            response = requests.request(
                "GET",
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                data={},
            )
            if response.ok:
                data = response.json()
                all_projects.extend(data["projects"])
                url = data.get("next", None)
            else:
                raise Exception(
                    f"Failed to download {url} (status: {response.status_code})"
                )

        return all_projects

    def _metadata_for_project(self, project: Dict) -> Dict:
        """Gets project metadata for all files"""
        project_id = project.get("id")

        url = f"{self.api}/projects/{project_id}/artifacts/latest"
        all_artifacts = []

        while url:
            response = requests.request(
                "GET",
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                data={},
            )
            if response.ok:
                data = response.json()
                all_artifacts.extend(data["artifacts"])
                url = data.get("next", None)
            else:
                raise Exception(
                    f"Failed to download {url} (status: {response.status_code})"
                )

        per_file_metadata = {}
        for artifact in all_artifacts:
            artifact_name = artifact.get("name")
            artifact_url = artifact.get("url")
            artifact_doc = artifact.get("document")

            if artifact_name == "report-values.xml" and artifact_url and artifact_doc:
                doc_id = artifact_doc["id"]
                metadata: Dict = {}

                # the evaluated XML for each document is named after the project
                response = requests.request(
                    "GET",
                    f"{artifact_url}/content",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    data={},
                )

                if response.ok:
                    try:
                        from lxml import etree
                    except ImportError:
                        raise ValueError(
                            "Could not import lxml python package. "
                            "Please install it with `pip install lxml`."
                        )
                    artifact_tree = etree.parse(io.BytesIO(response.content))
                    artifact_root = artifact_tree.getroot()
                    ns = artifact_root.nsmap
                    entries = artifact_root.xpath("//pr:Entry", namespaces=ns)
                    for entry in entries:
                        heading = entry.xpath("./pr:Heading", namespaces=ns)[0].text
                        value = " ".join(
                            entry.xpath("./pr:Value", namespaces=ns)[0].itertext()
                        ).strip()
                        metadata[heading] = value[: self.max_metadata_length]
                    per_file_metadata[doc_id] = metadata
                else:
                    raise Exception(
                        f"Failed to download {artifact_url}/content "
                        + "(status: {response.status_code})"
                    )

        return per_file_metadata

    def _load_chunks_for_document(
        self, docset_id: str, document: Dict, doc_metadata: Optional[Dict] = None
    ) -> List[Document]:
        """Load chunks for a document."""
        document_id = document["id"]
        url = f"{self.api}/docsets/{docset_id}/documents/{document_id}/dgml"

        response = requests.request(
            "GET",
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            data={},
        )

        if response.ok:
            return self._parse_dgml(document, response.content, doc_metadata)
        else:
            raise Exception(
                f"Failed to download {url} (status: {response.status_code})"
            )

    def load_data(
        self,
        docset_id: str,
        document_ids: Optional[List[str]] = None,
        access_token: Optional[str] = None,
    ) -> List[Document]:
        """Load data the given docset_id in Docugami

        Args:
            docset_id (str): Document set ID to load data for.
            document_ids (Optional[List[str]]): Optional list of document ids to load data for.
                                    If not specified, all documents from docset_id are loaded.
        """
        chunks: List[Document] = []

        if access_token:
            self.access_token = access_token

        if not self.access_token:
            raise Exception(
                "Please specify access token as argument or set the DOCUGAMI_API_KEY"
                " env var."
            )

        _document_details = self._document_details_for_docset_id(docset_id)
        if document_ids:
            _document_details = [
                d for d in _document_details if d["id"] in document_ids
            ]

        _project_details = self._project_details_for_docset_id(docset_id)
        combined_project_metadata = {}
        if _project_details:
            # if there are any projects for this docset, load project metadata
            for project in _project_details:
                metadata = self._metadata_for_project(project)
                combined_project_metadata.update(metadata)

        for doc in _document_details:
            doc_metadata = combined_project_metadata.get(doc["id"])
            chunks += self._load_chunks_for_document(docset_id, doc, doc_metadata)

        return chunks

    def load_data_from_xml(self, xml_file_path: Path) -> List[Document]:
        chunks: List[Document] = []
        with open(xml_file_path, "rb") as file:
            chunks += self._parse_dgml(
                {
                    DOCUMENT_ID_KEY: xml_file_path.name,
                    DOCUMENT_NAME_KEY: xml_file_path.name,
                },
                file.read(),
            )
        return chunks
