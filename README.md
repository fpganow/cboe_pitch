# cboe_pitch
Python Parser and Creator of CBOE PITCH Messages

## Based on
https://cdn.cboe.com/resources/membership/US_EQUITIES_OPTIONS_MULTICAST_PITCH_SPECIFICATION.pdf

## Supported Message Types


Sequenced Unit Header
Heartbeat

| Message Type                 | Type | Source File              | Tests | LabVIEW |
|------------------------------|------|--------------------------|-------|---------|
| Time                         | 0x20 | /pitch/time.py           | [x]   | [x]     |
| Unit Clear                   | 0x97 | /pitch/misc.py           | [ ]   | [ ]     |
| Add Order Long               | 0x21 | /pitch/add_order.py      | [x]   | [x]     |
| Add Order Short              | 0x22 | /pitch/add_order.py      | [x]   | [ ]     |
| Add Order Expanded           | 0x2f | /pitch/add_order.py      | [x]   | [ ]     |
| Order Executed               | 0x23 | /pitch/order_executed.py | [x]   | [x]     |
| Order Executed at Price/Size | 0x24 | /pitch/order_executed.py | [x]   | [ ]     |
| Reduce Size (long)           | 0x25 | /pitch/reduce_size.py    | [x]   | [ ]     |
| Reduce Size (short)          | 0x26 | /pitch/reduce_size.py    | [x]   | [ ]     |
| Modify Order (long)          | 0x27 | /pitch/modify.py         | [x]   | [ ]     |
| Modify Order (short)         | 0x28 | /pitch/modify.py         | [x]   | [ ]     |
| Delete Order                 | 0x29 | /pitch/delete_order.py   | [x]   | [ ]     |
| Trade (long)                 | 0x2a | /pitch/trade.py          | [x]   | [ ]     |
| Trade (short)                | 0x2b | /pitch/trade.py          | [x]   | [ ]     |
| Trade (expanded)             | 0x30 | /pitch/trade.py          | [x]   | [ ]     |
| Trade Break                  | 0x2c | /pitch/misc.py           | [ ]   | [ ]     |
| End of Session               | 0x2d | /pitch/misc.py           | [ ]   | [ ]     |

### Calculation of Execution IDs

### Gap Request Proxy Message
 - not implemented -
Login (messageType = 0x01)
Login Response (messageType = 0x02)
Gap Request (messageType = 0x03)
Gap Response (messageType = 0x04)

### Options
- not implemented -
