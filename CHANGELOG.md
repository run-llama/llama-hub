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