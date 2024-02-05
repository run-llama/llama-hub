"""Mintter reader class.

Pass in the access_method (either author_publications or group_publications). For groups_publications, pass in the group_id as well.
This will import the publications into a List of Documents,
with each Document containing text from under a Mintter block.

"""
from groups.v1alpha import groups_pb2
from groups.v1alpha import groups_pb2_grpc
from documents.v1alpha import documents_pb2
from documents.v1alpha import documents_pb2_grpc

from google.protobuf.json_format import MessageToDict

import grpc

from typing import Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from langchain.docstore.document import Document as LCDocument

from llama_index.readers.base import BaseReader
from llama_index.readers.json import JSONReader
from llama_index.readers.schema.base import Document


class MintterPublicationsReader(BaseReader):
    """Utilities for loading data from a Mintter Daemon.

    Args:
        access_method (str): group_publications | author_publications.
        (opt) group_id (str): The group id to load publications from.

    """

    def __init__(self, access_method:str, group_id: str):
        """Init params."""
        self.access_method = access_method
        self.group_id = group_id

    def list_group_content(self,group_id):
        with grpc.insecure_channel('localhost:55002') as channel:
            stub = groups_pb2_grpc.GroupsStub(channel)
            request = groups_pb2.ListContentRequest(id=group_id)
            response = stub.ListContent(request)
            # print(response)
            return response
        
    def generate_publications_info(self,group_publication_list):
        document_details = []

        for key, value in group_publication_list["content"].items():
            document_id = value
            cid_list = document_id.split("?v=")
            document_info = {
                "title": key,  # Store the title/key for reference
                "document_id": cid_list[0],  # The document ID is always present
                "version": cid_list[1] if len(cid_list) > 1 else None  # The version is optional
            }   
            document_details.append(document_info)
        
        return document_details

    def extract_document_content(self,document_id, version,local_only=False):
        # LightClient Syntax: res = self._publications.GetPublication(documents_pb2.GetPublicationRequest(document_id=eid.split("?v=")[0], version=eid.split("?v=")[1], local_only=local_only))
        
        with grpc.insecure_channel('localhost:55002') as channel:
            stub = documents_pb2_grpc.PublicationsStub(channel)
            if version is None:
                request = documents_pb2.GetPublicationRequest(document_id=document_id, local_only=local_only)
            else:
                request = documents_pb2.GetPublicationRequest(document_id=document_id, version=version, local_only=local_only)
            
            response = stub.GetPublication(request)
            print(f'Document content: {response}')
            return response

    def load_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
        """Load data from the input directory."""
        docs: List[Document] = []
        
        group_publications = self.list_group_content(self.group_id)
        group_publications_list = MessageToDict(group_publications)
        group_publications_details = self.generate_documents_info(group_publications_list)
        
        for doc in group_publications_details:
            extracted_document = self.extract_document_content(self, doc['document_id'], doc['version'])
            content = JSONReader().load_data(extracted_document)
            docs.extend(content)
        return docs

    def load_langchain_documents(self, **load_kwargs: Any) -> List["LCDocument"]:
        """Load data in LangChain document format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]