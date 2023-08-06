from datetime import date
from enum import Enum
from typing import Optional

from algoralabs.common.base import Base


class BacktestType(Enum):
    STRATEGY = 'STRATEGY'
    BACKTEST = 'BACKTEST'


class BacktestStatus(Enum):
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'


class BacktestRequest(Base):
    strategy_id: str
    type: BacktestType
    status: BacktestStatus
    start_date: date
    end_date: date
    portfolio: str  # TODO replace with portfolio object in Quant SDK


class BacktestResponse(Base):
    id: str
    strategy_id: str
    type: BacktestType
    status: BacktestStatus
    start_date: date
    end_date: date
    portfolio: str  # TODO replace with portfolio object in Quant SDK
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class BacktestViewResponse(Base):
    id: str
    strategy_id: str
    strategy_name: str
    type: BacktestType
    status: BacktestStatus
    start_date: date
    end_date: date
    portfolio: str  # TODO replace with portfolio object in Quant SDK
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class BacktestEventType(Enum):
    PORTFOLIO = 'PORTFOLIO'
    CASH_PAYMENT = 'CASH_PAYMENT'


class BacktestEvent(Base):
    backtest_id: str
    backtest_type: BacktestEventType


class CashPaymentRequest(Base):
    backtest_id: str
    payment_date: date
    type: str
    amount: float
    position_id: Optional[str]
    currency: Optional[str]


class PortfolioStateRequest(Base):
    backtest_id: str
    date: date
    valuation: float
    pnl: float
    portfolio: str


class CashPaymentResponse(BacktestEvent):
    id: str
    backtest_id: str
    backtest_type: BacktestEventType
    payment_date: date
    type: str
    amount: float
    position_id: Optional[str]
    currency: Optional[str]
    created_at: int


class PortfolioStateResponse(BacktestEvent):
    id: str
    backtest_id: str
    backtest_type: BacktestEventType
    date: date
    valuation: float
    pnl: float
    portfolio: str
    created_at: int
