from typing import Dict, Any

from algoralabs.common.requests import __get_request, __async_get_request
from algoralabs.decorators.data import data_request, async_data_request


def _get_research_requet_info(id: str) -> dict:
    return {
        'endpoint': f"config/research/research/{id}"
    }


@data_request(transformer=lambda data: data)
def get_research(id: str) -> Dict[str, Any]:
    request_info = _get_research_requet_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=lambda data: data)
async def async_get_research(id: str) -> Dict[str, Any]:
    request_info = _get_research_requet_info(id)
    return await __async_get_request(**request_info)
