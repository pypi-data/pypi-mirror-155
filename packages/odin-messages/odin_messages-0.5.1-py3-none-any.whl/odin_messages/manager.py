from typing import Dict, Any
from odin_messages.base import BaseEventMessage


class OperatorLoansConfigMessage(BaseEventMessage):
    loans: Dict[str, float]
    target_exchange: str


class OperatorMinimumToTradeMessage(BaseEventMessage):
    exchange: str
    minimum_to_trade: Dict[str, float]


class OperatorMinimumLimitPriceMessage(BaseEventMessage):
    exchange: str
    minimum_limit_price: Dict[str, float]


class OperatorCostConfigMessage(BaseEventMessage):
    costs: Dict[str, float]


class OperatorIsActiveMessage(BaseEventMessage):
    active: bool


class OperatorConfigsMessage(BaseEventMessage):
    configs: Dict[str, Any]


class OperatorPricerConfigMessage(BaseEventMessage):
    pricer: Dict[str, Any]


class OperatorSizerConfigMessage(BaseEventMessage):
    sizer: Dict[str, Any]


class OperatorMarketSpreadsMessage(BaseEventMessage):
    market_spreads: Dict[str, Any]


class OperatorUSDCLPStock(BaseEventMessage):
    stock: Dict[str, Any]
