import io
from typing import Optional, Any, Dict
import pandas as pd
from pandas import DataFrame

from algoralabs.common.requests import __post_request, __async_post_request
from algoralabs.common.functions import no_transform
from algoralabs.data_engine import TransformOverride
from algoralabs.decorators.data import data_request, async_data_request


def _analyze_data_request_info(data: pd.DataFrame) -> dict:
    parquet_bytes = data.to_parquet()

    return {
        'endpoint': "data-engine/alpha/analyze",
        'files': {'file': parquet_bytes}
    }


@data_request(transformer=no_transform)
def analyze_data(data: pd.DataFrame) -> Dict[str, Any]:
    request_info = _analyze_data_request_info(data)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_analyze_data(data: pd.DataFrame) -> Dict[str, Any]:
    request_info = _analyze_data_request_info(data)
    return await __async_post_request(**request_info)


def _transform_data_request_info(data: pd.DataFrame, transform_override: Optional[TransformOverride] = None) -> dict:
    if transform_override is not None:
        transform_override = {'transform_override': transform_override.json()}
    else:
        transform_override = None

    parquet_bytes = data.to_parquet()

    return {
        'endpoint': f"data-engine/alpha/transform",
        'data': transform_override,
        'files': {'file': parquet_bytes}
    }


@data_request(processor=lambda r: r.content, transformer=lambda r: pd.read_parquet(io.BytesIO(r)))
def transform_data(data: pd.DataFrame, transform_override: Optional[TransformOverride] = None) -> DataFrame:
    request_info = _transform_data_request_info(data, transform_override)
    return __post_request(**request_info)


@async_data_request(processor=lambda r: r.content, transformer=lambda r: pd.read_parquet(io.BytesIO(r)))
async def async_transform_data(data: pd.DataFrame, transform_override: Optional[TransformOverride] = None) -> DataFrame:
    request_info = _transform_data_request_info(data, transform_override)
    return await __async_post_request(**request_info)
