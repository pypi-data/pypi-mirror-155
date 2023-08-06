import json
from typing import Dict, Any

from algoralabs.backtests import BacktestRequest
from algoralabs.common.functions import no_transform
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)
from algoralabs.decorators.data import data_request, async_data_request


def _get_backtest_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/backtest/{id}"
    }


@data_request(transformer=no_transform)
def get_backtest(id: str) -> Dict[str, Any]:
    request_info = _get_backtest_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_backtest(id: str) -> Dict[str, Any]:
    request_info = _get_backtest_request_info(id)
    return await __async_get_request(**request_info)


def _get_backtests_request_info() -> dict:
    return {
        "endpoint": f"config/backtest"
    }


@data_request(transformer=no_transform)
def get_backtests() -> Dict[str, Any]:
    request_info = _get_backtests_request_info()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_backtests() -> Dict[str, Any]:
    request_info = _get_backtests_request_info()
    return await __async_get_request(**request_info)


def _create_backtest_request_info(request: BacktestRequest) -> dict:
    return {
        "endpoint": "config/backtest",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_backtest(request: BacktestRequest) -> Dict[str, Any]:
    request_info = _create_backtest_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_backtest(request: BacktestRequest) -> Dict[str, Any]:
    request_info = _create_backtest_request_info(request)
    return await __async_put_request(**request_info)


def _update_backtest_request_info(id: str, request: BacktestRequest):
    return {
        "endpoint": f"config/backtest/{id}",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_backtest(id: str, request: BacktestRequest) -> Dict[str, Any]:
    request_info = _update_backtest_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_backtest(id: str, request: BacktestRequest) -> Dict[str, Any]:
    request_info = _update_backtest_request_info(id, request)
    return await __async_post_request(**request_info)


def _delete_backtest_request_info(id: str):
    return {
        "endpoint": f"config/backtest/{id}",
    }


@data_request(transformer=no_transform)
def delete_backtest(id: str) -> None:
    request_info = _delete_backtest_request_info(id, )
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_backtest(id: str) -> None:
    request_info = _delete_backtest_request_info(id, )
    return await __async_delete_request(**request_info)


if __name__ == '__main__':
    print(get_backtests())
