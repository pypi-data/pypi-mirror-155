from typing import Dict, Any

from algoralabs.common.functions import no_transform
from algoralabs.common.requests import __get_request, __delete_request, __async_get_request, __async_delete_request
from algoralabs.decorators.data import data_request, async_data_request


def _get_resource_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/research/resource/{id}/code"
    }


@data_request(transformer=lambda data: data, processor=lambda response: response.content)
def get_resource(id: str) -> Dict[str, Any]:
    request_info = _get_resource_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=lambda data: data, processor=lambda response: response.content)
async def get_resource(id: str) -> Dict[str, Any]:
    request_info = _get_resource_request_info(id)
    return await __async_get_request(**request_info)


def _delete_resource_request_info(id: str):
    return {
        'endpoint': f"config/research/resource/{id}"
    }


@data_request(transformer=no_transform)
def delete_resource(id: str) -> None:
    request_info = _delete_resource_request_info(id)
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_resource(id: str) -> None:
    request_info = _delete_resource_request_info(id)
    return await __async_delete_request(**request_info)
