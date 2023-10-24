import pytest
from pytest_mock import MockerFixture
from unittest.mock import patch
from llama_hub.microsoft_onedrive.base import OneDriveReader
from importlib.util import find_spec

msal_spec = find_spec("msal")
if msal_spec is None:
    msal_available = False
else:
    msal_available = True


def test_onedrivereader_init():

    client_id = "test_client_id"
    client_secret = "test_client_secret"
    tenant_id = "test_tenant_id"

    reader = OneDriveReader(client_id, client_secret, tenant_id)

    # Verify that the object's attributes are correctly set
    assert reader.client_id == client_id
    assert reader.client_secret == client_secret
    assert reader.tenant_id == tenant_id
    assert reader._is_interactive_auth is False

    # Test with the client_secret being None
    reader = OneDriveReader(client_id, None, tenant_id)

    assert reader.client_id == client_id
    assert reader.client_secret is None
    assert reader.tenant_id == tenant_id
    assert reader._is_interactive_auth is True


@pytest.mark.skipif(
    not msal_available,
    reason="Skipping test because MSAL package is not available",
)
def test_authenticate_with_msal_interactive(mocker: MockerFixture):
    # Mocking the MSAL PublicClientApplication and its method
    public_app_mock = mocker.Mock()
    public_app_mock.acquire_token_interactive.return_value = {
        "access_token": "test_access_token"
    }
    mocker.patch("msal.PublicClientApplication", return_value=public_app_mock)
    mocker.patch("llama_hub.microsoft_onedrive.base.logger")

    # Creating the OneDriveReader instance with _is_interactive_auth = True
    reader = OneDriveReader("client_id", None, "tenant_id")

    token = reader._authenticate_with_msal()

    # Assert the token is returned correctly and acquire_token_interactive was called
    assert token == "test_access_token"
    public_app_mock.acquire_token_interactive.assert_called_once()


@pytest.mark.skipif(
    not msal_available,
    reason="Skipping test because MSAL package is not available",
)
def test_authenticate_with_msal_confidential(mocker: MockerFixture):
    # Mocking the MSAL ConfidentialClientApplication and its method
    confidential_app_mock = mocker.Mock()
    confidential_app_mock.acquire_token_for_client.return_value = {
        "access_token": "test_access_token"
    }
    mocker.patch(
        "msal.ConfidentialClientApplication", return_value=confidential_app_mock
    )
    mocker.patch("llama_hub.microsoft_onedrive.base.logger")

    # Creating the OneDriveReader instance with _is_interactive_auth = False
    reader = OneDriveReader("client_id", "client_secret", "tenant_id")
    token = reader._authenticate_with_msal()

    # Assert the token is returned correctly and acquire_token_for_client was called
    assert token == "test_access_token"
    confidential_app_mock.acquire_token_for_client.assert_called_once()


@pytest.mark.skipif(
    not msal_available,
    reason="Skipping test because MSAL package is not available",
)
def test_authenticate_with_msal_failure(mocker: MockerFixture):
    # Mocking the MSAL PublicClientApplication and its method to simulate a failure
    public_app_mock = mocker.Mock()
    public_app_mock.acquire_token_interactive.return_value = {"error": "test_error"}
    mocker.patch("msal.PublicClientApplication", return_value=public_app_mock)

    # Mocking the logger
    mocker.patch("llama_hub.microsoft_onedrive.base.logger")

    # Creating the OneDriveReader instance
    reader = OneDriveReader("client_id", None, "tenant_id")

    # Call the method we are testing and expect an MsalException
    with pytest.raises(Exception):
        reader._authenticate_with_msal()

    # Assert acquire_token_interactive was called
    public_app_mock.acquire_token_interactive.assert_called_once()


def test_check_approved_mimetype_and_download_file(mocker: MockerFixture):
    # Mocking the "_download_file_by_url" and "_extract_metadata_for_file" methods within OneDriveReader
    mocker.patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._download_file_by_url",
        return_value="/path/to/downloaded/file",  # Simulate the return of a file path
    )
    mocker.patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._extract_metadata_for_file",
        return_value={"key": "value"},  # Simulate the return of file metadata
    )

    ondrive_reader = OneDriveReader("client_id")
    item = {"file": {"mimeType": "application/pdf", "name": "test.pdf"}}

    # Call the method
    result = ondrive_reader._check_approved_mimetype_and_download_file(
        item, "/local/dir", ["application/pdf"]
    )

    # Verify the results.
    assert result == {"/path/to/downloaded/file": {"key": "value"}}


@pytest.mark.parametrize(
    "client_secret,is_interactive,is_relative,is_file,userprincipalname,expected_endpoint,expected_exception",
    [
        # Interactive auth, relative path, file
        (
            None,
            True,
            True,
            True,
            None,
            "https://graph.microsoft.com/v1.0/me/drive/root:/item_ref",
            None,
        ),
        # App auth, relative path, folder
        (
            "client_secret",
            False,
            True,
            False,
            "user@example.com",
            "https://graph.microsoft.com/v1.0/users/user@example.com/drive/root:/item_ref:/children",
            None,
        ),
        # App auth, no userprincipalname
        (
            "client_secret",
            False,
            False,
            True,
            None,
            None,
            "userprincipalname cannot be empty for App authentication. Provide the userprincipalname (email mostly) of user whose OneDrive needs to be accessed",
        ),
        # App auth, non-relative path, file
        (
            "client_secret",
            False,
            False,
            True,
            "user@example.com",
            "https://graph.microsoft.com/v1.0/users/user@example.com/drive/items/item_ref",
            None,
        ),
    ],
)
def test_construct_endpoint(
    client_secret,
    is_interactive,
    is_relative,
    is_file,
    userprincipalname,
    expected_endpoint,
    expected_exception,
):
    reader = OneDriveReader("client_id", client_secret)

    if expected_exception:
        with pytest.raises(Exception) as excinfo:
            reader._construct_endpoint(
                "item_ref", is_relative, is_file, userprincipalname
            )
        assert str(excinfo.value) == expected_exception
    else:
        endpoint = reader._construct_endpoint(
            "item_ref", is_relative, is_file, userprincipalname
        )
        assert endpoint == expected_endpoint


