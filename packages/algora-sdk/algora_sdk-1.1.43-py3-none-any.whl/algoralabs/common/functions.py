"""
This module contains helpful functions
"""
import dataclasses
from calendar import calendar
from functools import reduce
from typing import Dict, Any, Union, List

import pandas as pd
from pandas import DataFrame

from algoralabs.common.types import Datetime


def coalesce(*args):
    """
    Coalesce operator returns the first arg that isn't None

    Parameters:
        *args: Tuple of args passed to the function

    Returns:
        The first non-None value in *args
    """
    return reduce(lambda x, y: x if x is not None else y, args)


def coalesce_callables(*args):
    """
    Coalesce operator returns the first arg that isn't None. If the arg is callable it will check that the value
    returned from calling the arg is not none and then return the value from calling it.

    WARNING: If an argument implements __call__ this method will evaluate the return of the __call__ method and return
    that instead of the argument itself. This is important when using python classes.

    Parameters:
        *args: Tuple of args passed to the function

    Returns:
        The first non-None value in *args
    """
    for arg in args:
        value = arg() if callable(arg) else arg
        if value is not None:
            return value
    return None


def dataclass_to_dict(data_cls: dataclasses.dataclass, remove_none: bool) -> dict:
    """
    This method gets all the dataclass fields (i.e. the key value pairs) and builds a dict representation

    Parameters:
        data_cls: The dataclass being converted to json
        remove_none: A flag used to remove key value pairs where the value is None from the json conversion

    Returns:
        A dict representation of the dataclass
    """

    def factory(data):
        return dict(x for x in data if not (x[1] is None and remove_none))

    return dict(dataclasses.asdict(data_cls, dict_factory=factory))


def no_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    return data


def to_pandas_with_index(data: Dict[str, Any], index: str = 'date') -> DataFrame:
    # necessary to drop column in order to avoid duplicates when converting to json
    return pd.DataFrame(data).set_index(index, drop=True)


def transform_one_or_many(
        data: Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]],
        key: str
) -> Union[DataFrame, Dict[str, DataFrame]]:
    if isinstance(data, dict):
        for s in data:
            data[s] = DataFrame(data[s][key])
        return data

    return DataFrame(data)


def date_to_timestamp(date: Datetime) -> int:
    return calendar.timegm(date.timetuple()) * 1000
