import json
from typing import Dict

from parsers.manifest import Manifest


class ManifestParser:
    def parse(self, manifest_raw: str) -> Dict[str, Manifest]:
        manifest_json = json.loads(manifest_raw)
        nodes = manifest_json["nodes"]
        nodes.update(manifest_json["sources"])

        parsed_manifest = {}
        for item_key, item_value in nodes.items():

            (
                owner,
                slack_support_group_name,
                slack_support_group_id,
            ) = self._parse_slack_support_group(item_value["config"].get("meta", None))
            resource_type = self._parse_resource_type(
                item_value["resource_type"], item_value.get("raw_sql", None)
            )

            parsed_manifest[item_key] = Manifest(
                identifier=item_key,
                unique_id=item_value["unique_id"],
                name=item_value["name"],
                alias=item_value["alias"]
                if resource_type != "source"
                else item_value["name"],
                resource_type=resource_type,
                package_name=item_value["package_name"],
                dataset_name=item_value["schema"],
                original_file_path=item_value["original_file_path"],
                path=item_value["path"],
                depends_on=item_value["depends_on"]["nodes"]
                if "depends_on" in item_value.keys()
                else [],
                owner=owner,
                slack_support_group=slack_support_group_name,
                slack_support_group_id=slack_support_group_id,
            )

        # 2nd pass to populate schema test items with the ownership and slack support info from the underlying table
        test_items = []
        for _, manifest in parsed_manifest.items():
            if manifest.resource_type == "generic test":
                test_items.append(manifest)

        for item in test_items:
            if len(item.depends_on) > 0:
                # Hack to not use source tests right now and do that on next iteration
                if item.depends_on[0].startswith("source"):
                    continue

                test_table = parsed_manifest[item.depends_on[0]]
                item.owner = test_table.owner
                item.slack_support_group = test_table.slack_support_group
                item.slack_support_group_id = test_table.slack_support_group_id

        return parsed_manifest

    def _parse_slack_support_group(self, meta):
        if meta is None or len(meta) == 0:
            return None, None, None

        owner = meta.get("owner", None)
        if owner is None:
            return None, None, None

        slack_support_group = meta["slack_support_group"]
        group_parts = slack_support_group.split(",")
        return owner, group_parts[0], group_parts[1]

    def _parse_resource_type(self, resource_type: str, test_type_indicator) -> str:
        if resource_type == "test":
            test_type = (
                "generic" if "_dbt_generic_test" in test_type_indicator else "singular"
            )
            return f"{test_type} test"
        else:
            return resource_type
