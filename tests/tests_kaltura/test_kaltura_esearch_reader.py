import os

import pytest

from llama_hub.kaltura.esearch.base import KalturaESearchReader

# Kaltura credentials
PARTNER_ID: int = int(os.getenv("KALTURA_PARTNER_ID", 0))
API_SECRET: str = os.getenv("KALTURA_API_SECRET", "")
USER_ID: str = "LlamaTester"
KS_TYPE: int = 2
KS_EXPIRY: int = 86400
KS_PRIVILEGES: str = "disableentitlement"
KALTURA_API_ENDPOINT: str = "https://cdnapi-ev.kaltura.com/"
REQUEST_TIMEOUT: int = 500
SHOULD_LOG_API_CALLS: bool = True
MAX_ENTRIES = 1  # how many entries to load (pageSize)


class TestKalturaESearchReader:
    def test_kaltura_reader_simple_search(self):
        reader = KalturaESearchReader(
            partner_id=PARTNER_ID,
            api_secret=API_SECRET,
            user_id=USER_ID,
            ks_type=KS_TYPE,
            ks_expiry=KS_EXPIRY,
            ks_privileges=KS_PRIVILEGES,
            kaltura_api_endpoint=KALTURA_API_ENDPOINT,
            request_timeout=REQUEST_TIMEOUT,
            should_log_api_calls=SHOULD_LOG_API_CALLS,
        )
        entry_docs = reader.load_data(
            search_operator_and=True,
            free_text="education",
            category_ids=None,
            with_captions=True,
            max_entries=MAX_ENTRIES,
        )
        # test that we indeed gotten the number of entries we asked for -
        assert len(entry_docs) == MAX_ENTRIES

    def test_kaltura_reader_load_data_invalid_args(self):
        faulty_reader = KalturaESearchReader(
            partner_id=0, api_secret="willfail", user_id="somefaileduser"
        )

        with pytest.raises(
            ValueError,
            match="Kaltura Auth failed, check your credentials",
        ):
            faulty_reader.load_data(search_operator_and=True, free_text="education")
