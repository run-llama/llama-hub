"""SharePoint files reader."""

import os
import logging

from typing import Any, Dict, List, Optional
import tempfile

import requests

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.schema import Document
from llama_hub.utils import import_loader


logger = logging.getLogger(__name__)


class SharePointReader(BaseReader):
    """SharePoint reader.

    Reads folders from the SharePoint site from a folder under documents.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        filename_as_id: bool = False,
        file_extractor: Optional[Dict[str, BaseReader]] = None,
    ) -> None:
        """
        Initializes an instance of SharePoint reader.

        Args:
            client_id: The Application ID for the app registered in Microsoft Azure Portal.
                       The application must alse be configured with MS Graph permissions "Files.ReadAll", "Sites.ReadAll" and BrowserSiteLists.Read.All.
            client_secret: The application secret for the app registered in Azure.
            tenant_id: Unique identifier of the Azure Active Directory Instance.
            file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file
                extension to a BaseReader class that specifies how to convert that file
                to text. See `SimpleDirectoryReader` for more details.
        """
        self.client_id = (client_id,)
        self.client_secret = (client_secret,)
        self.tenant_id = tenant_id
        self._authorization_headers = None
        self.file_extractor = file_extractor
        self.filename_as_id = filename_as_id

    def _setup_site_config(self, sharepoint_site_name: str):
        self._authorization_headers = {
            "Authorization": f"Bearer {self._get_access_token()}"
        }
        self._site_id_with_host_name = self._get_site_id_with_host_name(
            sharepoint_site_name
        )

    def _get_access_token(self) -> str:
        """
        Gets the access_token for accessing file from SharePoint.

        Returns:
            str: The access_token for accessing the file.

        Raises:
            ValueError: If there is an error in obtaining the access_token.
        """
        authority = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "resource": "https://graph.microsoft.com/",
        }

        response = requests.post(
            url=authority,
            data=payload,
        )

        if response.status_code == 200 and "access_token" in response.json().keys():
            return response.json()["access_token"]

        else:
            logger.error(response.json()["error"])
            raise ValueError(response.json()["error_description"])

    def _get_site_id_with_host_name(self, sharepoint_site_name: str) -> str:
        """
        Retrieves the site ID of a SharePoint site using the provided site name.

        Args:
            sharepoint_site_name (str): The name of the SharePoint site.

        Returns:
            str: The ID of the SharePoint site.

        Raises:
            Exception: If the specified SharePoint site is not found.
        """
        site_information_endpoint = (
            f"https://graph.microsoft.com/v1.0/sites?search={sharepoint_site_name}"
        )

        response = requests.get(
            url=site_information_endpoint,
            headers=self._authorization_headers,
        )

        if response.status_code == 200 and "value" in response.json():
            if (
                len(response.json()["value"]) > 0
                and "id" in response.json()["value"][0]
            ):
                return response.json()["value"][0]["id"]
            else:
                raise ValueError(
                    f"The specified sharepoint site {sharepoint_site_name} is not found."
                )
        else:
            if "error_description" in response.json():
                logger.error(response.json()["error"])
                raise ValueError(response.json()["error_description"])
            raise ValueError(response.json()["error"])

    def _get_drive_id(self) -> str:
        """
        Retrieves the drive ID of the SharePoint site.

        Returns:
            str: The ID of the SharePoint site drive.

        Raises:
            ValueError: If there is an error in obtaining the drive ID.
        """
        self._drive_id_endpoint = f"https://graph.microsoft.com/v1.0/sites/{self._site_id_with_host_name}/drives"

        response = requests.get(
            url=self._drive_id_endpoint,
            headers=self._authorization_headers,
        )

        if response.status_code == 200 and "value" in response.json():
            if (
                len(response.json()["value"]) > 0
                and "id" in response.json()["value"][0]
            ):
                return response.json()["value"][0]["id"]
            else:
                raise ValueError(
                    "Error occured while fetching the drives for the sharepoint site."
                )
        else:
            logger.error(response.json()["error"])
            raise ValueError(response.json()["error_description"])

    def _get_sharepoint_folder_id(self, folder_path: str) -> str:
        """
        Retrieves the folder ID of the SharePoint site.

        Args:
            folder_path (str): The path of the folder in the SharePoint site.

        Returns:
            str: The ID of the SharePoint site folder.
        """
        folder_id_endpoint = f"{self._drive_id_endpoint}/{self._drive_id}/root"

        if folder_path:
            folder_id_endpoint += f":/{folder_path}"

        response = requests.get(
            url=folder_id_endpoint,
            headers=self._authorization_headers,
        )

        if response.status_code == 200 and "id" in response.json():
            return response.json()["id"]
        else:
            raise ValueError(response.json()["error"])

    def _download_files_and_extract_metadata(
        self,
        folder_id: str,
        download_dir: str,
        include_subfolders: bool,
        file_types: List[str],
    ) -> Dict[str, Dict[str, str]]:
        """
        Downloads files from the specified folder ID and extracts metadata.

        Args:
            folder_id (str): The ID of the folder from which the files should be downloaded.
            download_dir (str): The directory where the files should be downloaded.
            include_subfolders (bool): If True, files from all subfolders are downloaded.
            file_types: (List[str]): A set of file types to load. If empty, loads all file types.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the metadata of the downloaded files.

        Raises:
            ValueError: If there is an error in downloading the files.
        """
        folder_info_endpoint = (
            f"{self._drive_id_endpoint}/{self._drive_id}/items/{folder_id}/children"
        )

        response = requests.get(
            url=folder_info_endpoint,
            headers=self._authorization_headers,
        )

        if response.status_code == 200:
            data = response.json()
            metadata = {}
            for item in data["value"]:
                if include_subfolders and "folder" in item:
                    sub_folder_download_dir = os.path.join(download_dir, item["name"])
                    subfolder_metadata = self._download_files_and_extract_metadata(
                        folder_id=item["id"],
                        download_dir=sub_folder_download_dir,
                        include_subfolders=include_subfolders,
                        file_types=file_types,
                    )

                    metadata.update(subfolder_metadata)

                elif "file" in item:
                    file_type = item["name"].split(".")[-1]
                    if not file_types or (file_type in file_types):
                        file_metadata = self._download_file(item, download_dir)
                        metadata.update(file_metadata)
            return metadata
        else:
            logger.error(response.json()["error"])
            raise ValueError(response.json()["error"])

    def _download_pages_and_extract_metadata(
        self,
        download_dir: str,
    ) -> Dict[str, Dict[str, str]]:
        """
        Downloads Sharepoint pages as HTML files and extracts metadata.

        Args:
            download_dir (str): The directory where the files should be downloaded.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the metadata of the downloaded Sharepoint pages.

        Raises:
            ValueError: If there is an error in downloading the files.
        """
        pages_endpoint = f"https://graph.microsoft.com/beta/sites/{self._site_id_with_host_name}/pages"

        data = self._get_results_with_odatanext(pages_endpoint)
        # the maximum is 20 requests per batch
        # see https://learn.microsoft.com/en-us/graph/json-batching
        batch_size = 20
        metadata = {}

        # request the page content for a batch of 20 pages
        for i in range(0, len(data), batch_size):
            # Create a dict using enumerate to index each item in the batch, to later correlate the result with the original data
            batch = dict(enumerate(data[i : i + batch_size]))
            batch_endpoint: str = "https://graph.microsoft.com/beta/$batch"

            # set-up the requests to be made
            body = {
                "requests": [
                    {
                        "url": f"/sites/{self._site_id_with_host_name}/pages/{item['id']}/microsoft.graph.sitepage/webparts",
                        "method": "GET",
                        "id": idx,
                    }
                    for idx, item in batch.items()
                ]
            }
            batch_response = requests.post(
                url=batch_endpoint, json=body, headers=self._authorization_headers
            )

            # the result should contain results for all pages.
            # If something went wrong, this is indicated in the response per page
            for response in batch_response.json()["responses"]:
                try:
                    file_metadata = self._extract_page(
                        item=batch[int(response["id"])],
                        response=response,
                        download_dir=download_dir,
                    )
                    metadata.update(file_metadata)
                except ValueError:
                    pass
        return metadata

    def _extract_page(
        self, item: Dict[str, Any], response: Dict[str, Any], download_dir: str
    ) -> Dict[str, Dict[str, str]]:
        """
        Retrieves the HTML content of the SharePoint page referenced by the 'item' argument
        from the Microsoft Graph batch response. Stores the content as an .html file in the download_dir.

        Args:
            item (Dict[str, Any]): a sharepoint item that contains
                  the fields 'id', 'name' and 'webUrl'.
            response (Dict[str, Any]): A single Microsoft Graph response from a batch request.
                                       Expected to be correlated with the given item.
            download_dir (str): A directory to download the file to.

        Returns:
            Dict[str, Dict[str, str]]: The file_name of the page stored in the download_dir as key
                                       and the metadata of the page (item) as value
        """
        file_name = item["name"].replace(".aspx", ".html")
        metadata = {}

        if response.get("status") == 200:

            html_content = "\n".join(
                [
                    i["innerHtml"]
                    for i in response["body"]["value"]
                    if i["@odata.type"] == "#microsoft.graph.textWebPart"
                ]
            )
            if html_content == "":
                raise ValueError(
                    f"The page {item['name']} does not contain a textWebPart."
                )

            # Create the directory if it does not exist and save the file.
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            file_path = os.path.join(download_dir, file_name)
            with open(file_path, "w") as f:
                f.write(html_content)
            metadata[file_path] = self._extract_metadata_for_file(item)
            return metadata
        else:
            logger.error(response.json()["error"])
            raise ValueError(
                f"status: {response['status']}, body: {response['body']['error']}"
            )

    def _get_results_with_odatanext(
        self, request: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Given a request, checks if the result contains `@odata.nextLink` in the result.
        If true, this function returns itself calling the @odata.nextLink.
        If false, this function returns a list of all retrieved values.

        Args:
            request (str): A GET request to be made, that might include a field '@odata.nextLink'

        Returns:
            List[Dict[str, Any]]: A List with containing the metadata in Dict[str, Any] form of the pages to be extracted
        """
        if "prev_responses" not in kwargs.keys():
            prev_responses = []
        else:
            prev_responses = kwargs["prev_responses"]
        response = requests.get(url=request, headers=self._authorization_headers)
        if response.status_code == 200:
            result: Dict[str, Any] = response.json()
            prev_responses += result["value"]
            if "@odata.nextLink" in result.keys():
                return self._get_results_with_odatanext(
                    request=result["@odata.nextLink"],
                    prev_responses=prev_responses,
                )
            else:
                return prev_responses
        else:
            logger.error(response.json()["error"])
            raise ValueError(response.json()["error"])

    def _download_file_by_url(self, item: Dict[str, Any], download_dir: str) -> str:
        """
        Downloads the file from the provided URL.

        Args:
            item (Dict[str, Any]): Dictionary containing file metadata.
            download_dir (str): The directory where the files should be downloaded.

        Returns:
            str: The path of the downloaded file in the temporary directory.
        """

        # Get the donwload URL for the file.
        file_download_url = item["@microsoft.graph.downloadUrl"]
        file_name = item["name"]

        response = requests.get(file_download_url)

        # Create the directory if it does not exist and save the file.
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path

    def _extract_metadata_for_file(self, item: Dict[str, Any]) -> Dict[str, str]:
        """
        Extracts metadata related to the file.

        Parameters:
        - item (Dict[str, str]): Dictionary containing file metadata.

        Returns:
        - Dict[str, str]: A dictionary containing the extracted metadata.
        """
        # Extract the required metadata for file.

        file_metadata = {
            "file_id": item.get("id"),
            "file_name": item.get("name"),
            "url": item.get("webUrl"),
        }

        return file_metadata

    def _download_file(
        self,
        item: Dict[str, Any],
        download_dir: str,
    ) -> Dict[str, Dict[str, str]]:
        """
        Downloads a file to the temporary download folder and returns
        its metadata.

        Args:
            item (Dict[str, Any]): a sharepoint item that contains
                  the fields 'id', 'name' and 'webUrl'
            download_dir (str): A directory to download the file to.

        Returns:
            The metadata of the item
        """
        metadata = {}

        file_path = self._download_file_by_url(item, download_dir)

        metadata[file_path] = self._extract_metadata_for_file(item)
        return metadata

    def _download_files_from_sharepoint(
        self,
        download_dir: str,
        sharepoint_folder_path: str,
        recursive: bool,
        file_types: List[str],
    ) -> Dict[str, Dict[str, str]]:
        """
        Downloads files from the specified folder and returns the metadata for the downloaded files.

        Args:
            download_dir (str): The directory where the files should be downloaded.
            sharepoint_site_name (str): The name of the SharePoint site.
            sharepoint_folder_path (str): The path of the folder in the SharePoint site.
            recursive (bool): If True, files from all subfolders are downloaded.
            file_types: (List[str]): A set of file types to load. If empty, loads all file types.

        Returns:
            Dict[str,Dict[str, str]]: A dictionary containing file_name of the stored file
                                      as key and the metadata of the downloaded files as value.

        """

        self._drive_id = self._get_drive_id()

        self.sharepoint_folder_id = self._get_sharepoint_folder_id(
            sharepoint_folder_path
        )

        metadata = self._download_files_and_extract_metadata(
            folder_id=self.sharepoint_folder_id,
            download_dir=download_dir,
            include_subfolders=recursive,
            file_types=file_types,
        )

        return metadata

    def _load_documents_with_metadata(
        self,
        files_metadata: Dict[str, Any],
        download_dir: str,
        recursive: bool,
    ) -> List[Document]:
        """
        Loads the documents from the downloaded files.

        Args:
            files_metadata (Dict[str,Any]): A dictionary containing the metadata of the downloaded files.
            download_dir (str): The directory where the files should be downloaded.
            recursive (bool): If True, files from all subfolders are downloaded.

        Returns:
            List[Document]: A list containing the documents with metadata.
        """

        def get_metadata(filename: str) -> Any:
            return files_metadata[filename]

        try:
            simple_directory_reader = import_loader("SimpleDirectoryReader")
        except ImportError:
            simple_directory_reader = download_loader("SimpleDirectoryReader")

        simple_loader = simple_directory_reader(
            download_dir,
            file_metadata=get_metadata,
            recursive=recursive,
            filename_as_id=self.filename_as_id,
            file_extractor=self.file_extractor,
        )
        documents = simple_loader.load_data()
        return documents

    def load_data(
        self,
        sharepoint_site_name: str,
        sharepoint_folder_path: str = "",
        recursive: bool = False,
        include: List[str] = ["documents", "pages"],
        file_types: List[str] = [],
    ) -> List[Document]:
        """
        Loads the files from the specified folder in the SharePoint site.

        Args:
            sharepoint_site_name (str): The name of the SharePoint site.
            sharepoint_folder_path (str): The path of the folder in the SharePoint site.
                                          If `""` (default), loads data from the root folder of the
                                          SharePoint site.
            recursive (bool): If True, files from all subfolders are downloaded.
            include (List[str]): list of Sharepoint objects to include.
                                  Must contain at least 'pages' or 'documents' or both.
            file_types (List[str]): list of file extensions to include when downloading from
                                     the Sharepoint Drive. Leave empty to download all filetypes.

        Returns:
            List[Document]: A list containing the documents with metadata.

        Raises:
            Exception: If an error occurs while accessing SharePoint site.
        """
        if not include:
            raise ValueError(
                "'include' should not be an empty list, and include either 'documents' and/or 'pages'"
            )
        if any([i not in ["documents", "pages"] for i in include]):
            raise ValueError(
                "'include' contains an unexpected value. "
                + f"Valid values are ['documents', 'pages'], but got {include}"
            )
        if "documents" not in include and (recursive or file_types):
            logger.warning(
                "'documents' is not in 'include', so 'recursive' and 'file_types' have no effect."
            )
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                self._setup_site_config(sharepoint_site_name)
                files_metadata = {}
                if "documents" in include:
                    files_metadata.update(
                        self._download_files_from_sharepoint(
                            temp_dir, sharepoint_folder_path, recursive, file_types
                        )
                    )
                if "pages" in include:
                    files_metadata.update(
                        self._download_pages_and_extract_metadata(temp_dir)
                    )
                return self._load_documents_with_metadata(
                    files_metadata, temp_dir, recursive
                )
        except Exception as exp:
            logger.error(
                "An error occurred while accessing SharePoint: %s", exp, exc_info=True
            )
