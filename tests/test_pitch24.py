from unittest import TestCase
from hamcrest import assert_that, has_length, has_item, equal_to

from cboe_pitch.orderbook import OrderBook, Side
from cboe_pitch.pitch24 import FieldConverter

class TestFieldConverter(TestCase):
    def test_encode_orderid(self):
        # GIVEN
        orderid = "ORID0001"

        # WHEN
        encoded_oid = FieldConverter.orderid_to_u64(orderid)

        # THEN
        assert_that(encoded_oid, equal_to(0x313030304449524f))

    def test_decode_orderid(self):
        # GIVEN
        orderid_u64 = 0x313030304449524f

        # WHEN
        decoded_orderid = FieldConverter.u64_to_orderid(orderid_u64)

        # THEN
        assert_that(decoded_orderid, equal_to("ORID0001"))

    def test_encode_symbol(self):
        # GIVEN
        symbol = "AAPL"

        # WHEN
        encoded_symbol = FieldConverter.symbol_to_u64(symbol)

        # THEN
        assert_that(encoded_symbol, equal_to(0x4141504c20202020))

    def test_decode_symbol(self):
        # GIVEN
        symbol_u64 = 0x4141504c20202020

        # WHEN
        decoded_symbol = FieldConverter.u64_to_symbol(symbol_u64)

        # THEN
        assert_that(decoded_symbol, equal_to("AAPL"))
