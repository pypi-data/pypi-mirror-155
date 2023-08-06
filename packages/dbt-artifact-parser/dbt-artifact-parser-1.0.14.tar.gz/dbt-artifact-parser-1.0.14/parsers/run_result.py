from enum import Enum
from typing import Optional

from parsers.manifest import Manifest


class RunResultType(Enum):
    Model: str = "Model"
    Test: str = "Test"
    Freshness: str = "Freshness"


class RunResult:
    def __init__(
        self,
        run_type: RunResultType,
        status: str,
        execution_time: float,
        run_start: str,
        run_end: str,
        message: str,
        failures: int,
        unique_id: str,
        table_name: str,
        is_success: bool,
        manifest: Manifest,
        test_name: Optional[str] = None,
    ) -> None:
        self._run_type = run_type
        self._status = status
        self._execution_time = execution_time
        self._run_start = run_start
        self._run_end = run_end
        self._message = message
        self._failures = failures
        self._unique_id = unique_id
        self._is_success = is_success
        self._manifest = manifest
        self._table_name = table_name
        self._test_name = test_name

    @property
    def run_type(self) -> RunResultType:
        return self._run_type

    @property
    def status(self) -> str:
        return self._status

    @property
    def execution_time(self) -> float:
        return self._execution_time

    @property
    def run_start(self) -> str:
        return self._run_start

    @property
    def run_end(self) -> str:
        return self._run_end

    @property
    def message(self) -> str:
        return self._message

    @property
    def failures(self) -> int:
        return self._failures

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def test_name(self) -> Optional[str]:
        return self._test_name

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def manifest(self) -> Manifest:
        return self._manifest
