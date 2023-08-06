import abc
import datetime
import json
from typing import Dict, List, Tuple

from parsers.manifest import Manifest
from parsers.run_result import RunResult, RunResultType


def _parse_test_unique_id(unique_id) -> Tuple[RunResultType, str, str]:
    stg_table_prefix = "stg"
    int_table_prefix = "int"

    details = unique_id.split(".")[2]
    prefix = ""

    split_results = []
    if stg_table_prefix in unique_id:
        split_results = details.split(f"_{stg_table_prefix}")
        prefix = stg_table_prefix
    elif int_table_prefix in unique_id:
        split_results = details.split(f"_{int_table_prefix}")
        prefix = int_table_prefix
    else:
        split_results = details

    table_name = ""
    test_name = ""
    if type(split_results) is List:
        test_name = split_results[0] if split_results else None
        table_name = f"{prefix}{split_results[1]}" if split_results else details
    else:
        table_name = details
        test_name = details

    model_type = (
        RunResultType.Model if unique_id.startswith("model") else RunResultType.Test
    )

    # need to think of clever way to extract this and column name
    # currently it will include column name as well
    # column_name = ...

    return model_type, table_name, test_name


def _parse_run_timings(timing):
    for section in timing:
        if section["name"] == "execute":
            return section["started_at"], section["completed_at"]

    return None, None


def _parse_metadata_type(metadata):
    dbt_schema = metadata["dbt_schema_version"]
    if "run-results" in dbt_schema:
        return "run_results"
    if "sources" in dbt_schema:
        return "freshness"
    else:
        return None


class DbtResultsLogFactory:
    def build_results(
        self, run_results_text: str, manifest_list: Dict[str, Manifest]
    ) -> List[RunResult]:
        raw_results = json.loads(run_results_text)
        metadata = raw_results["metadata"]
        parser = self._get_parser(raw_results=raw_results, metadata=metadata)

        return parser.parse_run_results(raw_results, manifest_list)

    def _get_parser(self, raw_results: Dict, metadata: str):
        if _parse_metadata_type(metadata) == "run_results":
            return RunResultsParser()
        elif _parse_metadata_type(metadata) == "freshness":
            return FreshnessTestParser()


class ResultsParser(abc.ABC):
    @abc.abstractmethod
    def parse_run_results(
        self, raw_results, manifest_list: Dict[str, Manifest]
    ) -> List[RunResult]:
        raise NotImplementedError


class RunResultsParser(ResultsParser):
    def parse_run_results(
        self, raw_results, manifest_list: Dict[str, Manifest]
    ) -> List[RunResult]:
        results = []
        for single_run_result in raw_results["results"]:
            unique_id = single_run_result["unique_id"]
            manifest = manifest_list[unique_id]
            model_type, table_name, test_name = _parse_test_unique_id(unique_id)
            run_start, run_end = _parse_run_timings(single_run_result["timing"])
            results.append(
                RunResult(
                    run_type=model_type,
                    status=single_run_result["status"],
                    execution_time=single_run_result["execution_time"],
                    run_start=run_start,
                    run_end=run_end,
                    message=single_run_result["message"],
                    failures=single_run_result["failures"],
                    unique_id=unique_id,
                    table_name=table_name,
                    test_name=test_name,
                    manifest=manifest,
                    is_success=True
                    if single_run_result["status"] == "pass"
                    or single_run_result["status"] == "warn"
                    or single_run_result["status"] == "success"
                    else False,
                )
            )

        return results


class FreshnessTestParser(ResultsParser):
    def parse_run_results(
        self, raw_results, manifest_list: Dict[str, Manifest]
    ) -> List[RunResult]:
        results = []
        for single_run_result in raw_results["results"]:
            run_start, run_end = _parse_run_timings(single_run_result.get("timing", []))
            unique_id = single_run_result["unique_id"]
            manifest = manifest_list[unique_id]
            last_loaded_time = datetime.datetime.now() - datetime.timedelta(
                seconds=single_run_result.get("max_loaded_at_time_ago_in_s", 0)
            )
            error_after_criteria_count = (
                single_run_result["criteria"]["error_after"]["count"]
                if "criteria" in single_run_result.keys()
                else 0
            )
            error_after_criteria_period = (
                single_run_result["criteria"]["error_after"]["period"]
                if "criteria" in single_run_result.keys()
                else 0
            )
            results.append(
                RunResult(
                    run_type=RunResultType.Freshness,
                    status=single_run_result["status"],
                    execution_time=single_run_result.get("execution_time", None),
                    run_start=run_start,
                    run_end=run_end,
                    message=(
                        f"Data was last loaded at {last_loaded_time}, "
                        f"which is older than the {error_after_criteria_count} "
                        f" {error_after_criteria_period} threshold"
                    ),
                    failures=1,
                    unique_id=unique_id,
                    table_name=manifest.name,
                    manifest=manifest,
                    is_success=False
                    if single_run_result["status"] == "error"
                    else True,
                )
            )
        return results
