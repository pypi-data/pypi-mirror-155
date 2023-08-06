from __future__ import annotations

import os  # noqa: E402

from brane.typing import *  # noqa: F403


def check_path_existence(context: ContextInterface):
    # [TODO]: add candidate suggestion function ?
    # [TODO]: map the following if statement into the condition function
    path = context["path"]
    protocol = context.get("protocol", 'file')
    if path is not None and protocol == 'file':
        assert os.path.exists(str(path)), f"The specified path is not found, {path}"


def create_parent_directory(context: ContextInterface):
    # [TODO]: map the following if statement into the condition function
    path = context["path"]
    protocol = context.get("protocol", 'file')
    if path is not None and protocol == 'file':
        parent_dir = os.path.dirname(str(path))
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
