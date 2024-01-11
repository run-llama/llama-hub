# ChangeLog

## v[0.0.70] - 2024-01-11

### New Features
- add semantic chunker llama pack (#853)
- Feature/add agent search (#844)

## v[0.0.69] - 2024-01-08

### New Features
- add rag fusion query pipeline pack (#847)

## v[0.0.67] - 2024-01-07

### Security Fix
- Fixed security flaw when loading yaml, should always use `yaml.safe_load()` (#841)

## v[0.0.66] - 2024-01-04

### New Features
- add ragatouille pack  (#836)
- TelegramLoader (#822)

### Smaller Features + Bug Fixes / Nits
- handle bytestring (#834)
- Slack Tool: Fix "fn_schema is None" issue (#824)
-  Wikipedia tools should return text, not documents (Tools aren't DataLoaders!) (#828)
- Fixing JsonReader and introducing unit tests (#816)
- Fix:dense pack naming error in usage example notebook (#831)
- chore: get the full detailed text from Confluence (#809)
- feat: fix folder name and add keywords (#829)

## v[0.0.65] - 2023-12-29

### New Features
- Add Powerpoint Slide Loader PptxSlideReader to LLama-hub (#796)
- Added notebook for llama_guard_moderator pack (#814)
- add llm compiler pack  (#820)

### Smaller Features + Bug Fixes / Nits 
- docs: Address branding issues of Apache OpenDAL (#817)

## v[0.0.63] - 2023-12-22

### New Features
- add multi doc autoretrieval pack (#803) 

### Smaller Features + Bug Fixes / Nits
- Extract metadata from Azure BLOB (#804)

## v[0.0.62] - 2023-12-21

### New Features

- Add `MiniEsgBenchDataset` (#799)
- Add `PDFPlubmerReader` (#798)
- Add Cogniswitch llama pack and update Cogniswitch tool (#797)

### Smaller Features + Bug Fixes / Nits

- Improved s3Reader to move control where files are downloaded (#788)

## v[0.0.61] - 2023-12-20

- Add `MiniMtBenchSingleGradingDataset` & `MtBenchHumanJudgementDataset` (#782)
- Add `EvaluatorBenchmarkerPack` (#777)

### Smaller Features + Bug Fixes / Nits

- backwards compatibility import `ResumeScreenerPack`, `GmailOpenAIAgentPack`, `Neo4jQueryToolSpec`

## v[0.0.60] - 2023-12-16

### New Features

- Add `NebulaGraphQueryEnginePack` and `SnowflakeQueryEnginePack` (#776)

### Smaller Features + Bug Fixes / Nits

- Fix ui-breaking entry in library.json - authors can only be string (#779)

## [v0.0.59] - 2023-12-15

### Smaller Features + Bug Fixes / Nits

- Fix bugs in StreamlitChatPack (#772)
- NOTE: using "postX" as release version doesn't get picked up ui 

## [v0.0.58] - 2023-12-13

### New Features

- Logan/dense x retrieval (#769)
- add new Hive reader (#753)

### Smaller Features + Bug Fixes / Nits

- Update AzStorageBlobReader (#756)

## [v0.0.57] - 2023-12-12

### New Features

- Add Astra DB loader (#764)
- Add `DocugamiKgRagSec10Q` dataset (#767)

## [v0.0.56] - 2023-12-09

### New Features

- Create llama_packs_neo4j.ipynb (#744)
- Add Panel Chat Pack (#703) 
- Add AlexNet dataset (#750)
- Adding SnowflakeReader (#754) 
- Microsoft SharePoint Data Loader  (#745)

### Smaller Featuers + Bug Fixes / Nits

- Added fix to run SQL query function description (#729)
- add basic checks for datasets library (#746)
- added colab badge in neo4j test notebook (#747)
- Update pandas excel reader (#752)
- Implemented start and cursor support for confluence loader (#733)

## [v0.0.55] - 2023-12-07

### New Features

- add `CovidQaDataset` and `MiniCovidQaDataset` (#738)

### Smaller Features + Bug Fixes / Nits
- nit: remove print statements from ollama pack (#741)

## [v0.0.54] - 2023-12-06

### New Features

- Add batch execution controlled by `batch_size` and `sleep_time_in_seconds` to `RagEvaluatorPack` (#734)

## [v0.0.53] - 2023-12-05

### New Features

- added Neo4j query engine pack (#709)
- Vectara RAG pack (#661)
- feat: add StripeDocsReader loader (#684)
- Vectara rag bugfix (#732)
- Issue#667: New Ollama Query Engine pack (#731)
- add document_loader and cache (#687)

- Update Confluence loader with capability to set start and cursor offset when searching (#733)

## [v0.0.52] - 2023-12-04

### New Features

- Add `EvaluatingLlmSurveyPaperDataset` (#725)
- Add `OriginOfCovid19Dataset` (#723)

### Smaller Features + Bug Fixes / NITs

- Add citation to `MiniTruthfulQADataset` README (#726)
- Fix link to submission template nb in datasets README (#724)

## [v0.0.51] - 2023-12-03

### New Features

- add uber 10k dataset (#716)
- add llama2 dataset (#691)
- Add `MiniSquadV2Dataset` (#720)
- Add `MiniTruthfulQADataset` (#713)
- Add `LlamaDatasetMetadataPack` (#707)
- Add README template for Datasets (#702)
- Modify RagEvaluatorPack to handle missing reference_contexts (#698)
- Add async and sync run methods to RagEvaluatorPack (#697)
- Add Patronus AI Finance Bench Mini Dataset (#688)
- Add Braintrust Coda HelpDesk dataset (#686)
- Add RagEvaluatorPack (#683)
- New data loader - Opensearch (#672)
- AddMainContentExtractorReader (#679)
- Add `Datasets` structure with initial PaulGrahamEssayDataset (#669)

### Smaller Features + Bug Fixes

- Update main README to include info on llama-datasets (#711)
- Add missing README to `LlamaDatasetMetadataPack` (#708)
- Image reader was ignoring metadata. Added metadata to loaded ImageDocument (#668)
- Add Cypher validation to Neo4j db tool (#660)
- feat: Improvements to Chroma loader (#673)
- Adding Earning Call transcripts of US based companies (#658)

## [v0.0.50] - 2023-11-28

### New Features
- add amazon product extraction (#670)
- Add Waii connector (#647)

## [v0.0.49] - 2023-11-27

### New Features
- Citation LlamaPack (#666)

## [v0.0.48] - 2023-11-27

### New Features
- Add some advanced retrieval llama packs  (#659)

## [v0.0.46] - 2023-11-22

### New Features
- Add Llama Packs (#646)
- Unstructured.IO API support (#648)

## [v0.0.45] - 2023-11-16

### Smaller Features + Bug Fixes
- Updated init file (#633)
- fIMDB Movie reviews bug fixes and feature addition (#636)
- replace s/gpt_index/llama_index references in READMEs (#635) 

## [v0.0.44] - 2023-11-13

### Smaller Features + Bug Fixes
- Extend GoogleSheetsReader to Accept Custom Text Column Names (#620)
- feat: sync mongo to SimpleMongoReader of llama-index (#624)
- Adding moview reviews link for IMDB loader (#630)

## [v0.0.43] - 2023-11-1

### Smaller Features + Bug Fixes
- Update tavily requirements (#618)
- fix tavily tool (#617)

## [v0.0.42] - 2023-10-31

### New Features
- Add a Lilac dataset reader. (#563)

### Smaller Features + Bug Fixes
- Cogniswitch llama-hub corrections (#613)
- name change and README update to Tavily (#614)

## [v0.0.41] - 2023-10-30

### New Features
- CogniSwitch Connector (#604) 

### Smaller Features + Bug Fixes
- add docs to min_chunk_size (#607)
- Change Tavily client name (#609)

## [v0.0.40] - 2023-10-26

### New Features
- Added OpenAlex Reader for Scientific QA (#599)
- Added Tavily Search API as a tool (#600)
- Adding loader to read from OneDrive Personal and OneDrive for Business (#597)

### Smaller Features + Bug Fixes
- Update TrafilaturaWebReader in library.json (#602) 

## [v0.0.39] - 2023-10-24

### New Features
- Added smart layout aware fast PDF reader/loader (#587)
- Added Protein Data Bank citation reader (#595) 

### Smaller Features + Bug Fixes
- Fix Firestore client info (#586) 
- doc(README): remove typo (#589)
- Add model kwargs to image loader (#588)
- updating documentation to match method defaults (#591)
- doc(README): Fix Grammatical Error (#593)
- Fix import statement for CodeInterpreterToolSpec (#594) 

## [v0.0.38] - 2023-10-16

### New Features
- IMDB Review loader (#571) 
- Add AWS Athena Reader (#579)
- add PatentsviewReader for reading patent abstract (#582) 

### Smaller Features + Bug Fixes
- Add proper __init__.py files (#581)
- Add possibility to pass model kwargs to image loader models

## [v0.0.37] - 2023-10-09

### New Features
- Add Nougat OCR loader (#541)

### Smaller Features + Bug Fixes
- improve bitbucket loader and extension to skip (#576)

## [v0.0.36] - 2023-10-07

### New Features
- Add RayyanLoader to fetch review articles from Rayyan (#570)
- added bitbucket loader (#572)

### Smaller Features + Bug Fixes
- fix: credentials path and readme improvement (#567)
- fix: pdf google drive (#568)
- Updating URLs in Wikipedia Loader (#569)

### [v0.0.35] - 2023-10-05
- Loader for Macrometa GDN (#484)
- adding boto3 minio doc loader (#497)
- Add new data reader: AssemblyAIAudioTranscriptReader (#562)

### Smaller Features + Bug Fixes
- fix: PyMuPDF Reader broken (#547)
- Add page id to extra_info (#542) 
- Update: Readme with corrected example url for Playgrounds_subgraph_connector tool (#551)
- add url and status to confluence loader document (#553)
- Changes from llama_index/PR#7906 (#557)
- fix: sql_wrapper utilities (#558)
- Adding functionality for AsanaReader (#386)
- Add JSONL functionality to JSONReader (#552)
- add url and timestamp to slack loader documents metadata (#559)
- add url to asana loader docs (#560)
- Added oAuth to Jira loader (#272)
- refactor: add custom path for download_loader to enable functionality (#318)

## [v0.0.34] - 2023-09-27

### New Features
- feat: Add PlaygroundsSubgraphInspectorToolSpec to llama_hub (#535)
- add full formatting and linting (#537, #538)
- Add new data reader: AssemblyAIAudioTranscriptReader (#562)

### Smaller Features + Bug Fixes
- fix: added missing loaders removed from a old PR (#540)
- break loop if API error for slack reader (#544)  
- mbox: allow custom, stable document id (#393)
- update database doc (#531)
- fix: jsondata loader on library (#539)
- fix: remove isort due using black and add a new checklist (#546)

## [v0.0.33] - 2023-09-24

### New Features
- Neo4j Schema Query Builder Integration (#520)

## [v0.0.32] - 2023-09-22

### New Features
- feat: Add PlaygroundsSubgraphConnector to Llama Hub (#528)

### Smaller Features + Bug Fixes
- Fix BaseGithubClient and _generate_documents (#526)
- Refactor load_data for consistent sheet handling and cleaner code (#488)
- remove redundant if/else from imports in github readers (#524)
- fix: 🚑️ remove app id and secret from feishu reader (#525)

## [v0.0.31] - 2023-09-18

### New Features
- Add reader for GitHub collaborators (#512)
- HWPReader (#517)

### Smaller Features + Bug Fixes
- fixed typos in the readme.md of salesforce tool (#515)
- Service account support for google drive loader (#513)
- Enhance PDFReader to accept File object as well, in addition to a path string (#514)
- add urls to metadata saved by github repo reader (#522)

## [v0.0.30] - 2023-09-12

### New Features
- Elastic data reader (#508)
- Salesforce Tool (#507)

### Smaller Features + Bug Fixes
- add HWPReader to JSON (#500)
- Add issue labels to `extra_info` saved by GithubRepositoryIssuesReader (#502)

## [v0.0.29] - 2023-09-08

### New Features
- Adding MultiOn browsing tool (#481)

## [v0.0.28] - 2023-09-08

### Smaller Features + Bug Fixes
- fix olefile import 

## [v0.0.27] - 2023-09-07

### New Feature Releases

- add hanguel / hwp readers (#493)
- Enhancement to Semantic Scholar Loader - full text reader (#482)
- Adding hierarchical agent example and comparison (#495)

### Smaller Features + Bug Fixes
- fix transforming error in wordlift reader (#501)

## [v0.0.26] - 2023-08-31

(includes v0.0.25)

### New Feature Releases
- Add Linear loader (#490)
- Add PDF Table Reader (#476)
- Bagel loader Added (#479)

### Smaller Features + Bug Fixes
- Database arg fix in Firestore client (#483)
- Some update to prevent errors when transforming data in wordlift loader (#489)
- UTF-8 encode and decode for gmail (#491)
- iterate json data to Document object in unstructured loader (#485)
- add custom user agent for metaphor llama index initialization (#480)
- Fix Syntax in Docs (#478)

## [v0.0.24] - 2023-08-20

### New Feature Release
- Adding Metaphor tool and notebook (#466)

## [v0.0.23] - 2023-08-17

### New Feature Release
- Adding ArXiv tool spec (#464)

## [v0.0.22] - 2023-08-15

### New Feature Releases
-  Adding Azure speech, translate and CV tools (#459)
- SDLReader for Graphql (#461)

### Smaller Features + Bug Fixes
- missing import added for wikipedia (#463)
- patch document in wordpress (#462)

## [v0.0.21] - 2023-08-10

### New Feature Releases
- ZepReader (#452)
- GraphQL Tool Spec (#455)
- Adding PythonFileToolSpec (#453)
- Adding bing search tools (#457)
- RSS Feed / OPML reader and article parser (#444)

## [v0.0.20] - 2023-08-09

### New Feature Release
- Adding Shopify GraphQL Tool Spec and Demo (#442)

### Smaller Features + Bug Fixes
- changed num to init for better declaration in google search tool (#449)

## [v0.0.19] - 2023-08-07

### Smaller Features + Bug Fixes
- added a num parameter to the google_search (#446)

## [v0.0.18] - 2023-08-04

### New Feature Release
- Added Semantic scholar reader (#439)

### Smaller Features + Bug Fixes
- Update docugami loader notebook (#445)
- Remove release workflow in favor of using tags (#443)

## [v0.0.17] - 2023-08-02

### New Feature Release
- Auto-Tool creation notebook (#424)

### Smaller Features + Bug Fixes
- Security warning for Code Interpreter and lock requests headers to a domain (#438)
- A few more tags based on GA (#437)
- Add publish release workflow (#436)
- add retrieval augmented text-to-image example (#434)
- hatena blog reader add url (#425)
- adding more functions to DeepDoctectionReader and docs (#431)

## [v0.0.16] - 2023-07-30

### New Feature Release
- Gurureader (#427)
- feat: minio loader (#430)
- Adding SEC Filings Loader (#415)
- Adding some tags for llama hub searches (#422)

### Smaller Features + Bug Fixes 
- Update unstructured loader README (#418)
- synced with llama_index/readers/file/markdown_reader.py (#388)
- YoutubeTranscriptReader tests (#412)
- fix some bugs in WordLift loader (#421)

## [v0.0.15] - 2023-07-25

### New Feature Release
- Adding ChatGPT plugin tool (#405)

## [v0.0.14] - 2023-07-22
### New Feature Release
- Adding Dalle2 text to image tool (#407)
- Add SingleStoreReader (#404)

### Smaller Features + Bug Fixes
- Update GmailReader to return internalDate (#406)
- Update ChromaReader to use 0.4.0 API (#394)
- Update Zapier to expose a list of tools (#401)


## [v0.0.12] - 2023-07-17

### New Feature Release
- Add code interpreter tool (#398)
- Add Feishu Docs Reader (#383)
- Add Google Keep reader (#370)

### Smaller Features + Bug Fixes
- Various bug fix and improvements to pandas excel reader (#397, #372, #391)
- Update README.md to better highlight data agents (#395)
- Update Zapier tool to use parameters in addition to instructions (#390)
- Make S3Reader more configurable (#364)

## [v0.0.11] - 2023-07-13

### New Feature Release
- Add weather agent tool (#384) 

### Smaller Features + Bug Fixes
- fix tool readme imports (#381)
- fix tool notebooks (#380)
- fix gmail notebook  (#379)

## [v0.0.10] - 2023-07-12


### New Feature Release
- Adding Agent Tools to LlamaHub (#377)

### Smaller features + Bug Fixes 
- Docugami: use metadata over deprecated extra_info (#375)

## [v0.0.9] - 2023-07-09

### Smaller features + Bug Fixes
- change readme and requirements (#354)
- Update zendesk loader (#358)
- Remove ascii in gmail loader (#361)
- Fix readme for wordlift (#357)
- address bug in paginated loader that always fetches the next page, even if the max_results is met (#363)
- S3 Extensions Filtering (#362)
- Add argument encoding to specify the encoding to open the csv file. (#367)
- Update README.md for unstructured (#366)
- fix bug where messages are returned without getting message data (#368)

## [v0.0.8] - 2023-07-04

### New Loaders
- Add firebase realtime db (#347)
- Add WordLift Loader (#346)

### Bug Fixes
- [bugfix] replace None to empty string to avoid TypeError (#351)
- chore: add youtube_id to document metadata (#352)

## [v0.0.7] - 2023-07-01

### Smaller features + Bug Fixes
- Add extra_info with Source to web reader (#337)
- support pagination on gmail loader (#348)


## [v0.0.6] - 2023-06-28

### Smaller features + Bug Fixes
- feat: add source metadata to documents created by the GH issues reader (#341)
- Update markdown reader (#344)
- ensure metadata always valid (#343)

## [v0.0.5] - 2023-06-26

### Major (Breaking) Changes
- update document usage (#338). NOTE: all Document objects must be prefixed with a `kwargs` field.

### New Loaders
- feat: add document reader for GH issues (#332)
- Add sitemap loader (#328)

### Bug Fixes
- Fixed ValueError: Metadata key must be str! error (#317)
- update namespace (#324)
- add changelog (#333)
- Fix KibelaReader (#334)
- confluence.load_data new features, bug fixes, tests (#330)
- Update readme files for reference (#336)


## [v0.0.4] - 2023-06-25

### New Loaders
- Add KibelaReader (#319)
- reader: add deplot tabular graph image reader (#321)

### Minor Changes / Bug Fixes
- support Confluence personal access token (#323)
- service account credentials (#316)

### Breaking/Deprecated API Changes
- None
 
### Miscellaneous 
- None
