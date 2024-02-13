from typing import List, Optional

import json
import requests
from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class OpsgenieReader(BaseReader):
    """
    Opsgenie Reader. Get alerts from Opsgenie.
    """

    def __init__(
        self, api_key: str, api_url: str, max_alerts: Optional[int] = 300
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"GenieKey {self.api_key}",
            "Content-Type": "application/json",
        }
        self.max_alerts = max_alerts

    def load_data(self) -> List[Document]:
        """Load data by calling Opsgenie alerts API.

        Returns:
            List of alerts.
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
        """Get all alerts from Opsgenie."""

        all_alerts = []
        list_alerts_url = f"{self.api_url}/v2/alerts"

        print(f"max_alerts: {self.max_alerts}")

        while list_alerts_url and len(all_alerts) <= self.max_alerts:
            print(f"Alerts read so far {len(all_alerts)}")
            print(f"Retrieving alerts from {list_alerts_url}")
            response = requests.get(
                list_alerts_url, headers=self.headers, params={}, timeout=30
            )
            if response.status_code == 200:
                alerts = response.json()
                all_alerts.extend(alerts.get("data", []))
                paging = alerts["paging"]
                try:
                    list_alerts_url = paging["next"]
                except KeyError:
                    list_alerts_url = None
            else:
                raise ValueError(
                    f"Problem getting list of alerts from Opsgenie.Error: {response.status_code}, {response.text}"
                )

        print(f"Final Total alerts retrieved: {len(all_alerts)}")

        return all_alerts

    def get_alert_details(self, alert_id):
        """Get alert detail"""

        response = requests.get(
            f"{self.api_url}/v2/alerts/{alert_id}", headers=self.headers, timeout=30
        )

        if response.status_code == 200:
            details = response.json().get("data", {})
            return details
        else:
            raise ValueError(
                f"Problem getting alert details for {alert_id} from Opsgenie .Error: {response.status_code}, {response.text}"
            )
