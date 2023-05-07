from unittest import TestCase

from hamcrest import assert_that, has_length, is_

from pitch.trade import TradeLong, TradeShort, TradeExpanded
from tests.comparator import compare_bytes


class TestTrade(TestCase):
    def test_trade_long(self):
        # GIVEN
        message = TradeLong.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            side="B",
            quantity=20_000,
            symbol="AAPL",
            price=100.99,
            execution_id="EXEID001",
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(41))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            41,  # Length
                            0x2A,  # Message Type
                            0x18,
                            0xD2,
                            6,
                            0,  # Time offset
                            0x4F,
                            0x52,
                            0x49,
                            0x44,
                            0x30,
                            0x30,
                            0x30,
                            0x31,  # Order Id
                            0x42,  # Side Indicator
                            0x20,
                            0x4E,
                            0x0,
                            0x0,  # Quantity
                            0x41,
                            0x41,
                            0x50,
                            0x4C,
                            0x20,
                            0x20,  # Symbol
                            0xEC,
                            0x68,
                            0xF,
                            0,
                            0,
                            0,
                            0,
                            0,  # Price
                            0x45,
                            0x58,
                            0x45,
                            0x49,
                            0x44,
                            0x30,
                            0x30,
                            0x31,  # Execution Id
                        ]
                    )
                )
            ),
        )

    def test_trade_short(self):
        # GIVEN
        message = TradeShort.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            side="B",
            quantity=20_000,
            symbol="AAPL",
            price=100.99,
            execution_id="EXE10012",
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(33))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            33,  # Length
                            0x2B,  # Message Type
                            0x18,
                            0xD2,
                            6,
                            0,  # Time offset
                            0x4F,
                            0x52,
                            0x49,
                            0x44,
                            0x30,
                            0x30,
                            0x30,
                            0x31,  # Order Id
                            0x42,  # Side Indicator
                            0x20,
                            0x4E,  # Quantity
                            0x41,
                            0x41,
                            0x50,
                            0x4C,
                            0x20,
                            0x20,  # Symbol
                            0x73,
                            0x27,  # Price
                            0x45,
                            0x58,
                            0x45,
                            0x31,
                            0x30,
                            0x30,
                            0x31,
                            0x32,  # Execution Id
                        ]
                    )
                )
            ),
        )

    def test_trade_expanded(self):
        # GIVEN
        message = TradeExpanded.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            side="B",
            quantity=20_000,
            symbol="AAPL",
            price=100.99,
            execution_id="EXEID001",
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(43))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            43,  # Length
                            0x30,  # Message Type
                            0x18,
                            0xD2,
                            6,
                            0,  # Time offset
                            0x4F,
                            0x52,
                            0x49,
                            0x44,
                            0x30,
                            0x30,
                            0x30,
                            0x31,  # Order Id
                            0x42,  # Side Indicator
                            0x20,
                            0x4E,
                            0x0,
                            0x0,  # Quantity
                            0x41,
                            0x41,
                            0x50,
                            0x4C,
                            0x20,
                            0x20,
                            0x20,
                            0x20,  # Symbol
                            0xEC,
                            0x68,
                            0xF,
                            0,
                            0,
                            0,
                            0,
                            0,  # Price
                            0x45,
                            0x58,
                            0x45,
                            0x49,
                            0x44,
                            0x30,
                            0x30,
                            0x31,  # Execution Id
                        ]
                    )
                )
            ),
        )
