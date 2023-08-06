from __future__ import annotations

from brane.core.factory import BraneClassGenerator
from brane.core.hook import Hook
from brane.typing import *  # noqa: F403


class PILResizeHook(Hook):
    # [TODO]: After PIL config will be changed, update this module
    hook_name = "PILResize"

    def __init__(self, size: tuple[int, int], resample=None):
        from PIL import Image as PILImage

        if resample is None:
            resample = PILImage.BILINEAR
        self.size = size
        self.resample = resample

    def condition(self, context: ContextInterface) -> bool:
        obj = context.get("object", None)
        is_jpeg: bool = isinstance(obj, BraneClassGenerator.className2Object["PIL_JPEG"].object)
        is_png: bool = isinstance(obj, BraneClassGenerator.className2Object["PIL_PNG"].object)
        return is_jpeg or is_png

    def __call__(self, context: ContextInterface) -> Any:  # [TODO]: replace Any by the correct type
        print("resize")
        obj = context.get("object")
        return obj.resize(self.size, self.resample)
