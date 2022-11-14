#
# https://www.cboe.com/us/equities/support/technical/
#

from typing import List

from .time import Time
from .add_order import AddOrderLong
from .order_executed import OrderExecuted


#
# LabVIEW Interface
#
# The following functions are meant to be called from LabVIEW by
# using the Python Connectivity Palette
#

def get_time(parameters) -> List[int]:
    seconds_since_midnight = getattr(parameters, 'Seconds Since Midnight')
    return list(Time.from_parms(time=seconds_since_midnight).get_bytes())


def get_add_order_long(parameters) -> List[int]:
    time_offset = getattr(parameters, 'Time Offset')
    order_id = getattr(parameters, 'Order Id')
    side = getattr(parameters, 'Side Indicator')
    quantity = getattr(parameters, 'Quantity')
    symbol = getattr(parameters, 'Symbol')
    price = getattr(parameters, 'Price')
    msg_bytes = AddOrderLong.from_parms(time_offset=time_offset,
                                        order_id=order_id,
                                        side=side,
                                        quantity=quantity,
                                        symbol=symbol,
                                        price=price).get_bytes()
    return list(msg_bytes)


def get_order_executed(parameters) -> List[int]:
    time_offset = getattr(parameters, 'Time Offset')
    order_id = getattr(parameters, 'Order Id')
    executed_quantity = getattr(parameters, 'Executed Quantity')
    execution_id = getattr(parameters, 'Execution Id')
    msg_bytes = OrderExecuted.from_parms(time_offset=time_offset,
                                         order_id=order_id,
                                         executed_quantity=executed_quantity,
                                         execution_id=execution_id).get_bytes()
    return list(msg_bytes)
