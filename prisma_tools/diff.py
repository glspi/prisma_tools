"""prisma_tools.diff"""
import difflib
import json
import time
from typing import Any

from prisma_tools import utils
from prisma_tools.PrismaSASECloudManaged_Python.access import (
    policyObjects,
    prismaAccess,
)


def get_obj(objs: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    """Search through objects and return when found"""
    for obj in objs:
        if obj["name"] == name:
            return obj
    print(f"Error: {name} was not found.")
    return None


def run(prisma_api: prismaAccess.prismaAccess, object_type: str) -> None:
    """
    Compare two objects and provide html based diff output

    Args:
        prisma_api: prismaAccess API Object
        object_type: type of object to compare

    """
    # Initialize vars
    prisma_sdk = policyObjects.policyObjects(prisma_api)
    list_objects = utils.DIFF_API_CALLS[object_type]
    objects: list[dict[str, Any]] = getattr(prisma_sdk, list_objects)()
    obj_names = [obj["name"] for obj in objects]

    # List existing objects and get the 2 object names to compare
    print(f"Available {object_type}'s: ")
    [print("\t", name) for name in obj_names]
    print("\nWhich objects should be compared?")
    compare_1 = compare_2 = None
    while compare_1 is None:
        name = input(f"{object_type.upper()} 1: ")
        compare_1 = get_obj(objs=objects, name=name)
    while compare_2 is None:
        name = input(f"{object_type.upper()} 2: ")
        compare_2 = get_obj(objs=objects, name=name)

    # Do the diff
    diff_html = difflib.HtmlDiff(wrapcolumn=80).make_file(
        json.dumps(compare_1, indent=4).split("\n"),
        json.dumps(compare_2, indent=4).split("\n"),
        compare_1["name"],
        compare_2["name"],
    )

    # Output
    append = str(time.time()).split(".")[0]
    filename = f"{object_type}-diff-{append}.html"
    with open(filename, "w") as fout:
        fout.write(diff_html)
    print(f"Diff file created at: {filename}")
