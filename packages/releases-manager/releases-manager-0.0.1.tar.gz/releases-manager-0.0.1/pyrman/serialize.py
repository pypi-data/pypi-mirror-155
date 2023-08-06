import dataclasses
from datetime import datetime

import yaml


def make_serializable(obj):
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    elif isinstance(obj, (list, tuple)):
        return [dataclasses.asdict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: dataclasses.asdict(value) for key, value in obj.items()}
    else:
        return obj


def serialize_as_yaml(obj):
    return yaml.safe_dump(make_serializable(obj)).replace("- ", "\n- ")
