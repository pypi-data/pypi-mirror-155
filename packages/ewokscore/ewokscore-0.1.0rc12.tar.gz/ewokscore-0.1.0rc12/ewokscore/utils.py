import os
import importlib
from datetime import datetime
from collections.abc import Mapping, Sequence


def qualname(obj):
    return obj.__module__ + "." + obj.__name__


def import_qualname(qualname):
    if not isinstance(qualname, str):
        raise TypeError(qualname, type(qualname))
    module_name, dot, obj_name = qualname.rpartition(".")
    if not module_name:
        raise ImportError(f"cannot import {qualname}")
    module = importlib.import_module(module_name)
    try:
        return getattr(module, obj_name)
    except AttributeError:
        raise ImportError(f"cannot import {obj_name} from {module_name}")


def import_method(qualname):
    method = import_qualname(qualname)
    if not callable(method):
        raise RuntimeError(repr(qualname) + " is not callable")
    return method


def instantiate_class(class_name: str, *args, **kwargs):
    cls = import_qualname(class_name)
    return cls(*args, **kwargs)


def dict_merge(
    destination, source, overwrite=False, _nodes=None, contatenate_sequences=False
):
    """Merge the source into the destination"""
    if _nodes is None:
        _nodes = tuple()
    for key, value in source.items():
        if key in destination:
            _nodes += (str(key),)
            if isinstance(destination[key], Mapping) and isinstance(value, Mapping):
                dict_merge(
                    destination[key],
                    value,
                    overwrite=overwrite,
                    _nodes=_nodes,
                    contatenate_sequences=contatenate_sequences,
                )
            elif value == destination[key]:
                continue
            elif overwrite:
                destination[key] = value
            elif (
                contatenate_sequences
                and isinstance(destination[key], Sequence)
                and isinstance(value, Sequence)
            ):
                destination[key] += value
            else:
                raise ValueError("Conflict at " + ".".join(_nodes))
        else:
            destination[key] = value


def fromisoformat(s: str) -> datetime:
    if hasattr(datetime, "fromisoformat"):
        return datetime.fromisoformat(s)
    else:
        # python < 3.7
        return datetime.strptime(s[:-3] + s[-2:], "%Y-%m-%dT%H:%M:%S.%f%z")


def makedirs_from_filename(filename: str):
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
