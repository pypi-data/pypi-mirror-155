# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import importlib as imlb
import json
import sys as sstm
from array import array as py_array_t
from datetime import date as date_t
from datetime import datetime as date_time_t
from datetime import time as time_t
from datetime import timedelta as time_delta_t
from datetime import timezone as time_zone_t
from enum import Enum as enum_t
from io import BytesIO as io_bytes_t
from pathlib import Path as path_t
from typing import Any, Callable, Dict, GenericAlias, Tuple, Union
from uuid import UUID as uuid_t

try:
    import matplotlib.pyplot as pypl
except ModuleNotFoundError:
    pypl = None
try:
    import networkx as grph
except ModuleNotFoundError:
    grph = None
try:
    import numpy as nmpy
except ModuleNotFoundError:
    nmpy = None
if nmpy is None:
    blsc = None
    pcst = None
    sprs = None
else:
    try:
        import blosc as blsc
    except ModuleNotFoundError:
        blsc = None
    try:
        import pca_b_stream as pcst
    except ModuleNotFoundError:
        pcst = None
    try:
        import scipy.sparse as sprs
    except ModuleNotFoundError:
        sprs = None


builders_h = Dict[str, Callable[[Any], Any]]
description_h = Tuple[str, Any]
descriptors_h = Dict[str, Callable[[Any], Any]]
object_h = Any
# When a module is not found, using bytes, the first type tested while JSONing, as the main module type is a safe way to
# "disable" it.
if pypl is None:
    figure_t = bytes
else:
    figure_t = pypl.Figure
if grph is None:
    _NX_GRAPH_CLASSES = bytes
else:
    _NX_GRAPH_CLASSES = (grph.Graph, grph.DiGraph, grph.MultiGraph, grph.MultiDiGraph)
if nmpy is None:
    array_t = bytes
else:
    array_t = nmpy.ndarray
if sprs is None:
    _SPARSE_ARRAY_CLASSES = bytes
else:
    _SPARSE_ARRAY_CLASSES = (
        sprs.bsr_array,
        sprs.coo_array,
        sprs.csc_array,
        sprs.csr_array,
        sprs.dia_array,
        sprs.dok_array,
        sprs.lil_array,
    )


DESCRIPTION_FOR_JSON = "__DescriptionForJSON__"
NEW_FROM_JSON_DESCRIPTION = "__NewFromJsonDescription__"

_MODULE_SEPARATOR = ":"  # Must be a character forbidden in any (qualified) name

_NUMPY_PLAIN_VERSION = "plain"
_NUMPY_COMPRESSED_VERSION = "compressed"
_BLOSC_VERSION = "blosc"
_BLOSC_BYTES_VERSION = "blosc.bytes"
_PCA_B_STREAM_VERSION = "pca_b_stream"
_NUMPY_NDARRAY_TO_VERSIONS = {}
_NUMPY_NDARRAY_FROM_VERSIONS = {}


def FullyQualifiedType(type_: Union[Any, type], /) -> str:
    """"""
    if type(type_) is not type:
        # type_ is actually an instance of type type_
        type_ = _DeAliasedType(type_)

    return f"{type_.__module__}{_MODULE_SEPARATOR}{type_.__name__}"


def _DeAliasedType(instance: Any, /) -> type:
    """"""
    if isinstance(instance, GenericAlias):
        return type(instance).__origin__

    return type(instance)


def _IsNamedTuple(instance: Any, /) -> bool:
    """"""
    instance_type = _DeAliasedType(instance)
    if hasattr(instance_type, "_make"):
        try:
            as_tuple = tuple(instance)
        except TypeError:
            return False

        return instance_type._make(as_tuple) == instance

    return False


def _IsFullyDataclassBased(instance_type: type, /) -> bool:
    """"""
    if dtcl.is_dataclass(instance_type):
        inheritance = instance_type.__mro__[1:]  # Exclude oneself
        if inheritance[0] is object:
            return True

        # Exclude object
        return all(_IsFullyDataclassBased(_typ) for _typ in inheritance[:-1])

    return False


def _TypeOfModule(type_: str, module: str, /) -> type:
    """"""
    imported = sstm.modules.get(module, None)
    if imported is None:
        # Do not put instead of "None" in "get" above since it will then be evaluated all the time, I suppose
        imported = imlb.import_module(module)

    return getattr(imported, type_)


def JsonStringOf(instance: Any, /, *, descriptors: descriptors_h = None) -> str:
    """"""
    return json.dumps(
        _JsonableVersionOf(instance, higher_level_call=True, descriptors=descriptors)
    )


