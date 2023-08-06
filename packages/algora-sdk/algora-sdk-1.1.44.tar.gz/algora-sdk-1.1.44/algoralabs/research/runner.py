from algoralabs.common.requests import __put_request, __async_put_request
from algoralabs.decorators.data import data_request, async_data_request


def _get_or_create_runner_request_info() -> dict:
    return {
        'endpoint': f"research-service/runner/deployment"
    }


@data_request(transformer=lambda data: data)
def get_or_create_runner() -> str:
    request_info = _get_or_create_runner_request_info()
    return __put_request(**request_info)


@async_data_request(transformer=lambda data: data)
async def get_or_create_runner() -> str:
    request_info = _get_or_create_runner_request_info()
    return await __async_put_request(**request_info)
