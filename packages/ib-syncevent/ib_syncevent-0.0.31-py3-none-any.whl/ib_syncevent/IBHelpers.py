from __future__ import annotations

from ibapi.client import Contract, Order
from ibapi.scanner import ScannerSubscription
from ibapi.tag_value import TagValue

from .utilities import Actions


class IBHelpers():
    def create_contract(symbol: str, sec_type: str, exchange: str, primaryExchange: str, currency: str) -> Contract:
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange
        contract.primaryExchange = primaryExchange
        contract.currency = currency
        return contract

    def create_scanner_subscription(scan_code: str, instrument: str, locationCode: str, numberOfRows: int, abovePrice: int, aboveVolume: int) -> ScannerSubscription:
        scanner = ScannerSubscription()
        scanner.scanCode = scan_code
        scanner.instrument = instrument
        scanner.locationCode = locationCode
        scanner.numberOfRows = numberOfRows
        scanner.abovePrice = abovePrice
        scanner.aboveVolume = aboveVolume
        return scanner

    def create_tag_value(tag: str, value) -> TagValue:
        tag_value = TagValue()
        tag_value.tag = tag
        tag_value.value = value
        return tag_value

    def create_bracket_order(order_id: int, action: Actions, order_type: str, total_quantity: float, aux_price: float, lmt_price: float) -> Order:
        parent = Order()
        parent.orderId = order_id
        parent.action = action
        parent.orderType = order_type
        parent.totalQuantity = total_quantity
        parent.auxPrice = aux_price
        parent.lmtPrice = lmt_price

    def create_bracket_order(order_id: int, action: Actions, quantity: float, lmt_price: float, sl_price: float, tp_price: float, group_name: str) -> list[Order]:
        parent = Order()
        parent.orderId = order_id
        parent.action = action
        parent.orderType = "STP"
        parent.totalQuantity = quantity
        parent.auxPrice = lmt_price
        parent.eTradeOnly = False
        parent.firmQuoteOnly = False
        parent.transmit = False
        parent.ocaGroup = group_name

        slOrder = Order()
        slOrder.orderId = parent.orderId + 1
        slOrder.action = "SELL" if action == "BUY" else "BUY"
        slOrder.orderType = "STP"
        slOrder.totalQuantity = quantity
        slOrder.auxPrice = sl_price
        slOrder.parentId = order_id
        slOrder.eTradeOnly = False
        slOrder.firmQuoteOnly = False
        slOrder.transmit = False
        slOrder.ocaGroup = group_name

        tpOrder = Order()
        tpOrder.orderId = parent.orderId + 2
        tpOrder.action = "SELL" if action == "BUY" else "BUY"
        tpOrder.orderType = "LMT"
        tpOrder.totalQuantity = quantity
        tpOrder.lmtPrice = tp_price
        tpOrder.parentId = order_id
        tpOrder.eTradeOnly = False
        tpOrder.firmQuoteOnly = False
        tpOrder.transmit = True
        tpOrder.ocaGroup = group_name

        bracket_order = [parent, slOrder, tpOrder]
        return bracket_order