def _JsonableVersionOf(
    instance: Any,
    /,
    *,
    higher_level_call: bool = False,
    descriptors: descriptors_h = None,
) -> description_h:
    """"""
    instance_type = _DeAliasedType(instance)
    fully_qualified = FullyQualifiedType(instance_type)

    if descriptors is None:
        descriptors = {}

    # Test for high-level classes first since they can also be subclasses of standard classes below
    in_descriptors_full = fully_qualified in descriptors
    in_descriptors_empty = higher_level_call and ("" in descriptors)
    if in_descriptors := (in_descriptors_full or in_descriptors_empty):
        DescriptionForJSON = None
    else:
        DescriptionForJSON = getattr(instance_type, DESCRIPTION_FOR_JSON, None)
    if in_descriptors or (DescriptionForJSON is not None):
        json_type = f"CUSTOM_{fully_qualified}"
        if in_descriptors_full:
            DescriptionForJSON = descriptors[fully_qualified]
        elif in_descriptors_empty:
            DescriptionForJSON = descriptors[""]
        description = DescriptionForJSON(instance)
        jsonable = _JsonableVersionOf(description, descriptors=descriptors)
    elif dtcl.is_dataclass(instance):
        if _IsFullyDataclassBased(instance_type):
            json_type = f"dataclass_{fully_qualified}"
            # Do not use dtcl.asdict(instance) since it recurses into dataclass instances which, if they extend a
            # "container" class like list or dict, might lose information.
            as_dict = {
                _fld.name: getattr(instance, _fld.name)
                for _fld in dtcl.fields(instance)
            }
            jsonable = _JsonableVersionOf(as_dict, descriptors=descriptors)
        else:
            json_type = f"UNHANDLED_dataclass_{fully_qualified}"
            jsonable = None
            print(
                f"{instance_type.__name__}: Dataclass with inheritance "
                f'without a "{DESCRIPTION_FOR_JSON}" method. Using None.'
            )
    # Must be the first type to be tested (see un-findable modules above)
    elif instance_type in (bytes, bytearray):
        # bytes.hex was initially used in place of bytes.decode
        json_type = instance_type.__name__
        jsonable = instance.decode(encoding="iso-8859-1")
    # Check datetime before date since a datetime is also a date
    elif instance_type is date_time_t:
        json_type = "datetime_datetime"
        jsonable = _JsonableVersionOf((instance.date(), instance.timetz()))
    elif instance_type is date_t:
        json_type = "datetime_date"
        jsonable = (instance.year, instance.month, instance.day)
    elif instance_type is time_t:
        json_type = "datetime_time"
        jsonable = (
            instance.hour,
            instance.minute,
            instance.second,
            instance.microsecond,
            _JsonableVersionOf(instance.tzinfo),
            instance.fold,
        )
    elif instance_type is time_delta_t:
        json_type = "datetime_timedelta"
        jsonable = (instance.days, instance.seconds, instance.microseconds)
    elif instance_type is time_zone_t:
        json_type = "datetime_timezone"
        jsonable = _JsonableVersionOf((instance.utcoffset(None), instance.tzname(None)))
    elif issubclass(instance_type, enum_t):
        # Do not use FullyQualifiedType here
        json_type = f"enum_Enum_{instance_type.__module__}{_MODULE_SEPARATOR}{instance_type.__name__}"
        jsonable = _JsonableVersionOf(instance.value, descriptors=descriptors)
    elif instance_type is py_array_t:
        json_type, jsonable = "array_array", (instance.tolist(), instance.typecode)
    elif instance_type is slice:
        json_type, jsonable = "slice", (instance.start, instance.stop, instance.step)
    # Check before looking for tuples since named tuples are subclasses of... tuples
    elif _IsNamedTuple(instance):
        json_type = f"typing_NamedTuple_{fully_qualified}"
        jsonable = _JsonableVersionOf(tuple(instance), descriptors=descriptors)
    elif instance_type in (frozenset, list, set, tuple):
        json_type = instance_type.__name__
        jsonable = [
            _JsonableVersionOf(_elm, descriptors=descriptors) for _elm in instance
        ]
    elif instance_type is dict:
        # json does not accept non-str dictionary keys, hence the json.dumps
        json_type = "dict"
        jsonable = {
            json.dumps(
                _JsonableVersionOf(_key, descriptors=descriptors)
            ): _JsonableVersionOf(_vle, descriptors=descriptors)
            for _key, _vle in instance.items()
        }
    elif issubclass(instance_type, path_t):
        json_type, jsonable = "pathlib_Path", str(instance)
    elif instance_type is io_bytes_t:
        # Buffer is assumed to be open (i.e. no instance.closed check)
        json_type = "io_BytesIO"
        jsonable = instance.getvalue().decode(encoding="iso-8859-1")
    elif instance_type is uuid_t:
        json_type, jsonable = "uuid_UUID", instance.int
    elif instance_type is array_t:
        json_type, jsonable = "numpy_ndarray", _AsMostConcise(instance)
    elif instance_type in _SPARSE_ARRAY_CLASSES:
        json_type, jsonable = f"scipy_{instance_type.__name__}", _AsMostConcise(
            instance.toarray()
        )
    elif instance_type in _NX_GRAPH_CLASSES:
        edges = grph.to_dict_of_dicts(instance)
        # /!\ Node attributes are added to the edges dictionary! This must be taken into account when deJSONing. Note
        # that several attempts to avoid this have been made, including one relying on repr(node), which is based on
        # hash(node). Since the hash function gives different results across Python sessions, this could not work.
        for node, attributes in instance.nodes(data=True):
            edges[node] = (attributes, edges[node])
        json_type = f"networkx_{instance_type.__name__}"
        jsonable = _JsonableVersionOf(edges, descriptors=descriptors)
    elif instance_type is figure_t:
        fake_file = io_bytes_t()
        instance.canvas.draw()
        instance.savefig(
            fake_file,
            bbox_inches="tight",
            pad_inches=0.0,
            transparent=True,
            dpi=200.0,
            format="png",
        )
        json_type = "matplotlib_pyplot_Figure"
        jsonable = fake_file.getvalue().decode(encoding="iso-8859-1")
        fake_file.close()
    else:
        try:
            _ = json.dumps(instance)
            json_type = f"STANDARD_{instance_type.__name__}"
            jsonable = instance
        except TypeError:
            json_type = f"UNHANDLED_{instance_type.__name__}"
            jsonable = None
            print(f"{json_type[10:]}: UnJSONable type. Using None.")

    return json_type, jsonable


