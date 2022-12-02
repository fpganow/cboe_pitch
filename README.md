# cboe_pitch
Python Parser and Creator of CBOE PITCH Messages

## Based on
https://cdn.cboe.com/resources/membership/US_EQUITIES_OPTIONS_MULTICAST_PITCH_SPECIFICATION.pdf

## Create CBOE Pitch Messages

Good for generating test messages for your CBOE Pitch Parser

## Parse CBOE Pitch Messages

Good for testing your feed parser

- Using as a library
```
from pitch import AddOrderLong
message = AddOrderLong.from_parms(time_offset=447_000,
                                  order_id='ORID0001',
                                  side='B',
                                  quantity=20_000,
                                  symbol='AAPL',
                                  price=0.9050)

print(f'{message.get_bytes()}')
```

## See Also

I am using the code in this module to test a LabVIEW FPGA CBOE Pitch
Feed Handler and Filter

http://github.com/fpganow/cboe_pitch_lv_fpga

## Usage

See the tests

## Supported Message Types


Sequenced Unit Header
Heartbeat

| Message Type                 | Type | Source File              | Tests              | LabVIEW              |
|------------------------------|------|--------------------------|--------------------|----------------------|
| Time                         | 0x20 | /pitch/time.py           | :heavy_check_mark: | :heavy_check_mark:   |
| Add Order Long               | 0x21 | /pitch/add_order.py      | :heavy_check_mark: | :heavy_check_mark:   |
| Add Order Short              | 0x22 | /pitch/add_order.py      | :heavy_check_mark: | :heavy_check_mark:   |
| Add Order Expanded           | 0x2f | /pitch/add_order.py      | :heavy_check_mark: | :heavy_check_mark:   |
| Order Executed               | 0x23 | /pitch/order_executed.py | :heavy_check_mark: | :heavy_check_mark:   |
| Order Executed at Price/Size | 0x24 | /pitch/order_executed.py | :heavy_check_mark: | :heavy_check_mark:   |
| Reduce Size (long)           | 0x25 | /pitch/reduce_size.py    | :heavy_check_mark: | :heavy_check_mark:   |
| Reduce Size (short)          | 0x26 | /pitch/reduce_size.py    | :heavy_check_mark: | :heavy_check_mark:   |
| Modify Order (long)          | 0x27 | /pitch/modify.py         | :heavy_check_mark: | :heavy_check_mark:   |
| Modify Order (short)         | 0x28 | /pitch/modify.py         | :heavy_check_mark: | :heavy_check_mark:   |
| Delete Order                 | 0x29 | /pitch/delete_order.py   | :heavy_check_mark: | :heavy_check_mark:   |
| Trade (long)                 | 0x2a | /pitch/trade.py          | :heavy_check_mark: | :heavy_check_mark:   |
| Trade (short)                | 0x2b | /pitch/trade.py          | :heavy_check_mark: | :heavy_check_mark:   |
| Trade (expanded)             | 0x30 | /pitch/trade.py          | :heavy_check_mark: | :heavy_check_mark:   |


## Message Types not implemented

* Unit Clear
* Trade Break
* End of Session
* Trading Status
* Login (messageType = 0x01)
* Login Response (messageType = 0x02)
* Gap Request (messageType = 0x03)
* Gap Response (messageType = 0x04)

### Options
- not implemented -
