"""Kaltura eSearch API Reader."""
import requests
import logging
import json
from typing import Optional, List, Dict, Any
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

logger = logging.getLogger(__name__)

class KalturaESearchReader(BaseReader):
    """Kaltura eSearch API Reader."""
    def __init__(
        self,
        partnerId: str = "INSERT_YOUR_PARTNER_ID",
        apiSecret: str = "INSERT_YOUR_ADMIN_SECRET",
        userId: str = "INSERT_YOUR_USER_ID",
        ksType: int = 2,  # Default to KalturaSessionType.ADMIN, ksType set in _load_kaltura
        ksExpiry: int = 86400,
        ksPrivileges: str = "disableentitlement",
        kalturaApiEndpoint: str = "https://cdnapi-ev.kaltura.com/",
        requestTimeout: int = 500,
        shouldLogApiCalls: bool = False
    ) -> None:
        """Initialize with parameters."""
        self.partnerId = partnerId
        self.apiSecret = apiSecret
        self.userId = userId
        self.ksType = ksType
        self.ksExpiry = ksExpiry
        self.ksPrivileges = ksPrivileges
        self.kalturaApiEndpoint = kalturaApiEndpoint
        self.requestTimeout = requestTimeout
        self.shouldLogApiCalls = shouldLogApiCalls
        # Kaltura libraries will be loaded when they are needed
        self._kaltura_loaded = False

    def _load_kaltura(self):
        """Load Kaltura libraries."""
        from KalturaClient import KalturaClient
        from KalturaClient.Base import IKalturaLogger, KalturaConfiguration
        from KalturaClient.Plugins.Core import KalturaSessionType
        
        class KalturaLogger(IKalturaLogger):
            def log(self, msg):
                logging.info(msg)

        self.config = KalturaConfiguration(self.partnerId)
        self.config.requestTimeout = self.requestTimeout
        self.config.serviceUrl = self.kalturaApiEndpoint
        if self.shouldLogApiCalls:
            self.config.setLogger(KalturaLogger())
        self.client = KalturaClient(self.config)
        if self.ksType is None:
            self.ksType = KalturaSessionType.ADMIN
        self.ks = self.client.generateSessionV2(
            self.apiSecret,
            self.userId,
            self.ksType,
            self.partnerId,
            self.ksExpiry,
            self.ksPrivileges
        )
        self.client.setKs(self.ks)
        self._kaltura_loaded = True
    
    def _load_from_search_params(self, search_params, 
                                 withCaptions: bool = True, 
                                 maxEntries: int = 10) -> List[Dict[str, Any]]:
        from KalturaClient.Plugins.Core import KalturaPager
        try:
            entries = []
            pager = KalturaPager()
            pager.pageIndex = 1
            pager.pageSize = maxEntries
            response = self.client.elasticSearch.eSearch.searchEntry(search_params, pager)
            for searchResult in response.objects:
                entry = searchResult.object
                itemsData = searchResult.itemsData
                entry_info = {
                    'entry_id': str(entry.id),
                    'entry_reference_id': str(entry.referenceId),
                    'entry_media_type': entry.mediaType.value
                }
                entry_dict = {
                    'entry_id': str(entry.id),
                    'entry_name': str(entry.name),
                    'entry_description': str(entry.description),
                    'entry_media_type': entry.mediaType.value,
                    'entry_media_date': int(entry.createdAt),
                    'entry_ms_duration': int(entry.msDuration),
                    'entry_last_played_at': int(entry.lastPlayedAt),
                    'entry_application': str(entry.application),
                    'entry_tags': str(entry.tags),
                    'entry_reference_id': str(entry.referenceId)
                }
                if withCaptions == True:
                    entry_dict['entry_captions'] = self._get_captions(itemsData)
                entry_dict_json_string = json.dumps(entry_dict)
                # Create a LlamaIndex Document object
                entry_doc = Document(text=entry_dict_json_string, extra_info=entry_info)
                entries.append(entry_doc)
            return entries
        except Exception as e:
            logger.error('An error occurred while loading with search params: {}'.format(e))
            return []

    def _get_captions(self, itemsData):
        try:
            for captionSearchResult in itemsData[0].items:
                capId = captionSearchResult.captionAssetId
                capJsonUrl = self.client.caption.captionAsset.serveAsJson(capId)
                capJson = requests.get(capJsonUrl).json()
                return capJson
        except Exception as e:
            logger.error('An error occurred while getting captions: {}'.format(e))
            return {}
  
    def load_data(self, 
              search_params: Any = None,
              search_operator_and: bool = True, 
              free_text: Optional[str] = None, 
              category_ids: Optional[str] = None, 
              with_captions: bool = True, 
              max_entries: int = 5
             ) -> List[Dict[str, Any]]:
        """Load data from the Kaltura based on search parameters. 
        The function returns a list of dictionaries. 
        Each dictionary represents a media entry, where the keys are strings (field names) and the values can be of any type.

        Args:
            search_params: search parameters of type KalturaESearchEntryParams with pre-set search queries. If not provided, the other parameters will be used to construct the search query.
            search_operator_and: if True, the constructed search query will have AND operator between query filters, if False, the operator will be OR.
            free_text: if provided, will be used as the free text query of the search in Kaltura.
            category_ids: if provided, will only search for entries that are found inside these category ids.
            withCaptions: determines whether or not to also download captions/transcript contents from Kaltura.
            maxEntries: sets the maximum number of entries to pull from Kaltura, between 0 to 500 (max pageSize in Kaltura).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing Kaltura Media Entries with the following fields: 
            entry_id:str, entry_name:str, entry_description:str, entry_captions:JSON, 
            entry_media_type:int, entry_media_date:int, entry_ms_duration:int, entry_last_played_at:int, 
            entry_application:str, entry_tags:str, entry_reference_id:str. 
        """
        from KalturaClient.Plugins.ElasticSearch import (
            KalturaESearchCaptionItem, KalturaESearchCaptionFieldName, KalturaESearchUnifiedItem, 
            KalturaESearchEntryParams, KalturaESearchCategoryEntryItem, KalturaESearchEntryOperator, 
            KalturaESearchOperatorType, KalturaESearchItemType, KalturaCategoryEntryStatus, KalturaESearchCategoryEntryFieldName
        )

        # Load and initialize the Kaltura client
        if not self._kaltura_loaded:
            self._load_kaltura()

        # Validate input parameters:
        if search_params is None:
            search_params = KalturaESearchEntryParams()
            # Create an AND/OR relationship between the following search queries - 
            search_params.searchOperator = KalturaESearchEntryOperator()
            if search_operator_and:
                search_params.searchOperator.operator = KalturaESearchOperatorType.AND_OP
            else:
                search_params.searchOperator.operator = KalturaESearchOperatorType.OR_OP
            search_params.searchOperator.searchItems = []
            # Find only entries that have captions -
            if with_captions:
                caption_item = KalturaESearchCaptionItem()
                caption_item.fieldName = KalturaESearchCaptionFieldName.CONTENT
                caption_item.itemType = KalturaESearchItemType.EXISTS
                search_params.searchOperator.searchItems.append(caption_item)
            # Find only entries that are inside these category IDs - 
            if category_ids is not None:
                category_item = KalturaESearchCategoryEntryItem()
                category_item.categoryEntryStatus = KalturaCategoryEntryStatus.ACTIVE
                category_item.fieldName = KalturaESearchCategoryEntryFieldName.FULL_IDS
                category_item.addHighlight = False
                category_item.itemType = KalturaESearchItemType.EXACT_MATCH
                category_item.searchTerm = category_ids
                search_params.searchOperator.searchItems.append(category_item)
            # Find only entries that has this freeText found in them -
            if free_text is not None:
                unified_item = KalturaESearchUnifiedItem()
                unified_item.searchTerm = free_text
                unified_item.itemType = KalturaESearchItemType.PARTIAL
                search_params.searchOperator.searchItems.append(unified_item)
        
        return self._load_from_search_params(search_params, with_captions, max_entries)