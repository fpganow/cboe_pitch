import json
from typing import Dict, Any
from unittest import TestCase

from hamcrest import (
    assert_that,
    equal_to,
    greater_than,
    has_length,
    instance_of
)

from cboe_pitch import (
    get_seq_unit_hdr,
    get_time,
    get_add_order_long, get_add_order_short, get_add_order_expanded,
    get_order_executed, get_order_executed_at_price_size,
    get_reduce_size_long, get_reduce_size_short,
    get_modify_order_long, get_modify_order_short,
    get_delete_order,
    get_trade_long, get_trade_short, get_trade_expanded
)
from cboe_pitch.message_factory import MessageFactory

from cboe_pitch.time import Time
from cboe_pitch.add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from cboe_pitch.delete_order import DeleteOrder
from cboe_pitch.modify import ModifyOrderLong, ModifyOrderShort
from cboe_pitch.order_executed import OrderExecuted, OrderExecutedAtPriceSize
from cboe_pitch.reduce_size import ReduceSizeLong, ReduceSizeShort
from cboe_pitch.trade import TradeLong, TradeShort, TradeExpanded

#
# Message Types:
#
# SequencedUnitHeader
#
# [tested]  0x20  Time
#           0x97  UnitClear [not implemented]
#           0xBC  TransactionBegin [not implemented]
#           0xBD  TransactionEnd [not implemented]
# [tested]  0x21  AddOrderLong
# [tested]  0x22  AddOrderShort
# [tested]  0x2F  AddOrderExpanded
# [tested]  0x23  OrderExecuted
# [tested]  0x24  OrderExecutedAtPriceSize
# [tested]  0x25  ReduceSizeLong
# [tested]  0x26  ReduceSizeShort
# [tested]  0x27  ModifyOrderLong
# [tested]  0x28  ModifyOrderShort
# [tested]  0x29  DeleteOrder
# [tested]  0x2A  TradeLong
# [tested]  0x2B  TradeShort
# [tested]  0x30  TradeExpanded
#           0x2C  TradeBreak [not implemented]
#           0x2D  EndOfSession [not implemented]
#           0x31  TradingStatus [not implemented]

# Not Implemented
#  Gap Request Proxy Messages
#    - 0x01 Login
#    - 0x02 LoginResponse
#    - 0x03 GapRequest
#    - 0x04 GapResponse
#  Spin Messages
#    - 0x01 Login
#    - 0x02 LoginResponse
#    - 0x80 SpinImageAvailable
#    - 0x81 SpinRequest
#    - 0x82 SpinResponse
#    - 0x83 SpinFinished
#    - 0x84 InstrumentDefinitionRequest
#    - 0x85 InstrumentDefinitionResponse
#    - 0x86 InstrumentDefinitionFinished


def dump_bytes(msg_bytes):
    bytes_copy = msg_bytes.copy()
    slick = None
    while len(bytes_copy) > 0:
        slick = bytes_copy[0:8]
        line_str = ', '.join([f'{x:#04x}' for x in slick])
        print(f'\t{line_str}, ')
        bytes_copy = bytes_copy[8:]


class Parameters:
    @staticmethod
    def from_dictionary(args: Dict[str, Any]) -> "":
        parameters = ()
        for key, val in args.items():
            setattr(parameters, key, val)
        return parameters

    @staticmethod
    def to_json(args: Dict[str, Any]) -> str:
        return json.dumps(args)
#        res = '{\n'
#        for key, val in args.items():
#            val_str = f'{str(val)}'
#            res += f'"{key}" : ' + val_str
#        res += '}'
#        return res

class TestTime(TestCase):
    def test_timestamp_create(self):
        # GIVEN
        args = {
            # 34_200 seconds = 9:30 AM
            "Time": 34_300
        }

        # WHEN
        parameters = Parameters.to_json(args)
        msg_bytes = get_time(parameters)

        # THEN
        assert_that(msg_bytes, has_length(6))
        assert_that(msg_bytes, equal_to([
            0x06, 0x20, 0xfc, 0x85, 0x00, 0x00
            ]))

        new_time_msg = MessageFactory.from_list(msg_bytes)
        assert_that(new_time_msg, instance_of(Time))

        assert_that(new_time_msg.time(), equal_to(34_300))