def ObjectFromJsonString(jsoned: str, /, *, builders: builders_h = None) -> object_h:
    """"""
    return _ObjectFromUnJSONed(
        json.loads(jsoned), higher_level_call=True, builders=builders
    )


def _ObjectFromUnJSONed(
    description: description_h,
    /,
    *,
    higher_level_call: bool = False,
    builders: builders_h = None,
) -> object_h:
    """"""
    json_type, instance = description
    if json_type.startswith("UNHANDLED_"):
        print(f"{json_type[10:]}: UnJSONable type. Returning None.")
        return None

    if builders is None:
        builders = {}

    if json_type.startswith("CUSTOM_"):
        fully_qualified = json_type[7:]
        if fully_qualified in builders:
            Rebuilt = builders[fully_qualified]
        elif higher_level_call and ("" in builders):
            Rebuilt = builders[""]
        else:
            type_module, instance_type = fully_qualified.split(
                _MODULE_SEPARATOR, maxsplit=1
            )
            instance_type_t = _TypeOfModule(instance_type, type_module)
            Rebuilt = getattr(instance_type_t, NEW_FROM_JSON_DESCRIPTION, None)
        if Rebuilt is None:
            output = None
            print(f"{fully_qualified}: Type without builder. Returning None.")
        else:
            output = Rebuilt(_ObjectFromUnJSONed(instance, builders=builders))
    elif json_type.startswith("dataclass_"):
        type_module, dataclass = json_type[10:].split(_MODULE_SEPARATOR, maxsplit=1)
        dataclass_t = _TypeOfModule(dataclass, type_module)
        as_dict = _ObjectFromUnJSONed(instance, builders=builders)

        for_init = {}
        for field in dtcl.fields(dataclass_t):
            if field.init:
                # This could be limited to init fields without default values. However, all kind of things can happen in
                # init or post_init, so hopefully, the choice to ignore default values here works...
                name = field.name
                for_init[name] = as_dict[name]
        output = dataclass_t(**for_init)
        # Despite initial values being passed above, all the fields are reset here to their values at JSONing time,
        # again in case things happen in init or post_init.
        for key, value in as_dict.items():
            setattr(output, key, value)
    elif json_type in ("bytes", "bytearray"):
        output = instance.encode(encoding="iso-8859-1")
        if json_type == "bytearray":
            output = bytearray(output)
    elif json_type == "datetime_datetime":
        date, time = _ObjectFromUnJSONed(instance)
        output = date_time_t(
            date.year,
            date.month,
            date.day,
            time.hour,
            time.minute,
            time.second,
            time.microsecond,
            time.tzinfo,
            fold=time.fold,
        )
    elif json_type == "datetime_date":
        output = date_t(*instance)
    elif json_type == "datetime_time":
        time_zone = _ObjectFromUnJSONed(instance[4])
        as_dict = dict(
            zip(
                ("hour", "minute", "second", "microsecond", "tzinfo", "fold"),
                (*instance[:4], time_zone, *instance[5:]),
            )
        )
        output = time_t(**as_dict)
    elif json_type == "datetime_timedelta":
        output = time_delta_t(*instance)
    elif json_type == "datetime_timezone":
        time_delta, name = _ObjectFromUnJSONed(instance)
        output = time_zone_t(time_delta, name=name)
    elif json_type.startswith("enum_Enum_"):
        type_module, enum_type = json_type[10:].split(_MODULE_SEPARATOR, maxsplit=1)
        enum_e = _TypeOfModule(enum_type, type_module)
        output = enum_e(_ObjectFromUnJSONed(instance, builders=builders))
    elif json_type == "array_array":
        as_list, typecode = instance
        output = py_array_t(typecode)
        output.fromlist(as_list)
    elif json_type == "slice":
        output = slice(*instance)
    elif json_type.startswith("typing_NamedTuple_"):
        type_module, named_tuple = json_type[18:].split(_MODULE_SEPARATOR, maxsplit=1)
        named_tuple_t = _TypeOfModule(named_tuple, type_module)
        output = named_tuple_t._make(_ObjectFromUnJSONed(instance, builders=builders))
    elif json_type in ("frozenset", "list", "set", "tuple"):
        iterator = (_ObjectFromUnJSONed(_elm, builders=builders) for _elm in instance)
        if json_type == "frozenset":
            output = frozenset(iterator)
        elif json_type == "list":
            output = list(iterator)
        elif json_type == "set":
            output = set(iterator)
        else:
            output = tuple(iterator)
    elif json_type == "dict":
        output = {
            _ObjectFromUnJSONed(
                json.loads(_key), builders=builders
            ): _ObjectFromUnJSONed(_vle, builders=builders)
            for _key, _vle in instance.items()
        }
    elif json_type == "pathlib_Path":
        output = path_t(instance)
    elif json_type == "io_BytesIO":
        output = io_bytes_t(instance.encode(encoding="iso-8859-1"))
    elif json_type == "uuid_UUID":
        output = uuid_t(int=instance)
    elif json_type == "numpy_ndarray":
        output = _AsArray(*instance)
    elif json_type.startswith("scipy_"):
        sparse_type = json_type[6:]
        sparse_type_t = getattr(sprs, sparse_type)
        output = sparse_type_t(_AsArray(*instance))
    elif json_type.startswith("networkx_"):
        graph_type = json_type[9:]
        graph_type_t = getattr(grph, graph_type)

        edges_w_attributes = _ObjectFromUnJSONed(instance, builders=builders)
        attributes = {}
        edges = {}
        for node, (node_attributes, edge) in edges_w_attributes.items():
            attributes[node] = node_attributes
            edges[node] = edge

        output = grph.from_dict_of_dicts(edges, create_using=graph_type_t)
        grph.set_node_attributes(output, attributes)
    elif json_type == "matplotlib_pyplot_Figure":
        fake_file = io_bytes_t(instance.encode(encoding="iso-8859-1"))
        image = pypl.imread(fake_file)
        fake_file.close()
        output, axes = pypl.subplots()
        axes.set_axis_off()
        axes.matshow(image)
    elif json_type.startswith("STANDARD_"):
        output = instance
    else:
        raise ValueError(f"{json_type}: Invalid JSON type.")

    return output


