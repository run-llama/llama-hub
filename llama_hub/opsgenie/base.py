from typing import List, Optional

import json
import requests
from llama_index.readers.base import BaseReader
from llama_index.schema import Document

class OpsgenieReader(BaseReader):
    """
    Opsgenie Reader. Get open alerts from Opsgenie.
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 api_url: Optional[str] = None
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"GenieKey {self.api_key}",
            "Content-Type": "application/json",
        }
        self.params = {
            'query': 'status:open'
        }

    def load_data(self) -> List[Document]:
        """Load data from Opsgenie API.

        Args:
            query: Query to be passed to Opsgenie API.

        Returns:
            List of documents.
        """
        alerts = []
        all_opsgenie_alerts = self.get_all_alerts()
        if all_opsgenie_alerts:
            for opsgenie_alert in all_opsgenie_alerts:
                alert_id = opsgenie_alert["id"]
                details = self.get_alert_details(alert_id)
                alert = Document(text=json.dumps(details))
                alerts.append(alert)

        return alerts
    
    def get_all_alerts(self):
        response = requests.get(
            f"{self.api_url}/v2/alerts", headers=self.headers, params=self.params, timeout=30)

        if response.status_code == 200:
            alerts = response.json().get("data", [])
            return alerts
        else:
            raise ValueError("Problem getting list of alerts from Opsgenie. Check API key and URL.")

    def get_alert_details(self, alert_id):
        response = requests.get(
            f"{self.api_url}/v2/alerts/{alert_id}", headers=self.headers, timeout=30)

        if response.status_code == 200:
            details = response.json().get("data", {})
            return details
        else:
            raise ValueError("Problem getting alert details for alert_id from Opsgenie. Check API key and URL.")
