from copy import deepcopy


def build_many_workspaces_for_each_blocks_root(base_workspace):
    workspaces = []
    for block in base_workspace["blocks"]["blocks"]:
        workspaces.append(_get_workspace(base_workspace, block))

    return workspaces


def _get_workspace(base_workspace, block):
    return {
        "blocks": {
            "blocks": [block],
            "languageVersion": base_workspace["blocks"]["languageVersion"],
        },
        "variables": deepcopy(base_workspace["variables"]),
    }
