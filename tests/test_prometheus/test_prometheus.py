from llama_hub.prometheus import PrometheusReader
from datetime import datetime, timedelta


def test_prometheus_reader_with_query_range(mocker) -> None:
    end_time = datetime.utcnow() - timedelta(days=1)
    start_time = end_time - timedelta(hours=1)
    mocked_metric_data = [
        {
            "metric": {
                "endpoint": "http-metrics",
                "metric_name": "test_metric",
                "pod": "test-pod",
            },
            "values": [],
        }
    ]
    for metric_info in mocked_metric_data:
        for i in range(0, 60, 5):
            timestamp = int((start_time + timedelta(minutes=i)).timestamp())
            metric_info["values"].append([timestamp, i * 100])

    mocker.patch(
        "prometheus_api_client.PrometheusConnect.custom_query_range",
        return_value=mocked_metric_data,
    )
    reader = PrometheusReader(endpoint="test-endpoint", size=100)

    query = "avg_over_time(test_metric[5m])"

    documents = reader.load_data(query=query, start_time=start_time, end_time=end_time)
    assert len(documents) == 12
    for doc in range(0, len(documents)):
        assert documents[doc].text == str(doc * 5 * 100)


def test_prometheus_reader_with_query(mocker) -> None:
    mocked_metric_data = [
        {
            "metric": {
                "Name": "/dev_cicd_test1",
                "metric_name": "docker_memory_usage",
                "host": "dl1.dockerserver.com",
                "offering": "docker",
            },
            "values": [
                [1706898840, "338149320.8186831"],
                [1706898900, "338146802.62924147"],
                [1706898960, "281811971.070067"],
                [1706899020, "281813920.81963813"],
                [1706899080, "225405325.11296228"],
                [1706899140, "281780621.1695041"],
                [1706899200, "281800467.21272033"],
                [1706899260, "338153045.11319935"],
                [1706899320, "338145581.4473358"],
                [1706899380, "338119211.1141539"],
            ],
        },
        {
            "metric": {
                "Name": "/prod_cicd_test2",
                "metric_name": "docker_memory_usage",
                "host": "dl1.dockerserver.com",
                "offering": "docker",
            },
            "values": [
                [1706898840, "106213135.11232835"],
                [1706898900, "106212621.7800675"],
                [1706898960, "106221285.85705297"],
                [1706899020, "79666690.5925202"],
                [1706899080, "79650036.00729768"],
                [1706899140, "106208946.49888971"],
                [1706899200, "106216536.73648405"],
                [1706899260, "79660663.82172346"],
                [1706899320, "106211849.69262712"],
                [1706899380, "53101858.29009599"],
            ],
        },
    ]
    mocker.patch(
        "prometheus_api_client.PrometheusConnect.custom_query",
        return_value=mocked_metric_data,
    )
    reader = PrometheusReader(endpoint="test-endpoint", size=100)
    query = "rate(docker_memory_usage[5m])"
    metadata_fields = ["Name", "metric_name", "host", "offering"]
    documents = reader.load_data(
        query=query,
        metadata_fields=metadata_fields,
    )
    assert len(documents) == 20
    for doc in documents:
        field_count = 0
        for field in doc.metadata.keys():
            if field in metadata_fields:
                field_count += 1
        assert field_count == len(metadata_fields)


def test_prometheus_reader_with_empty_result(mocker) -> None:
    mocked_metric_data = []
    mocker.patch(
        "prometheus_api_client.PrometheusConnect.custom_query",
        return_value=mocked_metric_data,
    )
    reader = PrometheusReader(endpoint="test-endpoint", size=100)
    query = "rate(non_existing_metric[1m])"
    documents = reader.load_data(query=query)
    assert len(documents) == 0


def test_prometheus_reader_with_additional_metadata(mocker) -> None:
    end_time = datetime.utcnow() - timedelta(days=1)
    start_time = end_time - timedelta(hours=1)
    mocked_metric_data = [
        {
            "metric": {
                "endpoint": "http-metrics",
                "metric_name": "test_metric",
                "pod": "test-pod",
            },
            "values": [],
        }
    ]
    for metric_info in mocked_metric_data:
        for i in range(0, 60, 5):
            timestamp = int((start_time + timedelta(minutes=i)).timestamp())
            metric_info["values"].append([timestamp, i * 100])

    mocker.patch(
        "prometheus_api_client.PrometheusConnect.custom_query_range",
        return_value=mocked_metric_data,
    )
    reader = PrometheusReader(endpoint="test-endpoint", size=100)
    query = "avg_over_time(test_metric[5m])"
    metadata_fields = ["endpoint", "metric_name", "pod"]
    additional_metadata = {
        "collector": "prometheus_reader",
        "collection_date": datetime.now().isoformat(),
    }
    documents = reader.load_data(
        query=query,
        start_time=start_time,
        end_time=end_time,
        metadata_fields=metadata_fields,
        additional_metadata=additional_metadata,
    )
    assert len(documents) == 12
    for doc in documents:
        all_items_exist = all(
            key in doc.metadata and doc.metadata[key] == value
            for key, value in additional_metadata.items()
        )
        assert all_items_exist
