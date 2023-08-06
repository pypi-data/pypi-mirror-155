from __future__ import annotations

import os

from brane.typing import *  # noqa: F403


def integrate_args(base_args: tuple, new_args: tuple) -> tuple:
    if len(base_args) >= len(new_args):
        base_args_list = list(base_args)
    else:
        additional_num = len(new_args) - len(base_args)
        base_args_list = list(base_args) + [None for _ in range(additional_num)]

    for i, arg in enumerate(new_args):
        if arg is not None:
            base_args_list[i] = arg
    return tuple(base_args_list)


def integrate_kwargs(base_kwargs: dict, new_kwargs: dict) -> dict:
    return {**base_kwargs, **new_kwargs}


def sort_mapper(mapper: dict[str, Any], key: str, ascending: bool = False) -> dict[str, Any]:  # Any should has key
    """
    Args:
        mapper:
        key:
        ascending:
    """
    return dict(
        sorted(mapper.items(), key=lambda x: getattr(x[1], key), reverse=not ascending)
    )  # [TODO]: Any is dictionary case


def get_extension_from_filname_default(path: str) -> str:
    ext = os.path.splitext(path)[1][1:]
    return ext
