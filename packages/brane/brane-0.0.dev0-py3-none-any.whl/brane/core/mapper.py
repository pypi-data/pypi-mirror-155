from __future__ import annotations

from brane.core.format import Format, NoneFormat
from brane.core.module import NoneModule
from brane.core.object import Object
from brane.typing import *  # noqa: F403


class ExtensionMapper(object):  # [ARG]: rename ?
    # [TODO]:: caching
    @classmethod
    def get_format_class_from_extension(cls, ext: str) -> FormatClassType:  # ignore: this type is defined later
        for _, Fmt in Format.registered_formats.items():
            if Fmt.check_extension(ext):
                return Fmt
        # [ARG]: should we raise some error if non-exist ?
        # assert False, "no Format found" # noqa: B011
        return NoneFormat

    @classmethod
    def get_module_class_from_extension(cls, ext: str) -> ModuleClassType:
        Fmt: FormatClassType = cls.get_format_class_from_extension(ext=ext)
        if Fmt:
            if hasattr(Fmt, "module") and Fmt.module is not None:
                return Fmt.module
            else:
                raise AttributeError(f"'module' attribute is not defined at {Fmt}")
        else:
            # [ARG]: should we raise some error if non-exist ?
            # assert False, "no module found" # noqa: B011
            return NoneModule


class ObjectFormat2Module(object):  # [ARG]: rename ?
    # [TODO]: use hash  to faster loading... ( Obj.load_objects takes much time at first )
    def get_module_from_object(obj, fmt=None) -> ModuleClassType:
        # [TODO]: In the future, I'd like to use hashed-key for quick search
        # [TDOO]: If fmt is given, it uses it with high priority
        # [TODO]: If necessary, also returns format (may be used to decide filename extention ?)

        for _, Obj in Object.registered_objects.items():
            Obj.load_objects()  # [TODO]: may be removed because we do it at the time on accessing to Obj.object right later
            # [ARG]: should we allow several options to check object natching by adding some attributes for control at Object class ?
            if isinstance(obj, Obj.object):
                if hasattr(Obj, "module") and Obj.module is not None:
                    module = Obj.module
                    return module
                elif hasattr(Obj, "module_checker") and Obj.module_checker is not None:
                    if hasattr(Obj, "format") and Obj.format is not None:
                        fmt = Obj.format
                        print("[DEBUG]: Obj.format", fmt)
                    elif hasattr(Obj, "format_checker") and Obj.format_checker is not None:
                        fmt = Obj.format_checker(obj)
                        print("[DEBUG]: Obj.format_checker", fmt)
                    module = Obj.module_checker(obj, fmt)
                    print("[DEBUG]: module", module)
                    return module
                else:
                    print("[DEBUG]: pass", Obj)
                    pass
        # [ARG]: should we raise some error if non-exist ?
        # assert False, "no object found" # noqa: B011
        return NoneModule
