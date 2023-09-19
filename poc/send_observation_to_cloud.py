import json
from google.cloud import pubsub_v1
from google.oauth2 import service_account

credentials_obj = service_account.Credentials.from_service_account_file(
    "PATH-TO-SERVICE-ACCOUNT-KEY-JSON"
)

project_id = "superior-noise-loggers"
pubsub_topic = "noise-logger-ingest"


def publish_data(reporting_obj):
    publisher_client = pubsub_v1.PublisherClient(credentials = credentials_obj)

    pubsub_topic_path = "projects/{project_id}/topics/{pubsub_topic}".format(
        project_id = project_id,
        pubsub_topic = pubsub_topic
    )

    async_future = publisher_client.publish(
        pubsub_topic_path,
        json.dumps(reporting_obj).encode("utf-8")
    )

    async_future.result()
        
    return "data published"


def main():
    reporting_obj = {
        "reporting_station": "maday_shavano",
        "reporting_timestamp": "2023-09-03 16:58:28.524732",
        "db_report": -45.20
    }
    
    print(publish_data(reporting_obj)


if __name__ == "__main__":
    main()