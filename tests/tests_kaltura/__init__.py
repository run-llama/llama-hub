import os

import pytest

# tests changes to KalturaESearchReader.
# Skip this test if the Kaltura env vars don't exist
if not os.environ.get("KALTURA_PARTNER_ID") or not os.environ.get("KALTURA_API_SECRET"):
    pytest.skip(
        "Skipped Kaltura tests due to dependence on network request and Kaltura api"
        " secret that were not setup in env vars.",
        allow_module_level=True,
    )
