from enum import Enum


class Events(Enum):
    HISTORICAL_DATA = "HISTORICAL_DATA"
    SCANNER_DATA = "SCANNER_DATA"
    ACCOUNT_DATA = "ACCOUNT_DATA"
    CANCEL_DATA = "CANCEL_DATA"
    ORDER_DATA = "ORDER_DATA"

class Actions(Enum):
    BUY = "BUY"
    SELL = "SELL"
