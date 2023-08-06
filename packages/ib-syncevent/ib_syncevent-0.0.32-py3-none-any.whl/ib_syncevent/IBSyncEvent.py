
from __future__ import annotations

import time
import threading
from threading import Thread
import functools

from .utilities import IBDataReciver
from .utilities import IBEvents
from .utilities import Events
from .utilities import IBApi

from ibapi.client import BarData, TagValueList, TickerId, Contract, Order
from ibapi.scanner import ScanData, ScannerSubscription
from ibapi.tag_value import TagValue


def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print ('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco


class IBSyncEvent():
    def __init__(self) -> None:
        self.global_state = IBDataReciver()

        self.ib_handlers = IBEvents()

        self.events_thread = {
            Events.HISTORICAL_DATA: threading.Event(),
            Events.SCANNER_DATA: threading.Event(),
            Events.ACCOUNT_DATA: threading.Event(),
            Events.CANCEL_DATA: threading.Event(),
        }

        self.ibapi = IBApi(self.events_thread,
                           self.global_state, self.ib_handlers)

        self.connection_thread = threading.Thread(
            target=self.ibapi.run, daemon=True)
        
        self.host = None
        self.port = None
        self.conId = None
    
    def connect(self, host: str, port: int, conId: int) -> None:
        self.host = host
        self.port = port
        self.conId = conId
        self.ibapi.connect(host, port, conId)
        self.connection_thread.start()
        time.sleep(1)

    def wait_for_connection(self):
        if not self.ibapi.isConnected():
            while not self.ibapi.isConnected():
                print('[IBSyncEvent] waiting for api connection...')
                time.sleep(30)
                self.ibapi.connect(self.host, self.port, self.conId)
                self.connection_thread = threading.Thread(target=self.ibapi.run,name='TradingApp')
                self.connection_thread.start()
            return

    @timeout(60)
    def request_historical_bars_from_ib(self, reqId: TickerId, contract: Contract, endDateTime: str, durationStr: str, barSizeSetting: str, whatToShow: str, useRTH: int, formatDate: int, keepUpToDate: bool, chartOptions: TagValueList) -> list[BarData] or None:
        self.global_state.set_service(Events.HISTORICAL_DATA.value)

        self.events_thread[Events.HISTORICAL_DATA].clear()
        self.ibapi.reqHistoricalData(reqId, contract, endDateTime, durationStr,
                                     barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)
        self.events_thread[Events.HISTORICAL_DATA].wait()

        if not self.ib_handlers.historical_bars_event:
            results = self.global_state.get_historical_bars()
            self.global_state.clear_historical_bars()
            return results
    
    def request_historical_bars(self, reqId: TickerId, contract: Contract, endDateTime: str, durationStr: str, barSizeSetting: str, whatToShow: str, useRTH: int, formatDate: int, keepUpToDate: bool, chartOptions: TagValueList) -> list[BarData] or None:
        self.wait_for_connection()
        try: 
            bars = self.request_historical_bars_from_ib(reqId, contract, endDateTime, durationStr,
                                        barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)
            return bars
        except Exception as e:
            self.ibapi.cancelHistoricalData(reqId)
            raise e

    def request_scanner_results(self, reqId: TickerId, subscription: ScannerSubscription, scannerSubscriptionOptions: list[TagValue], scannerSubscriptionFilterOptions: list[TagValue]) -> list[ScanData] or None:
        self.global_state.set_service(Events.SCANNER_DATA.value)

        self.events_thread[Events.SCANNER_DATA].clear()
        self.ibapi.reqScannerSubscription(
            reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions)
        self.events_thread[Events.SCANNER_DATA].wait()

        self.events_thread[Events.CANCEL_DATA].clear()
        self.ibapi.cancelScannerSubscription(reqId)
        self.events_thread[Events.CANCEL_DATA].wait()

        results = self.global_state.get_scanner_results()
        self.global_state.clear_scanner_results()
        return results

    def request_account_summary(self, reqId: TickerId, groupName: str, tags: str) -> TagValue or None:
        self.global_state.set_service(Events.ACCOUNT_DATA.value)

        self.events_thread[Events.ACCOUNT_DATA].clear()
        self.ibapi.reqAccountSummary(reqId, groupName, tags)
        self.events_thread[Events.ACCOUNT_DATA].wait()

        self.ibapi.cancelAccountSummary(reqId)

        results = self.global_state.get_account_summary_tag()
        self.global_state.clear_account_summary_tag()
        return results

    def place_order(self, reqId: TickerId, contract: Contract, order: Order) -> None:
        self.global_state.set_service(Events.ORDER_DATA.value)

        self.ibapi.placeOrder(reqId, contract, order)
        return