def AddNumpyNDArrayRepresentation(
    name: str,
    /,
    *,
    ToVersion: Callable[[array_t], Tuple[int, str, str]] = None,
    FromVersion: Callable[[str], array_t] = None,
) -> None:
    """"""
    global _NUMPY_NDARRAY_TO_VERSIONS, _NUMPY_NDARRAY_FROM_VERSIONS

    if name in (_NUMPY_PLAIN_VERSION, _NUMPY_COMPRESSED_VERSION):
        raise ValueError(
            f"{_NUMPY_PLAIN_VERSION}, {_NUMPY_COMPRESSED_VERSION}: Reserved representation names"
        )

    if name == _BLOSC_VERSION:
        if blsc is None:
            raise ModuleNotFoundError('Module "blosc" not installed or unfoundable')
        _NUMPY_NDARRAY_TO_VERSIONS[_BLOSC_VERSION] = _BloscVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[_BLOSC_VERSION] = _FromBloscVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[_BLOSC_BYTES_VERSION] = _FromBloscBytesVersion
    elif name == _PCA_B_STREAM_VERSION:
        if pcst is None:
            raise ModuleNotFoundError(
                'Module "pca_b_stream" not installed or unfoundable'
            )
        _NUMPY_NDARRAY_TO_VERSIONS[_PCA_B_STREAM_VERSION] = _PCABStreamVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[_PCA_B_STREAM_VERSION] = _FromPCABStreamVersion
    else:
        if (ToVersion is None) or (FromVersion is None):
            raise ValueError(
                f'{name}: Invalid keyword-only arguments "ToVersion" and/or "FromVersion". '
                f"Actual={ToVersion}/{FromVersion}. Expected=Both non-None."
            )
        _NUMPY_NDARRAY_TO_VERSIONS[name] = ToVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[name] = FromVersion


