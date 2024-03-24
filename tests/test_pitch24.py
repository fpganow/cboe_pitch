from unittest import TestCase
from hamcrest import assert_that, has_length, has_item, equal_to

from cboe_pitch.orderbook import OrderBook, Side
from cboe_pitch.pitch24 import FieldConverter

class TestFieldConverter(TestCase):
    def test_encode_orderid(self):
        # GIVEN
        order_id = "ORID0001"

        # WHEN
        encoded_oid = FieldConverter.orderid_to_u64(order_id)

        # THEN
        assert_that(encoded_oid, equal_to(0x313030304449524f))

    def test_encode_symbol(self):
        # GIVEN
        symbol = "AAPL"

        # WHEN
        encoded_symbol = FieldConverter.symbol_to_u64(symbol)

        # THEN
        print(f'encoded_symbol: {hex(encoded_symbol)}')
        assert_that(encoded_symbol, equal_to(0x4141504c20202020))