class TestAddOrder(TestCase):
    def test_add_order_long_create(self):
        # GIVEN
        args = {
            "Time Offset": 44_000,
            "Order Id": "ORID0001",
            "Side Indicator": "B",
            "Quantity": 95_000,
            "Symbol": "AAPL",
            "Price": 0.905,
        }

        # WHEN
        msg_bytes = get_add_order_long(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(34))
        assert_that(msg_bytes, equal_to([
            0x22, 0x21, 0xe0, 0xab,  0x0,  0x0, 0x4f, 0x52, 
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x42, 0x18,
            0x73,  0x1,  0x0, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0x5a, 0x23,  0x0,  0x0,  0x0,  0x0,  0x0, 
            0x0, 0x1]))

        new_addorder_long = MessageFactory.from_list(msg_bytes)

        assert_that(new_addorder_long, instance_of(AddOrderLong))
        assert_that(new_addorder_long.time_offset(), equal_to(44_000))
        assert_that(new_addorder_long.order_id(), equal_to("ORID0001"))
        assert_that(new_addorder_long.side(), equal_to("B"))
        assert_that(new_addorder_long.quantity(), equal_to(95_000))
        assert_that(new_addorder_long.symbol(), equal_to("AAPL"))
        assert_that(new_addorder_long.price(), equal_to(0.905))


    def test_add_order_short_create(self):
        # GIVEN
        args = {
            "Time Offset": 44_000,
            "Order Id": "ORID0001",
            "Side Indicator": "B",
            "Quantity": 25_000,
            "Symbol": "AAPL",
            "Price": 0.95,
        }

        # WHEN
        msg_bytes = get_add_order_short(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(26))
        assert_that(msg_bytes, equal_to([
            0x1a, 0x22, 0xe0, 0xab,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x42, 0xa8,
            0x61, 0x41, 0x41, 0x50, 0x4c, 0x20, 0x20, 0x5f,
            0x0, 0x1
            ]))
        new_addorder_short = MessageFactory.from_list(msg_bytes)

        assert_that(new_addorder_short, instance_of(AddOrderShort))
        assert_that(new_addorder_short.time_offset(), equal_to(44_000))
        assert_that(new_addorder_short.order_id(), equal_to("ORID0001"))
        assert_that(new_addorder_short.side(), equal_to("B"))
        assert_that(new_addorder_short.quantity(), equal_to(25_000))
        assert_that(new_addorder_short.symbol(), equal_to("AAPL"))
        assert_that(new_addorder_short.price(), equal_to(0.95))


    def test_add_order_expanded_create(self):
        # GIVEN
        args = {
            "Time Offset": 44_000,
            "Order Id": "ORID0001",
            "Side Indicator": "B",
            "Quantity": 25_000,
            "Symbol": "AAPL",
            "Price": 0.905,
            "Customer Indicator": "C",
            "Participant Id": "MPID"
        }

        # WHEN
        msg_bytes = get_add_order_expanded(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(41))
        assert_that(msg_bytes, equal_to([
            0x29, 0x2f, 0xe0, 0xab,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x31, 0x42, 0xa8,
            0x61,  0x0,  0x0, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0x20, 0x20, 0x5a, 0x23,  0x0,  0x0,  0x0,
             0x0,  0x0,  0x0,  0x1, 0x4d, 0x50, 0x49, 0x44,
            0x43
            ]))

        new_addorder_expanded = MessageFactory.from_list(msg_bytes)

        assert_that(new_addorder_expanded, instance_of(AddOrderExpanded))
        assert_that(new_addorder_expanded.time_offset(), equal_to(44_000))
        assert_that(new_addorder_expanded.order_id(), equal_to("ORID0001"))
        assert_that(new_addorder_expanded.side(), equal_to("B"))
        assert_that(new_addorder_expanded.quantity(), equal_to(25_000))
        assert_that(new_addorder_expanded.symbol(), equal_to("AAPL"))
        assert_that(new_addorder_expanded.price(), equal_to(0.905))

