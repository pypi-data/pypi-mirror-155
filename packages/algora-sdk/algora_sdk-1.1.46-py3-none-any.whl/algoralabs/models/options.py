from typing import Optional

from algoralabs.common.requests import __post_request, __async_post_request
from algoralabs.common.functions import no_transform
from algoralabs.decorators.data import data_request, async_data_request
from algoralabs.models import OptionStyle, OptionType, OptionModel, OptionModelRequest


def _option_price_request_info(
        strike_price: float,
        underlying_price: float,
        volatility: float,
        days_until_expiration: int,
        style: OptionStyle = OptionStyle.EUROPEAN,
        model: OptionModel = OptionModel.BLACK_SCHOLES,
        type: Optional[OptionType] = None,
        interest_rate: Optional[float] = None,
        dividend_yield: Optional[float] = None
) -> dict:
    return {
        'endpoint': "data-engine/alpha/price/option",
        'data': OptionModelRequest(
            model=model,
            style=style,
            type=type,
            interest_rate=interest_rate,
            dividend_yield=dividend_yield,
            days_until_expiration=days_until_expiration,
            strike_price=strike_price,
            underlying_price=underlying_price,
            volatility=volatility,
        ).json()
    }


@data_request(transformer=no_transform)
def option_price(
        strike_price: float,
        underlying_price: float,
        volatility: float,
        days_until_expiration: int,
        style: OptionStyle = OptionStyle.EUROPEAN,
        model: OptionModel = OptionModel.BLACK_SCHOLES,
        type: Optional[OptionType] = None,
        interest_rate: Optional[float] = None,
        dividend_yield: Optional[float] = None
) -> float:
    request_info = _option_price_request_info(
        strike_price,
        underlying_price,
        volatility,
        days_until_expiration,
        style,
        model,
        type,
        interest_rate,
        dividend_yield
    )

    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_option_price(
        strike_price: float,
        underlying_price: float,
        volatility: float,
        days_until_expiration: int,
        style: OptionStyle = OptionStyle.EUROPEAN,
        model: OptionModel = OptionModel.BLACK_SCHOLES,
        type: Optional[OptionType] = None,
        interest_rate: Optional[float] = None,
        dividend_yield: Optional[float] = None
) -> float:
    request_info = _option_price_request_info(
        strike_price,
        underlying_price,
        volatility,
        days_until_expiration,
        style,
        model,
        type,
        interest_rate,
        dividend_yield
    )

    return await __async_post_request(**request_info)
