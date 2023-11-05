"""Docugami reader."""

import io
import os
import re

from typing import Any, Dict, List, Mapping, Optional
import requests

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

TD_NAME = "{http://www.w3.org/1999/xhtml}td"
TABLE_NAME = "{http://www.w3.org/1999/xhtml}table"

XPATH_KEY = "xpath"
DOCUMENT_ID_KEY = "id"
DOCUMENT_NAME_KEY = "name"
STRUCTURE_KEY = "structure"
TAG_KEY = "tag"
PROJECTS_KEY = "projects"

DEFAULT_API_ENDPOINT = "https://api.docugami.com/v1preview1"


class DocugamiReader(BaseReader):
    """Docugami reader.

    Reads Documents as nodes in a Document XML Knowledge Graph, from Docugami.

    """

    api: str = DEFAULT_API_ENDPOINT
    """API endpoint URL"""

    access_token: Optional[str] = os.environ.get("DOCUGAMI_API_KEY")
    """Access token for API endpoint."""

    min_chunk_size: int = 32
    """Threshold under which chunks are appended to next chunk to avoid over-chunking."""

    include_xml_tags: bool = False
    """Set to true for XML tags in chunk output text."""

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

        # helpers
        def _xpath_qname(node: Any) -> str:
            """Get the xpath qname for a node."""
            qname = f"{node.prefix}:{node.tag.split('}')[-1]}"

            parent = node.getparent()
            if parent is not None:
                doppelgangers = [x for x in parent if x.tag == node.tag]
                if len(doppelgangers) > 1:
                    idx_of_self = doppelgangers.index(node)
                    qname = f"{qname}[{idx_of_self + 1}]"

            return qname

        def _xpath(node: Any) -> str:
            """Get the xpath for a node."""
            ancestor_chain = node.xpath("ancestor-or-self::*")
            return "/" + "/".join(_xpath_qname(x) for x in ancestor_chain)

        def _structure_value(node: Any) -> Optional[str]:
            """Get the structure value for a node."""
            structure = (
                "table"
                if node.tag == TABLE_NAME
                else node.attrib[STRUCTURE_KEY]
                if STRUCTURE_KEY in node.attrib
                else None
            )
            return structure

        def _is_structural(node: Any) -> bool:
            """Check if a node is structural."""
            return _structure_value(node) is not None

        def _is_list_item_marker(node: Any) -> bool:
            """Check if a node is a list item marker."""
            structure = _structure_value(node)
            return structure is not None and structure.lower() == "lim"

        def _is_heading(node: Any) -> bool:
            """Check if a node is a heading."""
            structure = _structure_value(node)
            return structure is not None and structure.lower().startswith("h")

        def _get_text(nodes: List[Any]) -> str:
            """Get the text of a node."""
            text = ""
            for node in nodes:
                text += " ".join(node.itertext()).strip()
            return text

        def _get_simple_xml(nodes: List[Any]) -> str:
            """Gets simplified XML without attributes or namespaces for the given node."""

            # Recursive function to copy over elements to a new tree without namespaces and attributes
            def strip_ns_and_attribs(el):
                # Create a new element without namespace or attributes
                stripped_el = etree.Element(etree.QName(el).localname)
                # Copy text and tail (if any)
                stripped_el.text = el.text
                stripped_el.tail = el.tail
                # Recursively apply this function to all children
                for child in el:
                    stripped_el.append(strip_ns_and_attribs(child))
                return stripped_el

            xml = ""
            for node in nodes:
                clean_root = strip_ns_and_attribs(node)

                # Return the modified XML as a string
                xml += etree.tostring(clean_root, encoding="unicode")

            # remove empty non-semantic chunks from output
            xml = xml.replace("<chunk>", "").replace("</chunk>", "")
            return xml.strip()

        def _has_structural_descendant(node: Any) -> bool:
            """Check if a node has a structural descendant."""
            for child in node:
                if _is_structural(child) or _has_structural_descendant(child):
                    return True
            return False

        def _leaf_structural_nodes(node: Any) -> List:
            """Get the leaf structural nodes of a node."""
            if _is_structural(node) and not _has_structural_descendant(node):
                return [node]
            else:
                leaf_nodes = []
                for child in node:
                    leaf_nodes.extend(_leaf_structural_nodes(child))
                return leaf_nodes

        def _create_doc(main_node: Any, prepended_nodes: []) -> Document:
            """Create a Document from a node, with possibly some prepended nodes."""
            metadata = {
                XPATH_KEY: _xpath(main_node),
                DOCUMENT_ID_KEY: document[DOCUMENT_ID_KEY],
                DOCUMENT_NAME_KEY: document[DOCUMENT_NAME_KEY],
                STRUCTURE_KEY: main_node.attrib.get(STRUCTURE_KEY, ""),
                TAG_KEY: re.sub(r"\{.*\}", "", main_node.tag),
            }

            nodes = prepended_nodes
            if main_node is not None:
                nodes += main_node

            text = ""
            if self.include_xml_tags:
                text = _get_simple_xml(nodes)
            else:
                text = _get_text(nodes)

            if doc_metadata:
                metadata.update(doc_metadata)

            return Document(
                text=text,
                metadata=metadata,
                excluded_llm_metadata_keys=[XPATH_KEY, DOCUMENT_ID_KEY, STRUCTURE_KEY],
            )

        # parse the tree and return chunks
        tree = etree.parse(io.BytesIO(content))
        root = tree.getroot()

        chunks: List[Document] = []
        prepended_nodes = []
        for node in _leaf_structural_nodes(root):
            text = _get_text([node])
            if (
                _is_heading(node)
                or _is_list_item_marker(node)
                or len(text) < self.min_chunk_size
            ):
                # save headings, list markers, or other small chunks to be appended to the next chunk
                prepended_nodes.append(node)
            else:
                chunks.append(_create_doc(node, prepended_nodes))
                prepended_nodes = []

        if prepended_nodes:
            if not chunks:
                # edge case, there are only prepended nodes, no chunks yet
                chunks.append(_create_doc(None, prepended_nodes))
            else:
                # small chunk at the end left over, just append to last chunk
                if not chunks[-1].text:
                    chunks[-1].text = _get_text(prepended_nodes)
                else:
                    chunks[-1].text += " " + _get_text(prepended_nodes)

        return chunks

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
                        metadata[heading] = value
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


if __name__ == "__main__":
    reader = DocugamiReader()
    print(
        reader.load_data(
            docset_id="ecxqpipcoe2p", document_ids=["43rj0ds7s0ur", "bpc1vibyeke2"]
        )
    )
