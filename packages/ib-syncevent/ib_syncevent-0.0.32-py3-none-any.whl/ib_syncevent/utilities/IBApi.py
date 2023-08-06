from __future__ import annotations

import threading
from decimal import Decimal

from ibapi.client import EClient, Order, Contract
from ibapi.wrapper import EWrapper
from ibapi.client import BarData
from ibapi.contract import ContractDetails
from ibapi.scanner import ScanData
from ibapi.tag_value import TagValue
from ibapi.order_state import OrderState

from .Enums import Events
from .IBDataReciver import IBDataReciver
from .IBEvents import IBEvents


class IBApi(EWrapper, EClient):

    def __init__(self, events_thread: dict[Events, threading.Event], global_state: IBDataReciver, ib_handlers: IBEvents) -> None:

        self.global_state = global_state

        self.ib_handlers = ib_handlers

        self.event_thread = events_thread

        self.counter = 0

        # Initial Eclient
        EClient.__init__(self, self)

    def error(self, reqId: int, errorCode: int, errorString: str):
        service = self.global_state.service if self.global_state.service else 'IBApi'
        print(
            f"ERROR [{service}] [{reqId}] [{errorCode}] [{errorString}]")
        if self.global_state.service == Events.HISTORICAL_DATA.value:
            self.event_thread[Events.HISTORICAL_DATA].set()
        if self.global_state.service == Events.SCANNER_DATA.value:
            self.event_thread[Events.CANCEL_DATA].set()

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

    def historicalData(self, reqId: int, bar: BarData) -> None:
        if self.ib_handlers.historical_bars_event:
            self.ib_handlers.historical_bars_event(bar)
        else:
            self.global_state.append_historical_bar(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str) -> None:
        self.event_thread[Events.HISTORICAL_DATA].set()

    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails, distance: str, benchmark: str, projection: str, legsStr: str):
        scan_data = ScanData(
            contractDetails.contract, rank, distance, benchmark, projection, legsStr)
        self.global_state.append_scanner_result(scan_data)
        self.event_thread[Events.SCANNER_DATA].set()

    def scannerDataEnd(self, reqId: int):
        self.event_thread[Events.CANCEL_DATA].set()

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        self.global_state.set_account_summary_tag(TagValue(tag, value))
        self.event_thread[Events.ACCOUNT_DATA].set()

    def accountSummaryEnd(self, reqId: int):
        pass

    def orderStatus(self, orderId: int, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        if self.ib_handlers.order_status:
            self.ib_handlers.order_status(orderId, status, filled, remaining, avgFillPrice,
                                          permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def openOrder(self, orderId: int, contract: Contract, order: Order, orderState: OrderState):
        if self.ib_handlers.open_order:
            self.ib_handlers.open_order(orderId, contract, order, orderState)
