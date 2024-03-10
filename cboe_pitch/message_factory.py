from typing import ByteString, List, Union

from .time import Time
from .add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from .delete_order import DeleteOrder
from .modify import ModifyOrderLong, ModifyOrderShort
from .order_executed import OrderExecuted, OrderExecutedAtPriceSize
from .reduce_size import ReduceSizeLong, ReduceSizeShort
from .modify import ModifyOrderLong, ModifyOrderShort
from .delete_order import DeleteOrder
from .trade import TradeLong, TradeShort, TradeExpanded

class MessageFactory:
    @staticmethod
    def from_list(
        msg_bytes: List[int],
    ) -> Union[Time, AddOrderLong, AddOrderShort, AddOrderExpanded]:
        return MessageFactory.from_bytes(bytearray(msg_bytes))

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

        elif msg_bytes[1] == ModifyOrderLong._messageType:
            message = ModifyOrderLong()
        elif msg_bytes[1] == ModifyOrderShort._messageType:
            message = ModifyOrderShort()

        elif msg_bytes[1] == DeleteOrder._messageType:
            message = DeleteOrder()

        elif msg_bytes[1] == TradeLong._messageType:
            message = TradeLong()
        elif msg_bytes[1] == TradeShort._messageType:
            message = TradeShort()
        elif msg_bytes[1] == TradeExpanded._messageType:
            message = TradeExpanded()

        if message is None:
            raise Exception("Unknown type")
        message.from_bytes(msg_bytes)
        return message
