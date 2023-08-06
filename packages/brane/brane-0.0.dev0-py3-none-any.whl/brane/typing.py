from __future__ import annotations

from typing import (  # noqa: F401
    Any,
    Callable,
    Container,
    Generator,
    Generic,
    NamedTuple,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

try:
    from typing import Protocol, TypedDict  # noqa: F401 # >=3.8
except ImportError:
    from typing_extensions import Protocol, TypedDict  # noqa: F401 # <=3.7


# define the types for universal objects


def _generate_file_related_types():
    import io
    import pathlib

    class IO(Protocol):
        def open(file):
            pass

    from fsspec.asyn import AsyncFileSystem

    PathType = Union[str, pathlib.Path]
    FileType = Union[io._io._IOBase]  # [TODO]: more types should be added
    IOType = Union[IO, AsyncFileSystem]  # [TODO]: more types should be added
    return PathType, FileType, IOType


PathType, FileType, IOType = _generate_file_related_types()
del _generate_file_related_types


# define the package specific types


class ModuleClassType:
    name: str
    loaded: bool
    reload_modules: Callable
    read: Callable
    write: Callable


class FormatClassType:
    pass


class ObjectClassType:
    pass


class HookClassType:
    pass


class EventClassType:
    pass


HookFlagType = Optional[Union[str, set[str]]]


class ContextInterface(TypedDict):
    object: Optional[Any] = None
    objects: Optional[list[Any]] = None
    path: Optional[PathType] = None
    paths: Optional[list[PathType]] = None
    file: Optional[FileType] = None
    files: Optional[list[FileType]] = None
    Module: Optional[ModuleClassType] = None
    Format: Optional[FormatClassType] = None


# used for debug purpose temporalily
def print(*value, sep=' ', end='\n', file=None, flush=False):
    import builtins
    import os
    import sys

    if file is None:
        file = sys.stdout
    if os.environ.get("BRANE_MODE", None) == 'debug':
        builtins.print(*value, end=end, file=file, flush=flush)
    else:
        pass