class TestOrderExecuted(TestCase):
    def test_order_executed_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Executed Quantity": 25_000,
            "Execution Id": "EXID0001",
        }

        # WHEN
        msg_bytes = get_order_executed(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(26))
        assert_that(msg_bytes, equal_to([
            0x1a, 0x23, 0xd0, 0x84,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0xa8, 0x61,
             0x0,  0x0, 0x45, 0x58, 0x49, 0x44,  0x30,  0x30,
            0x30, 0x31
            ]))
        new_orderexecuted_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_orderexecuted_msg, instance_of(OrderExecuted))
        assert_that(new_orderexecuted_msg.time_offset(), equal_to(34_000))
        assert_that(new_orderexecuted_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_orderexecuted_msg.executed_quantity(), equal_to(25_000))
        assert_that(new_orderexecuted_msg.execution_id(), equal_to("EXID0001"))

    def test_order_executed_at_price_size_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Executed Quantity": 25_000,
            "Remaining Quantity": 20_000,
            "Execution Id": "EXEI0001",
            "Price": 0.905,
        }

        # WHEN
        msg_bytes = get_order_executed_at_price_size(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(38))
        assert_that(msg_bytes, equal_to([
            0x26, 0x24, 0xd0, 0x84,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0xa8, 0x61,
             0x0,  0x0, 0x20, 0x4e,  0x0,  0x0, 0x45, 0x58,
            0x45, 0x49, 0x30, 0x30, 0x30, 0x31, 0x5a, 0x23,
             0x0,  0x0,  0x0,  0x0,  0x0,  0x0
            ]))
        new_orderexecuted_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_orderexecuted_msg, instance_of(OrderExecutedAtPriceSize))
        assert_that(new_orderexecuted_msg.time_offset(), equal_to(34_000))
        assert_that(new_orderexecuted_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_orderexecuted_msg.executed_quantity(), equal_to(25_000))
        assert_that(new_orderexecuted_msg.remaining_quantity(), equal_to(20_000))
        assert_that(new_orderexecuted_msg.execution_id(), equal_to("EXEI0001"))
        assert_that(new_orderexecuted_msg.price(), equal_to(0.905))


