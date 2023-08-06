import pathlib
from operator import getitem, setitem
from typing import Any, Dict, Optional, Union

from ruamel.yaml import YAML

from .yaml_utils import lint_yaml_file


def update_yaml_file(
    yaml_folder: Union[str, pathlib.Path],
    file_name: str,
    update_dict: Dict[str, Any],
    record_file_name: Optional[str] = None,
) -> None:
    """TODO docstring"""

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)

    yaml_file = pathlib.Path(yaml_folder) / (file_name + ".yaml")
    if not yaml_file.exists():
        yaml_file = pathlib.Path(yaml_folder) / (file_name + ".yml")
        if not yaml_file.exists():
            raise FileNotFoundError(f"The file {file_name}.yaml/yml does not exist.")

    with open(yaml_file, "r", encoding="UTF-8") as file_handle:
        parameters_dict = yaml.load(file_handle)

    # For each key in the update_dict, update the corresponding key in the parameters_dict
    for key, value in update_dict.items():
        split_key = key.split(".")

        object_ref = parameters_dict

        while len(split_key) > 1:
            head = split_key.pop(0)
            object_ref = getitem(object_ref, head)
            if not isinstance(object_ref, dict):
                raise KeyError(f"Could not find {key} in {file_name}")

        # Check that the type matches
        last_value = getitem(object_ref, split_key[0])
        if not issubclass(type(last_value), type(value)):
            raise TypeError(
                f"The type of {key} in {file_name} is not the same as the type of the update value. "
                + f"It should be {type(last_value)} but is {type(value)}."
            )
        setitem(object_ref, split_key[0], value)

    # Write the updated parameters to the file
    with open(yaml_file, "w", encoding="UTF-8") as file_handle:
        yaml.dump(parameters_dict, file_handle)

    # Lint the yaml file after the changes.
    lint_yaml_file(yaml_file)

    if record_file_name is not None:
        record_file = pathlib.Path(yaml_folder) / (record_file_name + ".yaml")

        with open(record_file, "a", encoding="UTF-8") as file_handle:
            record_dict = yaml.load(file_handle)

            for key, value in update_dict.items():
                record_dict[f"record_{key}_value"] = value
                record_dict[f"record_{key}_time"] = type(value).__name__
