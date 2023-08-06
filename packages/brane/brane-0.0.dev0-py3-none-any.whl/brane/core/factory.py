from __future__ import annotations

import importlib
import os

import yaml

import brane.config as default_cfg
from brane.core.format import Format
from brane.core.module import Module
from brane.core.object import Object
from brane.typing import *  # noqa: F403

ClassAttributeType = dict[str, Any]
ConfigType = dict[str, Union[str, dict]]


class BraneClassGenerator(object):  # [ARG]: rename class name ?
    className2Module: dict[str, ModuleClassType] = dict()
    className2Format: dict[str, FormatClassType] = dict()
    className2Object: dict[str, ObjectClassType] = dict()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BraneClassGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.activate()

    @staticmethod
    def load_config(config_path: str) -> ConfigType:
        cfg: ConfigType = {}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                cfg = yaml.safe_load(f)
        return cfg

    @staticmethod
    def generate_classes_from_configs(
        config_list: list[ConfigType],
        suffix: str,
        cls: type,
        apply_attributes: Optional[Callable[[str, ClassAttributeType], ClassAttributeType]] = None,
    ) -> dict[str, type]:
        name2class: dict[str, type] = {}
        for config in config_list:
            name2class_for_cfg: dict[str, type] = {
                class_name: type(
                    f"{class_name}{suffix}",
                    (cls,),
                    apply_attributes(class_name, attributes) if apply_attributes else attributes,
                )
                for class_name, attributes in config.items()
            }
            name2class.update(name2class_for_cfg)
        return name2class

    @classmethod
    def load_brane_modules(cls) -> dict[str, ModuleClassType]:
        cfg_core = cls.load_config(config_path=default_cfg.CORE_MODULE_CONFIG_PATH)
        cfg_thirdparty = cls.load_config(config_path=default_cfg.THIRDPARTY_MODULE_CONFIG_PATH)

        className2Module = cls.generate_classes_from_configs(
            config_list=[cfg_core, cfg_thirdparty], suffix="Module", cls=Module, apply_attributes=None
        )
        return className2Module

    @classmethod
    def load_brane_formats(cls) -> dict[str, FormatClassType]:
        cfg_core = cls.load_config(config_path=default_cfg.CORE_FORMAT_CONFIG_PATH)
        cfg_thirdparty = cls.load_config(config_path=default_cfg.THIRDPARTY_FORMAT_CONFIG_PATH)

        def update_attributes(class_name: str, attributes: ClassAttributeType) -> ClassAttributeType:
            attributes = attributes.copy()
            if attributes.get("name", None):
                attributes["name"] = class_name

            if attributes.get("module", None) is None and attributes.get("module_name", None) is not None:
                attributes["module"] = cls.className2Module.get(attributes["module_name"], None)

            if attributes["module"] is None:
                if attributes["module_name"]:
                    print(f"[WARNING]: module name {attributes['module_name']} is not found")
                    # raise AssertionError(f"module name {attributes['module_name']} is not found")
                else:
                    print(f"[WARNING]: module name is not defined for {attributes.get('name', '')}")

            return attributes

        className2Format = cls.generate_classes_from_configs(
            config_list=[cfg_core, cfg_thirdparty], suffix="Format", cls=Format, apply_attributes=update_attributes
        )
        return className2Format

    @classmethod
    def load_brane_objects(cls) -> dict[str, ObjectClassType]:
        cfg_core = cls.load_config(config_path=default_cfg.CORE_OBJECT_CONFIG_PATH)
        cfg_thirdparty = cls.load_config(config_path=default_cfg.THIRDPARTY_OBJECT_CONFIG_PATH)

        def update_attributes(class_name: str, attributes: ClassAttributeType) -> ClassAttributeType:
            attributes = attributes.copy()
            if attributes.get("name", None):
                attributes["name"] = class_name

            if attributes.get("format", None) is None and attributes.get("format_name", None) is not None:
                attributes["format"] = cls.className2Format.get(attributes["format_name"], None)
            if attributes.get("module", None) is None and attributes.get("module_name", None) is not None:
                attributes["module"] = cls.className2Module.get(attributes["module_name"], None)

            if attributes["module"] is None:
                if attributes["module_name"]:
                    print(f"[WARNING]: module name {attributes['module_name']} is not found")
                    # raise AssertionError(f"module name {attributes['module_name']} is not found")
                else:
                    print(f"[WARNING]: module name is not defined for {attributes.get('name', '')}")

            if attributes["format"] is None:
                if attributes["format_name"]:
                    print(f"[WARNING]: format name {attributes['format_name']} is not found")
                    # raise AssertionError(f"format name {attributes['format_name']} is not found")
                else:
                    print(f"[WARNING]: format name is not defined for {attributes.get('name', '')}")

            return attributes

        className2Object = cls.generate_classes_from_configs(
            config_list=[cfg_core, cfg_thirdparty], suffix="_Object", cls=Object, apply_attributes=update_attributes
        )
        return className2Object

    @classmethod
    def activate(cls, config_paths: Optional[list[PathType]] = None):
        # [TODO]: use config_paths
        cls.className2Module = cls.load_brane_modules()
        cls.className2Format = cls.load_brane_formats()
        cls.className2Object = cls.load_brane_objects()


