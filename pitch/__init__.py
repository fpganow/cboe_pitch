#
# https://www.cboe.com/us/equities/support/technical/
#

from typing import List

from .delete_order import DeleteOrder
from .modify import ModifyOrderLong, ModifyOrderShort
from .time import Time
from .add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from .order_executed import OrderExecuted, OrderExecutedAtPriceSize
from .reduce_size import ReduceSizeLong, ReduceSizeShort

#
# LabVIEW Interface
#
# The following functions are meant to be called from LabVIEW by
# using the Python Connectivity Palette
#
from .trade import TradeLong, TradeShort, TradeExpanded


def get_time(parameters) -> List[int]:
    seconds_since_midnight = getattr(parameters, "Time")
    return list(Time.from_parms(time=seconds_since_midnight).get_bytes())


def get_add_order_long(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    side = getattr(parameters, "Side Indicator")
    quantity = getattr(parameters, "Quantity")
    symbol = getattr(parameters, "Symbol")
    price = getattr(parameters, "Price")
    msg_bytes = AddOrderLong.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        side=side,
        quantity=quantity,
        symbol=symbol,
        price=price,
    ).get_bytes()
    return list(msg_bytes)


def get_add_order_short(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    side = getattr(parameters, "Side Indicator")
    quantity = getattr(parameters, "Quantity")
    symbol = getattr(parameters, "Symbol")
    price = getattr(parameters, "Price")
    msg_bytes = AddOrderShort.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        side=side,
        quantity=quantity,
        symbol=symbol,
        price=price,
    ).get_bytes()
    return list(msg_bytes)
    pass


def get_add_order_expanded(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    side = getattr(parameters, "Side Indicator")
    quantity = getattr(parameters, "Quantity")
    symbol = getattr(parameters, "Symbol")
    price = getattr(parameters, "Price")
    participant_id = getattr(parameters, "Participant Id")
    customer_indicator = getattr(parameters, "Customer Indicator")
    msg_bytes = AddOrderExpanded.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        side=side,
        quantity=quantity,
        symbol=symbol,
        price=price,
        participant_id=participant_id,
        customer_indicator=customer_indicator,
    ).get_bytes()
    return list(msg_bytes)


def get_order_executed(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    executed_quantity = getattr(parameters, "Executed Quantity")
    execution_id = getattr(parameters, "Execution Id")
    msg_bytes = OrderExecuted.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        executed_quantity=executed_quantity,
        execution_id=execution_id,
    ).get_bytes()
    return list(msg_bytes)


def get_reduce_size_long(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    canceled_quantity = getattr(parameters, "Canceled Quantity")

    msg_bytes = ReduceSizeLong.from_parms(
        time_offset=time_offset, order_id=order_id, canceled_quantity=canceled_quantity
    ).get_bytes()

    return list(msg_bytes)


def get_reduce_size_short(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    canceled_quantity = getattr(parameters, "Canceled Quantity")

    msg_bytes = ReduceSizeShort.from_parms(
        time_offset=time_offset, order_id=order_id, canceled_quantity=canceled_quantity
    ).get_bytes()

    return list(msg_bytes)


def get_modify_order_long(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    quantity = getattr(parameters, "Quantity")
    price = getattr(parameters, "Price")

    msg_bytes = ModifyOrderLong.from_parms(
        time_offset=time_offset, order_id=order_id, quantity=quantity, price=price
    ).get_bytes()

    return list(msg_bytes)


def get_modify_order_short(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    quantity = getattr(parameters, "Quantity")
    price = getattr(parameters, "Price")

    msg_bytes = ModifyOrderShort.from_parms(
        time_offset=time_offset, order_id=order_id, quantity=quantity, price=price
    ).get_bytes()

    return list(msg_bytes)


def get_delete_order(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")

    msg_bytes = DeleteOrder.from_parms(
        time_offset=time_offset, order_id=order_id
    ).get_bytes()

    return list(msg_bytes)


def get_trade_long(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    side = getattr(parameters, "Side Indicator")
    quantity = getattr(parameters, "Quantity")
    symbol = getattr(parameters, "Symbol")
    price = getattr(parameters, "Price")
    execution_id = getattr(parameters, "Execution Id")

    msg_bytes = TradeLong.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        side=side,
        quantity=quantity,
        symbol=symbol,
        price=price,
        execution_id=execution_id,
    ).get_bytes()

    return list(msg_bytes)


def get_trade_short(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    side = getattr(parameters, "Side Indicator")
    quantity = getattr(parameters, "Quantity")
    symbol = getattr(parameters, "Symbol")
    price = getattr(parameters, "Price")
    execution_id = getattr(parameters, "Execution Id")

    msg_bytes = TradeShort.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        side=side,
        quantity=quantity,
        symbol=symbol,
        price=price,
        execution_id=execution_id,
    ).get_bytes()

    return list(msg_bytes)


def get_trade_expanded(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    side = getattr(parameters, "Side Indicator")
    quantity = getattr(parameters, "Quantity")
    symbol = getattr(parameters, "Symbol")
    price = getattr(parameters, "Price")
    execution_id = getattr(parameters, "Execution Id")

    msg_bytes = TradeExpanded.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        side=side,
        quantity=quantity,
        symbol=symbol,
        price=price,
        execution_id=execution_id,
    ).get_bytes()

    return list(msg_bytes)


def get_order_executed(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    executed_quantity = getattr(parameters, "Executed Quantity")
    execution_id = getattr(parameters, "Execution Id")

    msg_bytes = OrderExecuted.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        executed_quantity=executed_quantity,
        execution_id=execution_id,
    ).get_bytes()

    return list(msg_bytes)


def get_order_executed_at_price_size(parameters) -> List[int]:
    time_offset = getattr(parameters, "Time Offset")
    order_id = getattr(parameters, "Order Id")
    executed_quantity = getattr(parameters, "Executed Quantity")
    remaining_quantity = getattr(parameters, "Remaining Quantity")
    execution_id = getattr(parameters, "Execution Id")
    price = getattr(parameters, "Price")

    msg_bytes = OrderExecutedAtPriceSize.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        executed_quantity=executed_quantity,
        remaining_quantity=remaining_quantity,
        execution_id=execution_id,
        price=price,
    ).get_bytes()
    return list(msg_bytes)
