import os
from typing import List

from eventbus.events import AlertRaised
from eventbus.singleton import get_eventbus

from bigquery.bigquery import save_test_results
from message.builder import build_slack_message
from parsers.manifest_parser import ManifestParser
from parsers.parse_run_results import DbtResultsLogFactory
from parsers.run_result import RunResult

ALERT_ID = "dbt-alert"
DAG = os.environ.get("DAG")
STAGE = os.environ.get("STAGE")
UNIQUE_RUN_ID = os.environ.get("UNIQUE_RUN_ID")
ARTEFACT_STORAGE_LOCATION = os.environ.get("ARTEFACT_STORAGE_LOCATION")
PATH_RUN_RESULTS = "./target/run_results.json"
PATH_MANIFEST = "./target/manifest.json"
PATH_FRESHNESS = "./target/sources.json"
DBT_FAILURE_TITLE = "dbt Failure"

log_factory = DbtResultsLogFactory()
manifest_parser = ManifestParser()


def raise_alert(alert_id: str, title: str, description: str, category: str) -> None:
    eventbus = get_eventbus()
    event = AlertRaised(
        alert_id=alert_id,
        title=title,
        description=description,
        category=category
    )
    eventbus.publish(event)


def process_file(path: str, manifest) -> List[RunResult]:
    with open(path) as results_file:
        print(f"Reading {path}...")
        results = log_factory.build_results(results_file.read(), manifest)
        print("Completed")

        slack_messages = None
        if DAG is not None and UNIQUE_RUN_ID is not None:
            print(f"Building alert message for {path}...")
            slack_messages = build_slack_message(
                DAG, results, UNIQUE_RUN_ID, ARTEFACT_STORAGE_LOCATION
            )  # noqa
            print("Completed")

        if slack_messages:
            for message in slack_messages:
                print(f'{message.category}:- {message.content}')
                raise_alert(ALERT_ID, DBT_FAILURE_TITLE, message.content, message.category)

    return results


def trigger():
    manifest = {}
    print(f"Does manifest file exist? {os.path.exists(PATH_MANIFEST)}")
    with open(PATH_MANIFEST) as manifest_file:
        print("Reading manifest.json file...")
        manifest = manifest_parser.parse(manifest_file.read())
        print("Completed")

    results = process_file(PATH_RUN_RESULTS, manifest)

    if os.path.exists(PATH_FRESHNESS):
        results.extend(process_file(PATH_FRESHNESS, manifest))

    if UNIQUE_RUN_ID is not None:
        save_test_results(UNIQUE_RUN_ID, results)


if __name__ == "__main__":
    trigger()