class BraneHooksGenerator(object):
    event2hooks: dict[str, list] = dict()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BraneHooksGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.activate()

    @staticmethod
    def load_config(config_path: PathType) -> ConfigType:
        cfg: ConfigType = {}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                cfg = yaml.safe_load(f)
        return cfg

    @staticmethod
    def load_hooks_from_config(cfg: ConfigType) -> list:  # [TODO]: refine return type
        # [TODO]: reduce the depth of nested for-and-if-statements
        # [TODO]: allow Functionhook arguments (flg, condition, ...)
        if cfg["version"] != 'dev.0':
            raise NotImplementedError("Unsupported hook config version: {cfg['version']}")  # [TODO]: refine error
        if "targets" not in cfg:
            raise ValueError("Invalid config")  # [TODO]: refine error

        loaded_hooks = {}
        for event, target_hook_list in cfg["targets"].items():
            if target_hook_list is None:
                continue
            loaded_hooks_for_event = []
            for module2hooks in target_hook_list:
                for module_name, hook_info_list in module2hooks.items():
                    module = importlib.import_module(module_name)
                    for hook_info in hook_info_list:

                        if isinstance(hook_info, str):
                            if hasattr(module, hook_info):
                                hook_func = getattr(module, hook_info)
                                loaded_hooks_for_event.append(hook_func)
                            else:
                                print(f"[WARNING]: no {hook_info} is found in {module}")

                        elif isinstance(hook_info, dict) and len(hook_info) == 1:
                            hook_class_name, hook_params = next(iter(hook_info.items()))
                            if hasattr(module, hook_class_name):
                                hook_class = getattr(module, hook_class_name)
                                if hook_params is None:
                                    loaded_hooks_for_event.append(hook_class())
                                elif isinstance(hook_params, dict):
                                    loaded_hooks_for_event.append(hook_class(**hook_params))
                                else:
                                    print(
                                        f"[WARNING]: hook argument should be of dict or None. {hook_params} is not so."
                                    )
                            else:
                                print(f"[WARNING]: no {hook_class} is found in {module}")

                        else:
                            raise NotImplementedError("Invalid hook info: {hook_info}")  # [TODO]: refine error
            loaded_hooks[event] = loaded_hooks_for_event
        return loaded_hooks

    @classmethod
    def load_event2hooks(
        cls, base_config_path: Optional[list[PathType]] = None, extra_config_paths: Optional[list[PathType]] = None
    ) -> dict[str, list]:  # [TODO]: refine return type
        config_paths: list[PathType] = []
        if base_config_path is None:
            config_paths.extend(
                [
                    default_cfg.CORE_HOOK_CONFIG_PATH,
                    default_cfg.THIRDPARTY_HOOK_CONFIG_PATH,
                ]
            )
        if extra_config_paths:
            config_paths.extend(extra_config_paths)

        event2hooks = dict()
        for path in config_paths:
            if not os.path.exists(str(path)):
                continue
            cfg = cls.load_config(path)
            event2hooks_for_cfg = cls.load_hooks_from_config(cfg)
            for event, hooks in event2hooks_for_cfg.items():
                event2hooks.setdefault(event, []).extend(hooks)
        return event2hooks

    @classmethod
    def activate(cls, config_paths: Optional[list[PathType]] = None):
        assert config_paths is None, "Not implemented yet"
        # [TODO]: use config_paths
        cls.event2hooks = cls.load_event2hooks()
