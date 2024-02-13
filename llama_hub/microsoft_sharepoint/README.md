# Microsoft SharePoint Reader

The loader loads the files from a folder in sharepoint site.

It also supports traversing recursively through the sub-folders.

## Prequsites

### App Authentication using Microsoft Entra ID(formerly Azure AD)

1. You need to create an App Registeration in Microsoft Entra ID. Refer [here](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application)
2. API Permissions for the created app.
   1. Micorsoft Graph --> Application Permissions --> Sites.ReadAll (**Grant Admin Consent**)
   2. Microsoft Graph --> Application Permissions --> Files.ReadAll (**Grant Admin Consent**)
   3. Microsoft Graph --> Application Permissions --> BrowserSiteLists.Read.All (**Grant Admin Consent**)

More info on Microsoft Graph APIs - [Refer here](https://learn.microsoft.com/en-us/graph/permissions-reference)

## Usage

To use this loader `client_id`, `client_secret` and `tenant_id` of the registered app in Microsoft Azure Portal is required.

This loader can:
- Load files present in a specific folder in SharePoint
- Load all files present in the drive of a SharePoint
- Load all pages under a SharePoint site


If the files are present in the `Test` folder in SharePoint Site under `root` directory, then the input for the loader for  `file_path` is `Test`

![FilePath](file_path_info.png)

### Example loading all files and pages
If `sharepoint_folder_path` is not provided it defaults to `""`. 
In that case, the root folder of the SharePoint Drive is used as the folder to load files from. 

If both `sharepoint_folder_path` is not provided and `recursive` is set to `True`, all files in the SharePoint Drive are loaded. 
If `recursive` is not provided, it defaults to `False`. In this case, files from subfolders are not loaded. 

```python
from llama_index import download_loader 
SharePointLoader = download_loader("SharePointReader")

loader = SharePointLoader(
            client_id = "<Client ID of the app>",
            client_secret = "<Client Secret of the app>",
            tenant_id = "<Tenant ID of the Micorsoft Azure Directory>"
            )

documents = loader.load_data(
            sharepoint_site_name = "<Sharepoint Site Name>",
            recursive = True,
)
```

### Example loading a single folder
To load a single folder, specify the `sharepoint_folder_path` with the name of the folder or path from the root directory. 

Example: `sharepoint_folder_path = "my/folder/path"`

In order to load only the documents from this `sharepoint_folder_path`, and not the pages for the `sharepoint_site_name`, 
you need to provide the `include` argument as `['documents']`. By default, `include` is equal to `['documents', 'pages']`.

If you do not want to include files from subfolders for the given `sharepoint_folder_path`, remove the argument `recursive` (defaults to `False`). 

```python
from llama_index import download_loader 
SharePointLoader = download_loader("SharePointReader")

loader = SharePointLoader(
            client_id = "<Client ID of the app>",
            client_secret = "<Client Secret of the app>",
            tenant_id = "<Tenant ID of the Micorsoft Azure Directory>"
            )

documents = loader.load_data(
            sharepoint_site_name = "<Sharepoint Site Name>",
            sharepoint_folder_path = "<Folder Path>",
            recursive = True,
            include = ['documents']
)
```



### Example loading just pages
In order to load only the pages for the `sharepoint_site_name`, 
you need to provide the `include` argument as `['pages']`. By default, `include` is equal to `['documents', 'pages']`.

Note: `recursive` and `sharepoint_folder_path` arguments have no effect if `documents` is not in the list of the argument `include`.

```python
from llama_index import download_loader 
SharePointLoader = download_loader("SharePointReader")

loader = SharePointLoader(
            client_id = "<Client ID of the app>",
            client_secret = "<Client Secret of the app>",
            tenant_id = "<Tenant ID of the Micorsoft Azure Directory>"
            )

documents = loader.load_data(
            sharepoint_site_name = "<Sharepoint Site Name>",
            include = ['pages']
)
```

### Example loading just documents
```python
from llama_index import download_loader 
SharePointLoader = download_loader("SharePointReader")

loader = SharePointLoader(
            client_id = "<Client ID of the app>",
            client_secret = "<Client Secret of the app>",
            tenant_id = "<Tenant ID of the Micorsoft Azure Directory>"
            )

documents = loader.load_data(
            sharepoint_site_name = "<Sharepoint Site Name>",
            recursive = True,
            include = ['documents']
)
```

### Example loading just documents with filetype .docx or .pdf

If you want to only load specific filetypes, provide the file extension names in `file_types`. 
Example: to only include .pdf and .docx files, set `file_types` to `['docx', 'pdf']`

```python
from llama_index import download_loader 
SharePointLoader = download_loader("SharePointReader")

loader = SharePointLoader(
            client_id = "<Client ID of the app>",
            client_secret = "<Client Secret of the app>",
            tenant_id = "<Tenant ID of the Micorsoft Azure Directory>"
            )

documents = loader.load_data(
            sharepoint_site_name = "<Sharepoint Site Name>",
            recursive = True,
            include = ['documents'],
            file_types = ['docx', 'pdf']
)
```

The loader doesn't access other components of the `SharePoint Site`.

