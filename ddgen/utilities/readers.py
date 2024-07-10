import json

from ddgen.models import DatabaseModel


def read_json_to_db_model(path: str) -> DatabaseModel:
    with open(path) as f:
        return DatabaseModel.model_validate(json.load(f))