def RemoveNumpyNDArrayRepresentation(name: str, /) -> None:
    """"""
    global _NUMPY_NDARRAY_TO_VERSIONS, _NUMPY_NDARRAY_FROM_VERSIONS

    if name in (_NUMPY_PLAIN_VERSION, _NUMPY_COMPRESSED_VERSION):
        raise ValueError(
            f"{_NUMPY_PLAIN_VERSION}, {_NUMPY_COMPRESSED_VERSION}: Default representations cannot be removed"
        )

    del _NUMPY_NDARRAY_TO_VERSIONS[name]
    del _NUMPY_NDARRAY_FROM_VERSIONS[name]
    if name == _BLOSC_VERSION:
        del _NUMPY_NDARRAY_FROM_VERSIONS[_BLOSC_BYTES_VERSION]


def _AsMostConcise(array: array_t, /) -> Tuple[str, str]:
    """"""
    version = json.dumps((array.tolist(), array.dtype.name))
    min_length = version.__len__()

    output = (_NUMPY_PLAIN_VERSION, version)

    fake_file = io_bytes_t()
    nmpy.savez_compressed(fake_file, array=array)
    version = fake_file.getvalue().decode(encoding="iso-8859-1")
    fake_file.close()
    length = version.__len__()
    if length < min_length:
        output, min_length = (_NUMPY_COMPRESSED_VERSION, version), length

    for ToVersion in _NUMPY_NDARRAY_TO_VERSIONS.values():
        version = ToVersion(array)
        length = version[1].__len__()
        if length < min_length:
            output, min_length = version, length

    return output


def _AsArray(how: str, what: str) -> array_t:
    """"""
    if how == _NUMPY_PLAIN_VERSION:
        data, dtype = json.loads(what)
        return nmpy.array(data, dtype=dtype)
    elif how == _NUMPY_COMPRESSED_VERSION:
        fake_file = io_bytes_t(what.encode(encoding="iso-8859-1"))
        output = nmpy.load(fake_file)["array"]
        fake_file.close()
        return output

    return _NUMPY_NDARRAY_FROM_VERSIONS[how](what)


def _BloscVersion(array: array_t, /) -> Tuple[str, str]:
    """"""
    # Do not compare packed instances of an array since blsc.pack_array(array) !=_{can be} blsc.pack_array(array)
    packed = blsc.pack_array(array)
    if isinstance(packed, bytes):
        packed = packed.decode(encoding="iso-8859-1")
        how = _BLOSC_BYTES_VERSION
    else:
        how = _BLOSC_VERSION

    return how, packed


def _FromBloscVersion(blosc: str, /) -> array_t:
    """"""
    return blsc.unpack_array(blosc)


def _FromBloscBytesVersion(blosc: str, /) -> array_t:
    """"""
    return blsc.unpack_array(blosc.encode(encoding="iso-8859-1"))


def _PCABStreamVersion(array: array_t, /) -> Tuple[str, str]:
    """"""
    stream = pcst.PCA2BStream(array).decode(encoding="iso-8859-1")
    return _PCA_B_STREAM_VERSION, stream


def _FromPCABStreamVersion(pca_b_stream: str, /) -> array_t:
    """"""
    return pcst.BStream2PCA(pca_b_stream.encode(encoding="iso-8859-1"))
