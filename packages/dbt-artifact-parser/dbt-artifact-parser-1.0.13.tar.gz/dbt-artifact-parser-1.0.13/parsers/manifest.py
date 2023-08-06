from typing import List, Optional


class Manifest:
    def __init__(
        self,
        identifier: str,
        unique_id: str,
        name: str,
        alias: str,
        resource_type: str,
        package_name: str,
        dataset_name: str,
        original_file_path: str,
        path: str,
        depends_on: List[str],
        owner: Optional[str],
        slack_support_group: Optional[str],
        slack_support_group_id: Optional[str],
    ) -> None:
        self._identifier = identifier
        self._unique_id = unique_id
        self._name = name
        self._alias = alias
        self._resource_type = resource_type
        self._package_name = package_name
        self._dataset_name = dataset_name
        self._original_file_path = original_file_path
        self._path = path
        self._depends_on = depends_on
        self._owner = owner
        self._slack_support_group = slack_support_group
        self._slack_support_group_id = slack_support_group_id

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def resource_type(self) -> str:
        return self._resource_type

    @property
    def package_name(self) -> str:
        return self._package_name

    @property
    def dataset_name(self) -> str:
        return self._dataset_name

    @property
    def original_file_path(self) -> str:
        return self._original_file_path

    @property
    def path(self) -> str:
        return self._path

    @property
    def depends_on(self) -> List[str]:
        return self._depends_on

    @property
    def owner(self) -> Optional[str]:
        return self._owner

    @owner.setter
    def owner(self, value: str):
        self._owner = value

    @property
    def slack_support_group(self) -> Optional[str]:
        return self._slack_support_group

    @slack_support_group.setter
    def slack_support_group(self, value: str):
        self._slack_support_group = value

    @property
    def slack_support_group_id(self) -> Optional[str]:
        return self._slack_support_group_id

    @slack_support_group_id.setter
    def slack_support_group_id(self, value: str):
        self._slack_support_group_id = value
