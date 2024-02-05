from typing import ByteString, Union

from .time import Time
from .add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from .order_executed import OrderExecuted, OrderExecutedAtPriceSize
from .reduce_size import ReduceSizeLong, ReduceSizeShort


class MessageFactory:
    @staticmethod
    def from_bytes(
        msg_bytes: ByteString,
    ) -> Union[Time, AddOrderLong, AddOrderShort, AddOrderExpanded]:
        message = None
        if msg_bytes[1] == Time._messageType:
            message = Time()
        elif msg_bytes[1] == AddOrderLong._messageType:
            message = AddOrderLong()
        elif msg_bytes[1] == AddOrderShort._messageType:
            message = AddOrderShort()
        elif msg_bytes[1] == AddOrderExpanded._messageType:
            message = AddOrderExpanded()
        elif msg_bytes[1] == OrderExecuted._messageType:
            message = OrderExecuted()
        elif msg_bytes[1] == OrderExecutedAtPriceSize._messageType:
            message = OrderExecutedAtPriceSize()
        elif msg_bytes[1] == ReduceSizeLong._messageType:
            message = ReduceSizeLong()
        elif msg_bytes[1] == ReduceSizeShort._messageType:
            message = ReduceSizeShort()
        if message is None:
            raise Exception("Unknown type")
        message.from_bytes(msg_bytes)
        return message