class TestReduceSize(TestCase):
    def test_reduce_size_long_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Canceled Quantity": 25_000,
        }

        # WHEN
        msg_bytes = get_reduce_size_long(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(18))
        assert_that(msg_bytes, equal_to([
            0x12, 0x25, 0xd0, 0x84,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0xa8, 0x61,
             0x0,  0x0
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(ReduceSizeLong))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_msg.canceled_quantity(), equal_to(25_000))


    def test_reduce_size_short_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0003",
            "Canceled Quantity": 25_000,
        }

        # WHEN
        msg_bytes = get_reduce_size_short(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(16))
        assert_that(msg_bytes, equal_to([
            0x10, 0x26, 0xd0, 0x84,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x33, 0xa8, 0x61,
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(ReduceSizeShort))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0003"))
        assert_that(new_msg.canceled_quantity(), equal_to(25_000))


class TestModifyOrder(TestCase):
    def test_modify_order_long_create(self):
        # GIVE
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Quantity": 25_000,
            "Price": 0.905,
        }

        # WHEN
        msg_bytes = get_modify_order_long(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(27))
        assert_that(msg_bytes, equal_to([
            0x1b, 0x27, 0xd0, 0x84, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0xa8, 0x61,
            0x00, 0x00, 0x5a, 0x23, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x01,
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(ModifyOrderLong))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_msg.quantity(), equal_to(25_000))
        assert_that(new_msg.price(), equal_to(0.905))


    def test_modify_order_short_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Quantity": 25_000,
            "Price": 0.99,
        }

        # WHEN
        msg_bytes = get_modify_order_short(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(19))
        assert_that(msg_bytes, equal_to([
            0x13, 0x28, 0xd0, 0x84, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0xa8, 0x61,
            0x63, 0x00, 0x01,
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(ModifyOrderShort))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_msg.quantity(), equal_to(25_000))
        assert_that(new_msg.price(), equal_to(0.99))


class TestDeleteOrder(TestCase):
    def test_delete_order_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
        }

        # WHEN
        msg_bytes = get_delete_order(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(14))
        assert_that(msg_bytes, equal_to([
            0x0e, 0x29, 0xd0, 0x84, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(DeleteOrder))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0002"))


class TestTrade(TestCase):
    def test_trade_long_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Side Indicator": "B",
            "Quantity": 20_000,
            "Symbol": "AAPL",
            "Price": 100.99,
            "Execution Id":"EXEID001"
        }

        # WHEN
        msg_bytes = get_trade_long(parameters=Parameters.to_json(args))

        # THEN
        dump_bytes(msg_bytes)
        assert_that(msg_bytes, has_length(41))
        assert_that(msg_bytes, equal_to([
            0x29, 0x2a, 0xd0, 0x84, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0x42, 0x20,
            0x4e, 0x00, 0x00, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0xec, 0x68, 0x0f, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x45, 0x58, 0x45, 0x49, 0x44, 0x30, 0x30,
            0x31,
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(TradeLong))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_msg.side(), equal_to("B"))
        assert_that(new_msg.quantity(), equal_to(20_000))
        assert_that(new_msg.symbol(), equal_to("AAPL"))
        assert_that(new_msg.price(), equal_to(100.99))
        assert_that(new_msg.execution_id(), equal_to("EXEID001"))


    def test_trade_short_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Side Indicator": "B",
            "Quantity": 20_000,
            "Symbol": "AAPL",
            "Price": 100.99,
            "Execution Id":"EXEID002"
        }

        # WHEN
        msg_bytes = get_trade_short(parameters=Parameters.to_json(args))

        # THEN
        dump_bytes(msg_bytes)
        assert_that(msg_bytes, has_length(33))
        assert_that(msg_bytes, equal_to([
            0x21, 0x2b, 0xd0, 0x84, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0x42, 0x20,
            0x4e, 0x41, 0x41, 0x50, 0x4c, 0x20, 0x20, 0x73,
            0x27, 0x45, 0x58, 0x45, 0x49, 0x44, 0x30, 0x30,
            0x32,
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(TradeShort))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_msg.side(), equal_to("B"))
        assert_that(new_msg.quantity(), equal_to(20_000))
        assert_that(new_msg.symbol(), equal_to("AAPL"))
        assert_that(new_msg.price(), equal_to(100.99))
        assert_that(new_msg.execution_id(), equal_to("EXEID002"))


    def test_trade_expanded_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID0002",
            "Side Indicator": "B",
            "Quantity": 20_000,
            "Symbol": "AAPL",
            "Price": 100.99,
            "Execution Id":"EXEID001"
        }

        # WHEN
        msg_bytes = get_trade_expanded(parameters=Parameters.to_json(args))

        # THEN
        dump_bytes(msg_bytes)
        assert_that(msg_bytes, has_length(43))
        assert_that(msg_bytes, equal_to([
            0x2b, 0x30, 0xd0, 0x84, 0x00, 0x00, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x30, 0x32, 0x42, 0x20,
            0x4e, 0x00, 0x00, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0x20, 0x20, 0xec, 0x68, 0x0f, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x45, 0x58, 0x45, 0x49, 0x44,
            0x30, 0x30, 0x31,
            ]))
        new_msg = MessageFactory.from_list(msg_bytes)

        assert_that(new_msg, instance_of(TradeExpanded))
        assert_that(new_msg.time_offset(), equal_to(34_000))
        assert_that(new_msg.order_id(), equal_to("ORID0002"))
        assert_that(new_msg.side(), equal_to("B"))
        assert_that(new_msg.quantity(), equal_to(20_000))
        assert_that(new_msg.symbol(), equal_to("AAPL"))
        assert_that(new_msg.price(), equal_to(100.99))
        assert_that(new_msg.execution_id(), equal_to("EXEID001"))


class TestSequencedUnitHeader(TestCase):
    def test_seq_unit_hdr_w_time_msg(self):
        # GIVEN
        # These functions are intended to be called from
        # SystemVerilog via DPI
        time_msg_arr = get_time(Parameters.to_json({"Time": 34_201}))

        assert_that(time_msg_arr, has_length(6))
        assert_that(time_msg_arr, equal_to([0x6, 0x20, 0x99, 0x85, 0, 0]))

        final_array = get_seq_unit_hdr(parameters=
                Parameters.to_json({
                                    "HdrSeq": 15,
                                    "HdrCount": 0
                                   }),
                                   msgs_array=time_msg_arr)


#        print(f'time_msg_arr: {[hex(x) for x in time_msg_arr]}')
#        print(f'final_array: {[hex(x) for x in final_array]}')
        assert_that(final_array, equal_to([
            0xE, 0x00, 0x1, 0x1, 0x0F, 0x0, 0x0, 0x0, # Seq Unit Hdr
            0x6,  0x20, 0x99, 0x85, 0, 0 # Time
            ]))

    def test_seq_unit_hdr_w_time_n_add_order(self):
        # GIVEN
        final_arr = list()
        final_arr
        pass
        #full_msg_array = None
        #full_msg_array.extend(new_time_msg)
        #full_msg_array.extend(new_add_order_msg)
