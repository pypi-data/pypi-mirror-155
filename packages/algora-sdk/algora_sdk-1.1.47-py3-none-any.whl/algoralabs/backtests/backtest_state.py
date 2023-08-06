import json
from typing import Dict, Any

from algoralabs.backtests import PortfolioStateRequest, CashPaymentRequest
from algoralabs.common.functions import no_transform
from algoralabs.common.requests import (
    __put_request, __async_put_request
)
from algoralabs.decorators.data import data_request, async_data_request


def _create_portfolio_state_request_info(request: PortfolioStateRequest) -> dict:
    return {
        "endpoint": "config/backtest/state/portfolio",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_portfolio_state(request: PortfolioStateRequest) -> Dict[str, Any]:
    request_info = _create_portfolio_state_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_portfolio_state(request: PortfolioStateRequest) -> Dict[str, Any]:
    request_info = _create_portfolio_state_request_info(request)
    return await __async_put_request(**request_info)


def _create_cash_payment_request_info(request: CashPaymentRequest) -> dict:
    return {
        "endpoint": "config/backtest/state/cash_payment",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_cash_payment(request: CashPaymentRequest) -> Dict[str, Any]:
    request_info = _create_cash_payment_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_cash_payment(request: CashPaymentRequest) -> Dict[str, Any]:
    request_info = _create_cash_payment_request_info(request)
    return await __async_put_request(**request_info)
