from typing import List

from bigquery.bq_query_runner import BqQueryQueryRunner
from parsers.run_result import RunResult, RunResultType


def save_test_results(invocation_id: str, results: List[RunResult]):
    query = """
INSERT INTO backend-producti-b8633498.zoe_log.dbt_run_results
(
    invocation_id,
    result_type,
    run_start,
    run_end,
    package_name,
    dataset_name,
    table_name,
    success_status,
    message_text,
    materialisation,
    is_full_refresh,
    tags,
    execution_time,
    rows_affected,
    bytes_processed,
    timing,
    response,
    owning_team,
    slack_support_group,
    slack_support_group_id
)
VALUES
"""
    values_list = []
    for result in [r for r in results if r.run_type == RunResultType.Test]:
        values_list.append(
            f"""
(
    '{invocation_id}',
    '{result.manifest.resource_type.lower()}',
    {"PARSE_DATETIME('%FT%H:%M:%E6SZ', '" + result.run_start + "')"
    if result.run_start is not None
    else "NULL"},
    {"PARSE_DATETIME('%FT%H:%M:%E6SZ', '" + result.run_end + "')"
    if result.run_end is not None
    else "NULL"},
    '{result.manifest.package_name}',
    '{result.manifest.dataset_name}',
    '{result.table_name}',
    '{result.is_success}',
    {"'"+clean_message_text(result.message)+"'"
    if result.message is not None
    else "NULL"},
    NULL,
    NULL,
    NULL,
    {result.execution_time},
    NULL,
    NULL,
    NULL,
    NULL,
    {"'"+result.manifest.owner+"'"
    if result.manifest.owner is not None
    else "NULL"},
    {"'"+result.manifest.slack_support_group+"'"
    if result.manifest.slack_support_group is not None
    else "NULL"},
    {"'"+result.manifest.slack_support_group_id+"'"
    if result.manifest.slack_support_group_id is not None
    else "NULL"}
)
"""
        )

    if len(values_list) > 0:
        query_runner = BqQueryQueryRunner()
        query = query + ",".join(values_list)
        query_runner.run(query)


def clean_message_text(message_text: str) -> str:
    """
    Cleans message text by removing characters which may cause a failure in the SQL
    """
    return message_text.replace('"', "").replace("\n", "")
