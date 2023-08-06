# IB_SyncEvent

Get financial data synchronously. This package is a wrapper around the IB API.

## Installation

```
pip install ib-syncevent
```

## Example (get historical data)
```python
from ib_syncevent import IBSyncEvent, IBHelpers

app = IBSyncEvent()

app.connect("127.0.0.1", 7497, 1)

"""
Request AAPL data, 60 seconds bar size 2022/05/12 16:59:00
"""

contract = IBHelpers.create_contract(
    symbol="AAPL", sec_type="STK", exchange="SMART", primaryExchange="ISLAND", currency="USD")

end_date_time = "20220512 17:00:00"

historical_bars = app.request_historical_bars(
    2, contract, end_date_time, "60 s", "1 min", "TRADES", 1, 1, False, None)


print(historical_bars)
