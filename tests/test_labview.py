from typing import Dict, Any
from unittest import TestCase

from hamcrest import assert_that, has_length, greater_than

from pitch import get_time, get_add_order_long, get_order_executed


class Parameters:

    @staticmethod
    def from_dictionary(args: Dict[str, Any]) -> 'Parameters':
        parameters = Parameters()
        for key, val in args.items():
            setattr(parameters, key, val)
        return parameters


class TestTime(TestCase):
    def test_timestamp_create(self):
        # GIVEN
        args = {
            # 34_200 seconds = 9:30 AM
            'Seconds Since Midnight': 34_200
        }
        parameters = Parameters.from_dictionary(args)
        msg_bytes = get_time(parameters)

        assert_that(msg_bytes, has_length(greater_than(0)))

    def test_add_order_long_create(self):
        # GIVEN
        args = {
            'Time Offset': 44_000,
            'Order Id': 'ORID001',
            'Side Indicator': 'B',
            'Quantity': 95_000,
            'Symbol': 'AAPL',
            'Price': 0.905
        }

        # WHEN
        parameters = Parameters.from_dictionary(args)
        msg_bytes = get_add_order_long(parameters)

        # THEN
        assert_that(msg_bytes, has_length(greater_than(0)))

    def test_order_executed_create(self):
        # GIVEN
        args = {
            'Time Offset': 34_000,
            'Order Id': 'ORID002',
            'Executed Quantity': 25_000,
            'Execution Id': 'TSLA',
        }

        # WHEN
        parameters = Parameters.from_dictionary(args)
        msg_bytes = get_order_executed(parameters)

        # THEN
        assert_that(msg_bytes, has_length(greater_than(0)))
