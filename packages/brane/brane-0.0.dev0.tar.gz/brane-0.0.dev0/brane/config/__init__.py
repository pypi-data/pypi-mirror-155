from pathlib import Path

CORE_MODULE_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/modules/core.yaml").resolve()
THIRDPARTY_MODULE_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/modules/basic.yaml").resolve()
CORE_FORMAT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/formats/core.yaml").resolve()
THIRDPARTY_FORMAT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/formats/basic.yaml").resolve()
CORE_OBJECT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/objects/core.yaml").resolve()
THIRDPARTY_OBJECT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/objects/basic.yaml").resolve()
CORE_HOOK_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/hooks/core.yaml").resolve()
THIRDPARTY_HOOK_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./brane/config/hooks/basic.yaml").resolve()
