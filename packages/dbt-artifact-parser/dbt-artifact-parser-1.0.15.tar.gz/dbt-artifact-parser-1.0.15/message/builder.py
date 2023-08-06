import json
from typing import Dict, List, Optional, Tuple

from dbt_utils.dbt_runner import get_downstream_models
from parsers.manifest import Manifest
from parsers.run_result import RunResult, RunResultType

from message.slack_message import SlackMessage


def _build_run_message(
    result: RunResult, innvocation_id: str, storage_location: str, footer: str
) -> List[Dict]:
    downstream_models = get_downstream_models(result.table_name)
    compiled_sql_link = f"{storage_location}/{innvocation_id}-run/run/{result.manifest.package_name}/{result.manifest.original_file_path}"
    return [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":redsiren: *Critcal Model Failure: {result.table_name}* :redsiren:",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Compiled SQL", "emoji": True},
                "value": f"{result.table_name}",
                "url": f"{compiled_sql_link}",
                "action_id": "button-action",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":warning: *Impacts {len(downstream_models)} models, which will not be updated until the error is resolved*",
            },
        },
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"{result.message}"}},
        {"type": "divider"},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f"{footer}"}]},
        {"type": "divider"},
    ]


def _build_test_message(
    result: RunResult, innvocation_id: str, storage_location: str, footer: str
) -> List[Dict]:
    test_name = result.table_name if result.test_name is not None else result.test_name
    compiled_sql_link = f"{storage_location}/{innvocation_id}-test/run/{result.manifest.package_name}/{result.manifest.original_file_path}{'/' + result.manifest.path if result.manifest.resource_type == 'generic test' else ''}"
    test_result_message = (
        f"Check: {result.test_name}\n{result.message}"
        if result.test_name is not None
        else f"{result.message}"
    )
    return [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":test_tube: *Test Failure: {test_name}* :test_tube:",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Compiled SQL", "emoji": True},
                "value": f"{test_name}",
                "url": f"{compiled_sql_link}",
                "action_id": "button-action",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"{test_result_message}"},
        },
        {"type": "divider"},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f"{footer}"}]},
        {"type": "divider"},
    ]


def _build_freshness_message(result: RunResult, footer: str) -> List[Dict]:
    return [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":clock1: *Model Freshness: {result.table_name}* :clock1:",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"Stale Data: {result.message}"},
        },
        {"type": "divider"},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f"{footer}"}]},
        {"type": "divider"},
    ]


def _build_message_body(
    result: RunResult, dag_name: str, innvocation_id: str, storage_location: str
) -> Dict:

    message_parts = []
    if not result.is_success:

        team_ownership_text = (
            f"{result.manifest.owner} "
            f"( <!subteam^{result.manifest.slack_support_group_id}> )"
            if result.manifest.owner is not None
            else "WARNING: No assigned team"
        )

        footer = (
            f"Execution time: {round(result.execution_time, 4)}s\n"
            f"Owner | {team_ownership_text}\n"
            f"DAG name | {dag_name}"
        )

        if result.run_type == RunResultType.Model:
            message_parts += _build_run_message(
                result, innvocation_id, storage_location, footer
            )

        if result.run_type == RunResultType.Test:
            message_parts += _build_test_message(
                result, innvocation_id, storage_location, footer
            )

        if result.run_type == RunResultType.Freshness:
            message_parts += _build_freshness_message(result, footer)

    return message_parts


def build_slack_message(
    dag_name: str, results: List[RunResult], invocation_id: str, storage_location: str
) -> List[SlackMessage]:
    """
    Build a slack message blob from the raw dbt results
    """
    messages = []
    for result in results:
        if not result.is_success:
            messages.append(SlackMessage(
                content=json.dumps(
                    _build_message_body(
                        result, dag_name, invocation_id, storage_location
                    )
                ),
                category=result.table_name
            ))

    return messages


def lookup_team_info(
    manifest: Dict[str, Manifest], unique_id: str
) -> Tuple[Optional[str], Optional[str]]:
    dbt_item = manifest[unique_id]
    return dbt_item.owner, dbt_item.slack_support_group_id
