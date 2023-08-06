from __future__ import annotations

from ibapi.client import BarData
from ibapi.scanner import ScanData
from ibapi.tag_value import TagValue

from .Enums import Events

class IBDataReciver():
    def __init__(self) -> None:
        self.service = None

        self.historical_bars: list[BarData] = []

        self.scanner_results: list[ScanData] = []

        self.account_summary_tag: TagValue = None
    
    def set_service(self, service_name: Events):
        self.service = service_name
    
    def get_historical_bars(self) -> list[BarData]:
        return self.historical_bars

    def clear_historical_bars(self) -> None:
        self.historical_bars = []
    
    def append_historical_bar(self, historical_bar: BarData) -> None:
        self.historical_bars.append(historical_bar)
    
    def get_scanner_results(self) -> list[ScanData]:
        return self.scanner_results
    
    def clear_scanner_results(self) -> None:
        self.scanner_results = []
    
    def append_scanner_result(self, scanner_result: ScanData) -> None:
        self.scanner_results.append(scanner_result)
    
    def get_account_summary_tag(self) -> TagValue:
        return self.account_summary_tag   
    
    def clear_account_summary_tag(self) -> None:
        self.account_summary_tag = None
    
    def set_account_summary_tag(self, account_summary_tag: TagValue) -> None:
        self.account_summary_tag = account_summary_tag