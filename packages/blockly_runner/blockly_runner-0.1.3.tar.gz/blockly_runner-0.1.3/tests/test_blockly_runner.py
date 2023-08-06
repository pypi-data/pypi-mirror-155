import glob
import json
import os

import pytest

from blockly_runner import (
    InvalidBlock,
    UndefinedVariable,
    execute_workspace,
    execute_workspace_merge_all_roots,
)
from blockly_runner.utils import build_many_workspaces_for_each_blocks_root


def _generate_test_case():
    files = glob.glob("./tests/sample_workspaces/*.json")
    test_workspaces = []
    for file in files:
        with open(file, "r") as f:
            data = json.load(f)

        for env, expected_result in zip(data["envs"], data["expected_results"]):
            test_workspaces.append(
                pytest.param(
                    data["workspace"],
                    env,
                    expected_result,
                    id=f"{os.path.basename(file)}-{env}",
                )
            )

    return test_workspaces


def _extract_values_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        workspace = data["workspace"]
        env = data["envs"][0]

    return workspace, env


def _generate_test_case_with_invalid_blocks():
    base_workspace, env = _extract_values_from_json("./tests/invalid_workspaces/invalid_block.json")
    test_workspaces = []
    for index, workspace in enumerate(build_many_workspaces_for_each_blocks_root(base_workspace)):
        test_workspaces.append(
            pytest.param(
                workspace,
                env,
                id=f"invalid_block-{index}",
            )
        )

    return test_workspaces


@pytest.mark.parametrize("workspace, env, expected_result", _generate_test_case())
def test_execute_workspace_merge_all_roots(workspace, env, expected_result):
    result = execute_workspace_merge_all_roots(workspace, env)

    assert result == expected_result


def test_execute_workspace():
    workspace, env = _extract_values_from_json(
        "./tests/sample_workspaces/multiple_root_blocks.json"
    )

    result = execute_workspace(workspace, env)

    assert result == [{"my_var": -50}, {"my_var": -25}]


def test_execute_workspace_print_output(capsys):
    workspace, env = _extract_values_from_json("./tests/sample_workspaces/print_data.json")

    execute_workspace(workspace, env)

    captured = capsys.readouterr()
    assert captured.out == "Hello!\n12\nWorld!\n"


def test_execute_workspace_use_undefined_variable():
    workspace, env = _extract_values_from_json(
        "./tests/invalid_workspaces/use_undefined_variable.json"
    )

    with pytest.raises(UndefinedVariable):
        execute_workspace(workspace, env)


@pytest.mark.parametrize("workspace, env", _generate_test_case_with_invalid_blocks())
def test_execute_workspace_invalid_block(workspace, env):
    with pytest.raises(InvalidBlock):
        execute_workspace(workspace, env)
