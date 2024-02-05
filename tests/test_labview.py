import json
from typing import Dict, Any
from unittest import TestCase

from hamcrest import assert_that, equal_to, has_length, greater_than

from cboe_pitch import get_time, get_add_order_long, get_order_executed, get_seq_unit_hdr


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

        assert_that(msg_bytes, has_length(greater_than(0)))


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
        assert_that(msg_bytes, has_length(greater_than(0)))


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
        assert_that(msg_bytes, has_length(greater_than(0)))

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
