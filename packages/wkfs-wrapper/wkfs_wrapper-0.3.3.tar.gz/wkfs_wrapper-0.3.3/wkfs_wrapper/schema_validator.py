import json

from jsonschema import validate
from wkfs_wrapper.constants import BASE_DIR


def validate_wkfs_config(wkfs_config):
    json_schema = _get_json_schema()
    if json_schema is None:
        return "Error loading json schema!"
    validate(wkfs_config, json_schema)


def _get_json_schema():
    json_schema = None
    with open(f"{BASE_DIR}/../validator/schema_validation.json", "r", encoding="utf-8") as file:
        json_schema = json.load(file)
    return json_schema
