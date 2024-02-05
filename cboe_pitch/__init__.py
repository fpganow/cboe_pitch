#
# https://www.cboe.com/us/equities/support/technical/
#

import json
from typing import List

from .delete_order import DeleteOrder
from .modify import ModifyOrderLong, ModifyOrderShort
from .time import Time
from .add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from .order_executed import OrderExecuted, OrderExecutedAtPriceSize
from .reduce_size import ReduceSizeLong, ReduceSizeShort
from .seq_unit_header import SequencedUnitHeader

#
# LabVIEW Interface
#
# The following functions are meant to be called from LabVIEW by
# using the Python Connectivity Palette
#
from .trade import TradeLong, TradeShort, TradeExpanded


def get_seq_unit_hdr(parameters, msgs_array: List[int]) -> List[int]:
    json_dict = json.loads(parameters)

    HdrSeq = json_dict["HdrSeq"]
    HdrCount = json_dict["HdrCount"]
    return list(
        SequencedUnitHeader.from_message_array(
            msgs_array=msgs_array, hdr_count=HdrCount, hdr_sequence=HdrSeq
        )
    )


def get_time(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    seconds_since_midnight = json_dict["Time"]
    return list(Time.from_parms(time=seconds_since_midnight).get_bytes())


def get_add_order_long(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    side = json_dict["Side Indicator"]
    quantity = json_dict["Quantity"]
    symbol = json_dict["Symbol"]
    price = json_dict["Price"]
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
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    side = json_dict["Side Indicator"]
    quantity = json_dict["Quantity"]
    symbol = json_dict["Symbol"]
    price = json_dict["Price"]
    msg_bytes = AddOrderShort.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        side=side,
        quantity=quantity,
        symbol=symbol,
        price=price,
    ).get_bytes()
    return list(msg_bytes)


def get_add_order_expanded(parameters: str) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    side = json_dict["Side Indicator"]
    quantity = json_dict["Quantity"]
    symbol = json_dict["Symbol"]
    price = json_dict["Price"]
    participant_id = json_dict["Participant Id"]
    customer_indicator = json_dict["Customer Indicator"]

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
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    executed_quantity = json_dict["Executed Quantity"]
    execution_id = json_dict["Execution Id"]

    msg_bytes = OrderExecuted.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        executed_quantity=executed_quantity,
        execution_id=execution_id,
    ).get_bytes()

    return list(msg_bytes)


def get_order_executed_at_price_size(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    executed_quantity = json_dict["Executed Quantity"]
    remaining_quantity = json_dict["Remaining Quantity"]
    execution_id = json_dict["Execution Id"]
    price = json_dict["Price"]

    msg_bytes = OrderExecutedAtPriceSize.from_parms(
        time_offset=time_offset,
        order_id=order_id,
        executed_quantity=executed_quantity,
        remaining_quantity=remaining_quantity,
        execution_id=execution_id,
        price=price,
    ).get_bytes()
    return list(msg_bytes)


def get_reduce_size_long(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    canceled_quantity = json_dict["Canceled Quantity"]

    msg_bytes = ReduceSizeLong.from_parms(
        time_offset=time_offset, order_id=order_id, canceled_quantity=canceled_quantity
    ).get_bytes()

    return list(msg_bytes)


def get_reduce_size_short(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    canceled_quantity = json_dict["Canceled Quantity"]

    msg_bytes = ReduceSizeShort.from_parms(
        time_offset=time_offset, order_id=order_id, canceled_quantity=canceled_quantity
    ).get_bytes()

    return list(msg_bytes)


def get_modify_order_long(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    quantity = json_dict["Quantity"]
    price = json_dict["Price"]

    msg_bytes = ModifyOrderLong.from_parms(
        time_offset=time_offset, order_id=order_id, quantity=quantity, price=price
    ).get_bytes()

    return list(msg_bytes)


def get_modify_order_short(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    quantity = json_dict["Quantity"]
    price = json_dict["Price"]

    msg_bytes = ModifyOrderShort.from_parms(
        time_offset=time_offset, order_id=order_id, quantity=quantity, price=price
    ).get_bytes()

    return list(msg_bytes)


def get_delete_order(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]

    msg_bytes = DeleteOrder.from_parms(
        time_offset=time_offset, order_id=order_id
    ).get_bytes()

    return list(msg_bytes)


def get_trade_long(parameters) -> List[int]:
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    side = json_dict["Side Indicator"]
    quantity = json_dict["Quantity"]
    symbol = json_dict["Symbol"]
    price = json_dict["Price"]
    execution_id = json_dict["Execution Id"]

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
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    side = json_dict["Side Indicator"]
    quantity = json_dict["Quantity"]
    symbol = json_dict["Symbol"]
    price = json_dict["Price"]
    execution_id = json_dict["Execution Id"]

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
    json_dict = json.loads(parameters)

    time_offset = json_dict["Time Offset"]
    order_id = json_dict["Order Id"]
    side = json_dict["Side Indicator"]
    quantity = json_dict["Quantity"]
    symbol = json_dict["Symbol"]
    price = json_dict["Price"]
    execution_id = json_dict["Execution Id"]

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
