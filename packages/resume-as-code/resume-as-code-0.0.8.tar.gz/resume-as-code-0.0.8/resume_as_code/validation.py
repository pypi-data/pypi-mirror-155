from typing import Tuple

import yaml
from cerberus import Validator


def validate_resume(resume_filename: str, schema_filename: str) -> Tuple[bool, str]:
    """
    Validate a certain resume, located in `resume_filename` to the specification declared in `schema_filename`

    Args:
        resume_filename (str): The location of the resume that you would like to validate
        schema_filename (str): The location of the schema to which the resume should be validated

    Returns:
        Tuple[bool, str]: A tuple containing of the validation flag and the possible error messages.
    """
    with open(resume_filename, "r") as file:
        yaml_resume = yaml.load(file, Loader=yaml.FullLoader)

    with open(schema_filename, "r") as file:
        yaml_schema = yaml.load(file, Loader=yaml.FullLoader)

    validator = Validator(yaml_schema)
    validator.allow_unknown = True  # type: ignore

    if validator.validate(yaml_resume):  # type: ignore
        return True, ""
    else:
        return False, validator.errors  # type: ignore
