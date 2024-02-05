import json
from typing import Dict, Any
from unittest import TestCase

from hamcrest import assert_that, equal_to, has_length, greater_than

from cboe_pitch import (
    get_time,
    get_add_order_long, get_add_order_short, get_add_order_expanded,
    get_order_executed, get_order_executed_at_price_size,
    get_seq_unit_hdr
)

# TODO: Implement all of the remaining message types
# Available methods:
# SequencedUnitHeader
# [tested]  0x20  Time
#           0x97  UnitClear [not implemented]
#           0xBC  TransactionBegin [not implemented]
#           0xBD  TransactionEnd [not implemented]
# [tested]  0x21  AddOrderLong
# [tested]  0x22  AddOrderShort
# [tested]  0x2F  AddOrderExpanded
# [tested]  0x23  OrderExecuted
# [tested]  0x24  OrderExecutedAtPriceSize
# 0x25 ReduceSizeLong
# 0x26 ReduceSizeShort
# 0x27 ModifyOrderLong
# 0x28 ModifyOrderShort
# 0x29 DeleteOrder
# 0x2A TradeLong
# 0x2B TradeShort
# 0x30 TradeExpanded
# 0x2C TradeBreak [not implemented]
# 0x2D EndOfSession [not implemented]
# 0x31 TradingStatus [not implemented]

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
            "Time": 34_200
        }
        parameters = Parameters.to_json(args)
        msg_bytes = get_time(parameters)

        assert_that(msg_bytes, has_length(6))
        assert_that(msg_bytes, equal_to([0x06, 0x20, 0x98, 0x85, 0x00, 0x00]))


class TestAddOrder(TestCase):
    def test_add_order_long_create(self):
        # GIVEN
        args = {
            "Time Offset": 44_000,
            "Order Id": "ORID001",
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
            0x49, 0x44, 0x30, 0x30, 0x31,  0x0, 0x42, 0x18,
            0x73,  0x1,  0x0, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0x5a, 0x23,  0x0,  0x0,  0x0,  0x0,  0x0, 
            0x0, 0x1]))


    def test_add_order_short_create(self):
        # GIVEN
        args = {
            "Time Offset": 44_000,
            "Order Id": "ORID001",
            "Side Indicator": "B",
            "Quantity": 25_000,
            "Symbol": "AAPL",
            "Price": 0.905,
        }

        # WHEN
        msg_bytes = get_add_order_short(parameters=Parameters.to_json(args))

        # THEN
        assert_that(msg_bytes, has_length(26))
        assert_that(msg_bytes, equal_to([
            0x1a, 0x22, 0xe0, 0xab, 0x0, 0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x31, 0x0, 0x42, 0xa8,
            0x61, 0x41, 0x41, 0x50, 0x4c, 0x20, 0x20, 0x5a,
            0x0, 0x1
            ]))


    def test_add_order_expanded_create(self):
        # GIVEN
        args = {
            "Time Offset": 44_000,
            "Order Id": "ORID001",
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
            0x49, 0x44, 0x30, 0x30, 0x31,  0x0, 0x42, 0xa8,
            0x61,  0x0,  0x0, 0x41, 0x41, 0x50, 0x4c, 0x20,
            0x20, 0x20, 0x20, 0x5a, 0x23,  0x0,  0x0,  0x0,
             0x0,  0x0,  0x0,  0x1, 0x4d, 0x50, 0x49, 0x44,
            0x43
            ]))


class TestOrderExecuted(TestCase):
    def test_order_executed_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID002",
            "Executed Quantity": 25_000,
            "Execution Id": "TSLA",
        }

        # WHEN
        msg_bytes = get_order_executed(parameters=Parameters.to_json(args))

        # THEN
        print(f'msg_bytes: {[hex(x) for x in msg_bytes]}')
        assert_that(msg_bytes, has_length(26))
        assert_that(msg_bytes, equal_to([
            0x1a, 0x23, 0xd0, 0x84,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x32,  0x0, 0xa8, 0x61,
             0x0,  0x0, 0x54, 0x53, 0x4c, 0x41,  0x0,  0x0,
             0x0,  0x0
            ]))

    def test_order_executed_at_price_size_create(self):
        # GIVEN
        args = {
            "Time Offset": 34_000,
            "Order Id": "ORID002",
            "Executed Quantity": 25_000,
            "Execution Id": "TSLA",
        }

        # WHEN
        msg_bytes = get_order_executed_at_price_size(parameters=Parameters.to_json(args))

        # THEN
        print(f'msg_bytes: {[hex(x) for x in msg_bytes]}')
        assert_that(msg_bytes, has_length(26))
        assert_that(msg_bytes, equal_to([
            0x1a, 0x23, 0xd0, 0x84,  0x0,  0x0, 0x4f, 0x52,
            0x49, 0x44, 0x30, 0x30, 0x32,  0x0, 0xa8, 0x61,
             0x0,  0x0, 0x54, 0x53, 0x4c, 0x41,  0x0,  0x0,
             0x0,  0x0
            ]))

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


        print(f'time_msg_arr: {[hex(x) for x in time_msg_arr]}')
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