@patch("llama_hub.microsoft_onedrive.base.requests.get")
@patch("llama_hub.microsoft_onedrive.base.OneDriveReader._construct_endpoint")
def test_get_items_in_drive_with_maxretries(mock_construct_endpoint, mock_get, mocker):
    # Arrange
    access_token = "test_access_token"
    item_ref = "test_item"
    max_retries = 3
    mock_construct_endpoint.return_value = "constructed_endpoint"

    # Mock the response object that the requests.get method will return
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"data": "test_data"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    reader = OneDriveReader(client_id="test_client", tenant_id="test_tenant")

    # Act
    result = reader._get_items_in_drive_with_maxretries(
        access_token=access_token, item_ref=item_ref, max_retries=max_retries
    )

    # Assert
    mock_construct_endpoint.assert_called_once_with(item_ref, False, False, None)
    assert mock_get.call_count == 1
    assert result == {"data": "test_data"}


# Define a new fixture that will use parameters
@pytest.fixture(
    params=[
        # First scenario: successful data retrieval
        {
            "get_items_return_value": {"value": [{"id": "123", "file": {}}]},
            "expected_result": {"123": "metadata"},
            "raises": False,
        },
        # Second scenario: no data returned
        {
            "get_items_return_value": None,
            "expected_result": "Unable to retrieve items for: RootFolder",
            "raises": True,
        },
    ]
)
def mock_reader(request, mocker):
    # Use the parameters from 'request.param' to set the return values of the mocks
    mocker.patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._get_items_in_drive_with_maxretries",
        return_value=request.param["get_items_return_value"],
    )
    mocker.patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._check_approved_mimetype_and_download_file",
        return_value={"123": "metadata"},
    )

    reader = OneDriveReader(
        "client_id", "client_secret", "tenant_id"
    )  # Add necessary arguments for initialization
    return (
        reader,
        request.param,
    )  # Return both the reader and the current scenario's data


def test_connect_download_and_return_metadata_combined(mock_reader):
    reader, test_data = mock_reader  # Unpack the reader and the test data

    if test_data["raises"]:
        # If the scenario is expected to raise an exception, check this
        with pytest.raises(Exception, match=rf"{test_data['expected_result']}"):
            reader._connect_download_and_return_metadata("access_token", "local_dir")
    else:
        # If the scenario is not expected to raise, check the result
        result = reader._connect_download_and_return_metadata(
            "access_token", "local_dir"
        )
        assert result == test_data["expected_result"]


@pytest.fixture
def mock_methods():
    with patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._authenticate_with_msal",
        return_value="mocked_token",
    ), patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._connect_download_and_return_metadata"
    ) as mocked_connect, patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._get_items_in_drive_with_maxretries",
        return_value={},
    ), patch(
        "llama_hub.microsoft_onedrive.base.OneDriveReader._check_approved_mimetype_and_download_file",
        return_value={},
    ):
        yield mocked_connect  # this fixture returns the mocked _connect_download_and_return_metadata method


def test_from_root(mock_methods):
    reader = OneDriveReader("client_id", "client_secret", "tenant_id")
    reader._init_download_and_get_metadata("temp_dir")
    mock_methods.assert_called_once_with(
        "mocked_token",
        "temp_dir",
        "root",
        False,
        mime_types=None,
        userprincipalname=None,
    )


def test_with_folder_id(mock_methods):
    reader = OneDriveReader("client_id", "client_secret", "tenant_id")
    reader._init_download_and_get_metadata("temp_dir", folder_id="folder123")
    mock_methods.assert_called_once_with(
        "mocked_token",
        "temp_dir",
        "folder123",
        False,
        mime_types=None,
        userprincipalname=None,
    )


def test_with_file_ids(mock_methods):
    reader = OneDriveReader("client_id", "client_secret", "tenant_id")
    reader._init_download_and_get_metadata("temp_dir", file_ids=["file123"])
    mock_methods.assert_not_called()  # _connect_download_and_return_metadata should not be called for file IDs


def test_with_folder_path(mock_methods):
    reader = OneDriveReader("client_id", "client_secret", "tenant_id")
    reader._init_download_and_get_metadata("temp_dir", folder_path="/path/to/folder")
    mock_methods.assert_called_once_with(
        "mocked_token",
        "temp_dir",
        "/path/to/folder",
        False,
        mime_types=None,
        userprincipalname=None,
        isRelativePath=True,
    )


def test_with_file_paths(mock_methods):
    reader = OneDriveReader("client_id", "client_secret", "tenant_id")
    reader._init_download_and_get_metadata("temp_dir", file_paths=["/path/to/file"])
    mock_methods.assert_not_called()  # _connect_download_and_return_metadata should not be called for file paths
