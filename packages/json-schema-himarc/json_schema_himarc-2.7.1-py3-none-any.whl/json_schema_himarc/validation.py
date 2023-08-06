#!/usr/bin/env python3

"""Validate instance using Himarc JSON schema"""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from typing import Any, Dict
from warnings import warn

from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

__all__ = [
    "validate_himarc",
    "get_himarc_validation_errors",
    "WORK_SCHEMA",
    "REGISTER_SCHEMA",
]

WORK_SCHEMA = "work"
REGISTER_SCHEMA = "register"


def _get_schema(category: str) -> Dict[str, Any]:
    """Get Himarc JSON schema data."""
    schema_available = [REGISTER_SCHEMA, WORK_SCHEMA]
    schema_filename = f"himarc-{category}.schema.json"
    if category not in schema_available:
        categories = ", ".join(schema_available)
        error = f"Invalid schema category must be : [{categories}]"
        warn(error)
        raise ValueError(error)

    schema_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "schema"
    )
    schema_path = os.path.join(schema_dir, schema_filename)
    with open(schema_path, "r") as json_schema_file:
        return json.load(json_schema_file)


def validate_himarc(
    instance: Dict[str, Any], category: str = "register"
) -> bool:
    """Validate himarc instance using JSON schema validator."""
    try:
        schema = _get_schema(category)
        validator = Draft7Validator(schema)
        validator.validate(instance)
        return True
    except (ValidationError, ValueError):
        return False


def get_himarc_validation_errors(
    instance: Dict[str, Any], config: str = "register"
) -> Iterable[ValidationError]:
    """Get himarc instance errors using JSON schema validator.

    Returns an iterable of
    <https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError>
    """
    schema = _get_schema(config)
    validator = Draft7Validator(schema)
    return validator.iter_errors(instance)
