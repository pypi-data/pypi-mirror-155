__version__ = "0.1.3"

from copy import deepcopy
from typing import Any, Dict, List

from .constants import (
    BlockType,
    boolean_operators_to_fn,
    logic_operators_to_fn,
    math_operators_to_fn,
)
from .exceptions import InvalidBlock, UndefinedVariable
from .typing import assert_never


def execute_workspace_merge_all_roots(workspace, input_env: Dict[Any, Any]) -> Dict[str, Any]:
    """Execute the workspace.

    You will get a global result: all block roots will be executed in order, the new env of each one being the new env
    for the next root.
    """
    env = deepcopy(input_env)
    variable_id_to_name: Dict[str, Any] = {var["id"]: var["name"] for var in workspace["variables"]}
    for block in workspace["blocks"]["blocks"]:
        _execute_block(block, env, variable_id_to_name)

    return env


def execute_workspace(workspace, input_env: Dict[Any, Any]) -> List[Dict[str, Any]]:
    """Execute the workspace.

    You will get a list of results: each for each block root.
    """
    result_envs = []
    variable_id_to_name: Dict[str, Any] = {
        var["id"]: var["name"] for var in workspace.get("variables", [])
    }
    for block in workspace["blocks"]["blocks"]:
        env = deepcopy(input_env)
        _execute_block(block, env, variable_id_to_name)
        result_envs.append(env)

    return result_envs


def _execute_block(block, env, variable_id_to_name):
    block_type = BlockType(block["type"])
    inputs = block.get("inputs", {})
    fields = block.get("fields", {})
    value = None

    if block.get("enabled", True):
        if block_type is BlockType.controls_if:
            value = _controls_if(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.logic_compare:
            value = _logic_compare(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.logic_operation:
            value = _logic_operation(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.logic_negate:
            value = _logic_negate(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.logic_null:
            value = None
        elif block_type is BlockType.variables_get:
            value = _variables_get(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.variables_set:
            value = _variables_set(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.math_number:
            value = _math_number(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.math_change:
            value = _math_change(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.text:
            value = _text(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.text_print:
            value = _text_print(inputs, fields, env, variable_id_to_name)
        elif block_type is BlockType.math_arithmetic:
            value = _math_arithmetic(inputs, fields, env, variable_id_to_name)
        else:
            assert_never(block_type)

    if "next" in block:
        _execute_block(block["next"]["block"], env, variable_id_to_name)

    return value


def _controls_if(inputs, fields, env, variable_id_to_name):
    # IF blocks are structured like this:
    # {'IF0': {}, 'DO0': {}, 'IF1': {}, 'DO1': {}, 'ELSE': {}}
    for if_id, if_statement in sorted(tuple(inputs.items())):
        if not if_id.startswith("IF"):
            continue

        do_id = if_id.replace("IF", "DO")
        if do_id not in inputs:
            raise InvalidBlock

        if _execute_block(
            if_statement["block"],
            env,
            variable_id_to_name,
        ):
            return _execute_block(
                inputs[do_id]["block"],
                env,
                variable_id_to_name,
            )

    if "ELSE" in inputs:
        return _execute_block(
            inputs["ELSE"]["block"],
            env,
            variable_id_to_name,
        )

    return None


def _logic_compare(inputs, fields, env, variable_id_to_name):
    return logic_operators_to_fn[fields["OP"]](
        _execute_block(
            inputs["A"]["block"],
            env,
            variable_id_to_name,
        ),
        _execute_block(
            inputs["B"]["block"],
            env,
            variable_id_to_name,
        ),
    )


def _logic_operation(inputs, fields, env, variable_id_to_name):
    try:
        return boolean_operators_to_fn[fields["OP"]](
            _execute_block(inputs["A"]["block"], env, variable_id_to_name),
            _execute_block(inputs["B"]["block"], env, variable_id_to_name),
        )
    except KeyError as e:
        raise InvalidBlock from e


def _logic_negate(inputs, fields, env, variable_id_to_name):
    return not _execute_block(inputs["BOOL"]["block"], env, variable_id_to_name)


def _variables_get(inputs, fields, env, variable_id_to_name):
    variable_name = _get_variable_name_from_fields(fields, variable_id_to_name)

    try:
        return env[variable_name]
    except KeyError as e:
        raise UndefinedVariable(f"Variable {variable_name} is not defined.") from e


def _get_variable_name_from_fields(fields, variable_id_to_name):
    return variable_id_to_name[fields["VAR"]["id"]]


def _variables_set(inputs, fields, env, variable_id_to_name):
    variable_name = _get_variable_name_from_fields(fields, variable_id_to_name)

    try:
        env[variable_name] = _execute_block(
            inputs["VALUE"]["block"],
            env,
            variable_id_to_name,
        )
        return None
    except KeyError as e:
        raise InvalidBlock from e


def _math_number(inputs, fields, env, variable_id_to_name):
    return fields["NUM"]


def _math_change(inputs, fields, env, variable_id_to_name):
    variable_name = _get_variable_name_from_fields(fields, variable_id_to_name)
    variable_value = _variables_get({}, fields, env, variable_id_to_name)
    env[variable_name] = variable_value + inputs["DELTA"]["shadow"]["fields"]["NUM"]
    return None


def _math_arithmetic(inputs, fields, env, variable_id_to_name):
    try:
        return math_operators_to_fn[fields["OP"]](
            _execute_block(inputs["A"]["block"], env, variable_id_to_name),
            _execute_block(inputs["B"]["block"], env, variable_id_to_name),
        )
    except KeyError as e:
        raise InvalidBlock from e


def _text(inputs, fields, env, variable_id_to_name):
    return fields["TEXT"]


def _text_print(inputs, fields, env, variable_id_to_name):
    print(_execute_block(inputs["TEXT"]["block"], env, variable_id_to_name))
    return None
