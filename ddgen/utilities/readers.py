import json

from pydantic import BaseModel


def model_from_json(path: str, model: BaseModel) -> BaseModel:
    with open(path) as f:
        return model.model_validate(json.load(f))
