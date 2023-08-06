from __future__ import annotations

import importlib

from brane.core.base import BaseSubclassRegister, MetaFalse
from brane.core.utils import integrate_args, integrate_kwargs
from brane.typing import *  # noqa: F403


class MetaModule(type):
    def __new__(cls, classname: str, bases: tuple[type], class_info: dict):  # [TODO]: refine typing
        new_class_info: dict = class_info.copy()
        if new_class_info.get("name", None) is None:
            new_class_info["name"] = new_class_info.get("module_name", None)

        print(f"[DEBUG]: in MetaModule class_info={new_class_info}")
        return type.__new__(cls, classname, bases, new_class_info)

    # [TODO] python>=3.9, move to class as classmethod property
    @property
    def registered_modules(cls) -> dict:  # [TODO]: refine typing
        return cls._registered_subclasses


class Module(ModuleClassType, BaseSubclassRegister, metaclass=MetaModule):
    """
    Needed to be inheritated. The child class correspond to module.

    Args:
        name:
        loaded:
        reload_modules:
        read:
        write:

        module_name:
        module:

        module_read_method_name:
        module_read_method:
        file_read_method_name:
        file_open_for_read:
        open_mode_for_read:
        transform:
        transform_name:
        transform_info:
        object_transform_method_name:

        module_write_method_name:
        module_write_method:
        writer_method_name:
        object_write_method_name:
        file_write_method_name:
        file_open_for_write:
        open_mode_for_write:

        file_arg_first:
        object_unpacking_type:
        file_keyword_at_write:
        obj_keyword_at_write:

        base_args_read:
        base_kwargs_read:
        base_args_write:
        base_kwargs_write:
        generate_params_read:
        generate_params_write:

        filesystems:

    Note:
        Argument version v0.0
    """

    # [ARG]: may split two type of classes
    # 1. Base Module class which should be inheritated
    # 2. Config Module class defined here

    _registered_subclasses: dict = {}
    priority: int = 50

    # should be unqiue. package name specifed at pip install is usually set
    name: Optional[str] = None
    # module name for base. allow the string like "module1.module2"
    module_name: Optional[str] = None
    # the module specified by the module_name is set at load_modules method
    module: Any = None
    # temporal / experimental
    loaded: bool = False

    module_read_method: Optional[Callable] = None
    module_read_method_name: Optional[str] = None
    file_read_method_name: Optional[str] = None
    file_open_for_read: bool = False
    open_mode_for_read: dict[str, Any] = {"mode": "r"}
    transform: Optional[Callable] = None
    transform_name: Optional[str] = None
    transform_info: Optional[tuple[str, ...]] = None
    object_transform_method_name: Optional[str] = None

    module_write_method: Callable = None
    module_write_method_name: Optional[str] = None
    writer_method_name: Optional[str] = None
    object_write_method_name: Optional[str] = None
    file_write_method_name: Optional[str] = None
    file_open_for_write: bool = False
    open_mode_for_write: dict[str, Any] = {"mode": "w"}

    file_arg_first: bool = True
    object_unpacking_type: str = None
    file_keyword_at_write: Optional[str] = None
    obj_keyword_at_write: Optional[str] = None

    base_args_read: tuple = ()
    base_kwargs_read: dict = {}
    base_args_write: tuple = ()
    base_kwargs_write: dict = {}
    generate_params_read = None  # unnecessary ?
    generate_params_write = None

    filesystems: dict = {}

    @classmethod
    def load_modules(cls):
        """lazy loading of modules and setting their attributes or methods to this class."""
        if cls.loaded:
            return None

        if getattr(cls, "module_name", None):
            if cls.module is None:
                cls.module = importlib.import_module(cls.module_name)

        # set read method
        if getattr(cls, "module_read_method_name", None):
            cls.module_read_method = getattr(cls.module, cls.module_read_method_name)
        elif getattr(cls, "file_read_method_name", None):
            pass
        else:
            pass
            # # [ARGS]: other error type ?
            # raise ValueError(
            #     "neither 'module_read_method_name' nor 'file_read_method_name' is undefined"
            # )
        if getattr(cls, "transform_name", None):
            cls.transform = getattr(cls.module, cls.transform_name)
        if getattr(cls, "transform_info", None):
            transform_module_name, *attrs = cls.transform_info
            method = importlib.import_module(transform_module_name)
            for attr in attrs:
                method = getattr(method, attr)
            cls.transform = method

        # set write method
        if getattr(cls, "module_write_method_name", None):
            cls.module_write_method = getattr(cls.module, cls.module_write_method_name)
        elif getattr(cls, "object_write_method_name", None):
            pass
        elif getattr(cls, "file_write_method_name", None):
            pass
        else:
            pass
            # # [ARGS]: other error type ?
            # raise ValueError(
            #     "neither 'module_write_method_name', 'object_write_method_name' nor 'file_write_method_name' is undefined"
            # )

        cls.loaded = True

    @classmethod
    def reload_modules(cls):
        """reload modules or re-setting attributes or methods."""
        cls.loaded = False
        cls.load_modules()

    @classmethod
    def read(
        cls,
        path: Optional[PathType] = None,
        file: Optional[FileType] = None,
        io: Optional[IOType] = None,
        *args,
        **kwargs,
    ) -> Any:
        """read from path or file stream.

        Args:
            path: path object
            file: file stream object

        Returns:
            Any: loaded objects
        """
        if path is None and file is None:
            raise ValueError("Either path or file argument should be not None.")

        # generate the args and keyword args passed to read method
        base_args_read, base_kwargs_read = cls.base_args_read, cls.base_kwargs_read.copy()
        # [ARG]: unnecessary
        # if cls.generate_params_read:
        #     base_args_read, base_kwargs_read = cls.generate_params_read(base_args_read, base_kwargs_read)

        args_read: tuple = integrate_args(base_args_read, args)
        kwargs_read: dict = integrate_kwargs(base_kwargs_read, kwargs)

        if file is None:
            if cls.file_open_for_read:
                file = io.open(path, **cls.open_mode_for_read)
            else:
                file = path
        assert file is not None

        if cls.module_read_method:
            obj = cls.module_read_method(file, *args_read, **kwargs_read)
        elif cls.file_read_method_name:  # file read object
            if not hasattr(file, cls.file_read_method_name):
                raise AttributeError()  # [TODO]: error messsage
            obj = getattr(file, cls.file_read_method_name)(*args_read, **kwargs_read)
        else:
            raise NotImplementedError

        # do post-process
        if cls.transform:
            obj = cls.transform(obj)
        if cls.object_transform_method_name:
            if not hasattr(obj, cls.object_transform_method_name):
                raise AttributeError()  # [TODO]: error messsage
            obj = getattr(obj, cls.object_transform_method_name)()

        if cls.file_open_for_read:
            file.close()

        # [TODO]: assertion ( isinstance(obj, cls.object) ) if cls.object is not None
        return obj

    @classmethod
    def write(
        cls,
        obj: Any,
        path: Optional[PathType] = None,
        file: Optional[FileType] = None,
        io: Optional[IOType] = None,
        *args,
        **kwargs,
    ) -> Any:
        """write objects to the file specified by path object or file object.

        Args:
            obj: object to save
            path: path object
            file: file stream object
        """
        if path is None and file is None:
            raise ValueError("Either path or file argument should be not None.")

        base_args_write, base_kwargs_write = cls.base_args_write, cls.base_kwargs_write.copy()
        if cls.generate_params_write:
            base_args_write, base_kwargs_write = cls.generate_params_write(obj, base_args_write, base_kwargs_write)

        args_write = integrate_args(base_args_write, args)
        kwargs_write = integrate_kwargs(base_kwargs_write, kwargs)

        if file is None:
            if cls.file_open_for_write:
                file = io.open(path, **cls.open_mode_for_write)
            else:
                file = path

        """ Patterns
        # pass both file & obj at the same time
        * condition:
            * (module_write_method_name is not None)
            * (writer_method_name is None)

        ## both positional arguments
        * condition:
            * (object_unpacking_type != 'mapping')
        * call:
            * module.write(file, obj, *args, **kwargs)
                + condition:
                    + (file_arg_first is True)
                    + (object_unpacking_type == None)
                + (file, obj, *args, ), { **kwargs }
            * module.write(file, *obj, **kwargs)
                + condition:
                    + (file_arg_first is True)
                    + (object_unpacking_type == 'sequence')
                + (file, *obj, ), { **kwargs }
            * module.write(obj, file, *args, **kwargs)
                + condition:
                    + (file_arg_first is False)
                    + (object_unpacking_type == None)
                + (obj, file, *args ), { **kwargs }
            * module.write(*obj, file, **kwargs)
                + condition:
                    + (file_arg_first is False)
                    + (object_unpacking_type == 'sequence')
                + (*obj, file, ), { **kwargs }

        ## file is positional and object is keyword argument
        * condition:
            * (object_unpacking_type == 'mapping')
            * (file_keyword_at_write is None)
        * call:
            * module.write(file, obj=obj, **kwargs)
                + condition:
                    + (obj_keyword_at_write is not None)
                + (file,), { obj: obj, **kwargs }
            * module.write(file, **obj)
                + condition:
                    + (obj_keyword_at_write is None)
                + (file,), { **obj }

        ## both keyword arguments
        * condition:
            * (object_unpacking_type == 'mapping')
            * (file_keyword_at_write is not None)
        * call:
            * module.write(file=file, obj=obj, **kwargs)
                + (), { file: file, obj: obj, **kwargs }

        # pass only file and then write object
        * condition:
            * (module_write_method_name is not None)
            * (writer_method_name is not None)
        * call:
            * module.write(file, *args, **kwargs).write(obj)
                + condition:
                    + (object_unpacking_type is None)
                + (file, *args, ), { **kwargs }
            * module.write(file, *args, **kwargs).write(*obj)
                + condition:
                    + (object_unpacking_type == 'sequence')
                + (file, *args, ), { **kwargs }
            * module.write(file, *args, **kwargs).write(**obj)
                + condition:
                    + (object_unpacking_type == 'mapping')
                + (file, *args, ), { **kwargs }

        # object write file
        * condition:
            * (object_write_method_name is not None)
        * call:
            * obj.write(file, *args, **kwargs)
                + (file, *args), { **kwargs }

        """

        if cls.module_write_method_name:
            if cls.writer_method_name:  # pass only file and then write object
                writer = cls.module_write_method(file, *args_write, **kwargs_write)
                if not hasattr(writer, cls.writer_method_name):
                    raise AttributeError()  # [TODO]: error messsage
                if cls.object_unpacking_type is None:
                    getattr(writer, cls.writer_method_name)(obj)
                elif cls.object_unpacking_type == 'sequence':
                    getattr(writer, cls.writer_method_name)(*obj)
                elif cls.object_unpacking_type == 'mapping':
                    getattr(writer, cls.writer_method_name)(**obj)
                else:
                    raise NotImplementedError(f"object_unpacking_type: {cls.object_unpacking_type}")
            else:  # pass both file & obj at the same time
                if cls.object_unpacking_type is None:
                    if cls.file_arg_first:
                        cls.module_write_method(file, obj, *args_write, **kwargs_write)
                    else:
                        cls.module_write_method(obj, file, *args_write, **kwargs_write)
                elif object_unpacking_type == 'sequence':
                    if len(args_write) > 0:
                        raise AssertionError()  # [TODO]: error messsage
                    if cls.file_arg_first:
                        cls.module_write_method(file, *obj, **kwargs_write)
                    else:
                        cls.module_write_method(*obj, file, **kwargs_write)
                elif object_unpacking_type == 'mapping':
                    if len(args_write) > 0:
                        raise AssertionError()  # [TODO]: error messsage
                    args_, kwargs_ = list(), dict()
                    if cls.file_keyword_at_write:
                        kwargs_.update({cls.file_keyword_at_write: file})
                        if cls.obj_keyword_at_write:
                            kwargs_.update({cls.obj_keyword_at_write: obj})
                        else:
                            raise AssertionError
                    else:
                        args_.append(file)
                        if cls.obj_keyword_at_write:
                            kwargs_.update({cls.obj_keyword_at_write: obj})
                        else:
                            kwargs_.update(**obj)
                            if len(kwargs_write) > 0:
                                raise AssertionError()  # [TODO]: error messsage
                    cls.module_write_method(*args_, **kwargs_, **kwargs_write)
        elif cls.object_write_method_name:  # object write file
            if not hasattr(obj, cls.object_write_method_name):
                raise AttributeError()  # [TODO]: error messsage
            getattr(obj, cls.object_write_method_name)(file, *args_write, **kwargs_write)
        elif cls.file_write_method_name:  # file write object
            if not hasattr(file, cls.file_write_method_name):
                raise AttributeError()  # [TODO]: error messsage
            getattr(file, cls.file_write_method_name)(obj, *args_write, **kwargs_write)
        else:
            raise NotImplementedError

        if cls.file_open_for_write:
            file.close()


class MetaNoneModule(MetaModule, MetaFalse):  # [MEMO]: deprecated after removing MetaModule
    pass


class NoneModule(Module, metaclass=MetaNoneModule):
    valid = False  ###
    name = "None"

    # @classmethod # not work for class
    # def __bool__(cls):
    #    return False
