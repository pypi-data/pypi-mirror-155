from __future__ import annotations

from brane.core.base import BaseSubclassRegister, MetaFalse
from brane.typing import *  # noqa: F403


def normalize_extension_default(ext: str) -> str:
    return ext.strip().lower()


class MetaFormat(type):
    def __new__(cls, classname: str, bases: tuple[type], class_info: dict):
        new_class_info: dict = class_info.copy()
        default_extension: Optional[str] = class_info.get("default_extension", None)
        if new_class_info.get("name", None) is None:
            new_class_info["name"] = default_extension
        if default_extension not in class_info.get("variation", []):
            new_class_info.setdefault("variation", []).append(default_extension)

        print(f"[DEBUG]: in MetaFormat default_extension={default_extension} class_info={new_class_info}")
        return type.__new__(cls, classname, bases, new_class_info)

    # [TODO] python>=3.9, move to class as classmethod property
    @property
    def registered_formats(cls) -> dict:
        return cls._registered_subclasses


class Format(FormatClassType, BaseSubclassRegister, metaclass=MetaFormat):
    _registered_subclasses = {}
    priority = 50
    # valid = True

    # # Image, Text ... # experimental
    # data_type = None
    # jpg, png, tsv,... (flexible/variable/dynamical)
    default_extension: Optional[str] = None
    variation: list[str] = []  # variations ? // use tuple instead of list or replace later ?

    @classmethod
    def check_extension(cls, ext: str) -> bool:
        ext_normalized: str = normalize_extension_default(ext)
        return ext_normalized in cls.variation


class MetaNoneFormat(MetaFormat, MetaFalse):  # [MEMO]: deprecated after removing MetaFormat
    pass


class NoneFormat(Format, metaclass=MetaNoneFormat):
    valid = False
