from unittest import TestCase

from hamcrest import assert_that, has_length, is_, equal_to, instance_of

from pitch.add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from pitch.message_factory import MessageFactory
from tests.comparator import compare_bytes


class TestAddOrder(TestCase):
    def test_add_order_long(self):
        # GIVEN
        message = AddOrderLong.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            side="B",
            quantity=20_000,
            symbol="AAPL",
            price=0.9050,
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(34))

        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            0x22,  # Length
                            0x21,  # Type
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
                            0,
                            0,  # Quantity
                            0x41,
                            0x41,
                            0x50,
                            0x4C,
                            0x20,
                            0x20,  # Symbol
                            0x5A,
                            0x23,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,  # Price
                            0x01,  # AddFlags
                        ]
                    )
                )
            ),
        )
        assert_that(message.length(), equal_to(34))
        assert_that(message.messageType(), equal_to(0x21))
        assert_that(message.time_offset(), equal_to(447_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.side(), equal_to("B"))
        assert_that(message.quantity(), equal_to(20_000))
        assert_that(message.symbol(), equal_to("AAPL"))
        assert_that(message.price(), equal_to(0.9050))
        assert_that(message.displayed(), equal_to(True))

    def test_add_order_short(self):
        # GIVEN
        message = AddOrderShort.from_parms(
            time_offset=27_000,
            order_id="ORID0001",
            side="B",
            quantity=20_000,
            symbol="AAPL",
            price=90.50,
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(26))

        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            26,  # Length
                            0x22,  # Type
                            0x78,
                            0x69,
                            0,
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
                            0x5A,  # Price
                            0x23,  # Price
                            0x01,  # AddBitField
                        ]
                    )
                )
            ),
        )
        assert_that(message.length(), equal_to(26))
        assert_that(message.messageType(), equal_to(0x22))
        assert_that(message.time_offset(), equal_to(27_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.side(), equal_to("B"))
        assert_that(message.quantity(), equal_to(20_000))
        assert_that(message.symbol(), equal_to("AAPL"))
        assert_that(message.price(), equal_to(90.50))
        assert_that(message.displayed(), equal_to(True))

    def test_add_order_expanded(self):
        # GIVEN
        message = AddOrderExpanded.from_parms(
            time_offset=99_000,
            order_id="ORID0991",
            side="S",
            quantity=20_000,
            symbol="AAPL",
            price=0.9050,
            displayed=True,
            participant_id="MPID",
            customer_indicator="C",
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
                            0x2F,  # Type
                            0xB8,
                            0x82,
                            1,
                            0,  # Time offset
                            0x4F,
                            0x52,
                            0x49,
                            0x44,
                            0x30,
                            0x39,
                            0x39,
                            0x31,  # Order Id
                            0x53,  # Side Indicator
                            0x20,
                            0x4E,
                            0,
                            0,  # Quantity
                            0x41,
                            0x41,
                            0x50,
                            0x4C,
                            0x20,
                            0x20,
                            0x20,
                            0x20,  # Symbol
                            0x5A,
                            0x23,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,  # Price
                            0x01,  # AddFlags
                            0x4D,
                            0x50,
                            0x49,
                            0x44,  # ParticipantId
                            0x43,  # Customer Indicator
                        ]
                    )
                )
            ),
        )
        assert_that(message, instance_of(AddOrderExpanded))
        assert_that(message.length(), equal_to(41))
        assert_that(message.messageType(), equal_to(0x2F))
        assert_that(message.time_offset(), equal_to(99_000))
        assert_that(message.order_id(), equal_to("ORID0991"))
        assert_that(message.side(), equal_to("S"))
        assert_that(message.quantity(), equal_to(20_000))
        assert_that(message.symbol(), equal_to("AAPL"))
        assert_that(message.price(), equal_to(0.9050))
        assert_that(message.displayed(), equal_to(True))
        assert_that(message.participant_id(), equal_to("MPID"))
        assert_that(message.customer_indicator(), equal_to("C"))

    def test_add_order_long_parse(self):
        # GIVEN
        msg_bytes = bytearray(
            [
                0x22,  # Length
                0x21,  # Type
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
                0,
                0,  # Quantity
                0x41,
                0x20,
                0x20,
                0x20,
                0x20,
                0x20,  # Symbol
                0x5A,
                0x23,
                0,
                0,
                0,
                0,
                0,
                0,  # Price
                0x01,  # AddBitField
            ]
        )

        # WHEN
        message = MessageFactory.from_bytes(msg_bytes)

        # THEN
        assert_that(message, instance_of(AddOrderLong))
        assert_that(message.length(), equal_to(34))
        assert_that(message.messageType(), equal_to(0x21))
        assert_that(message.time_offset(), equal_to(447_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.side(), equal_to("B"))
        assert_that(message.quantity(), equal_to(20_000))
        assert_that(message.symbol(), equal_to("A"))
        assert_that(message.price(), equal_to(0.9050))
        assert_that(message.displayed(), equal_to(True))

    def test_add_order_short_parse(self):
        # GIVEN
        msg_bytes = bytearray(
            [
                26,  # Length
                0x22,  # Type
                0x08,
                0xEA,
                1,
                0,  # Time offset
                0x4F,
                0x52,
                0x49,
                0x44,
                0x30,
                0x30,
                0x30,
                0x32,  # Order Id
                0x42,  # Side Indicator
                0x20,
                0x4E,  # Quantity
                0x41,  # Symbol
                0x41,
                0x50,
                0x4C,
                0x20,
                0x20,  # Symbol
                0x5A,  # Price
                0x23,  # Price
                0x01,  # AddBitField
            ]
        )

        # WHEN
        message = MessageFactory.from_bytes(msg_bytes)

        # THEN
        assert_that(message, instance_of(AddOrderShort))
        assert_that(message.time_offset(), equal_to(125_448))
        assert_that(message.order_id(), equal_to("ORID0002"))
        assert_that(message.side(), equal_to("B"))
        assert_that(message.symbol(), equal_to("AAPL"))
        assert_that(
            message.price(), equal_to(90.50)
        )  # Binary Short Price (2 implied decimal places)
        assert_that(message.displayed(), equal_to(True))

    def test_add_order_expanded_parse(self):
        # GIVEN
        msg_bytes = bytearray(
            [
                41,  # Length
                0x2F,  # Type
                0x00,
                0xD6,
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
                0,
                0,  # Quantity
                0x41,
                0x41,
                0x50,
                0x4C,
                0x20,
                0x20,
                0x20,
                0x20,  # Symbol
                0x5A,
                0x23,
                0,
                0,
                0,
                0,
                0,
                0,  # Price
                0x01,  # AddFlags
                0x4D,
                0x50,
                0x49,
                0x44,  # ParticipantId
                0x43,  # Customer Indicator
            ]
        )

        # WHEN
        message = MessageFactory.from_bytes(msg_bytes)

        # THEN
        assert_that(message, instance_of(AddOrderExpanded))
        assert_that(message.time_offset(), equal_to(448_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.side(), equal_to("B"))
        assert_that(message.symbol(), equal_to("AAPL"))
        assert_that(message.price(), equal_to(0.9050))
        assert_that(message.displayed(), equal_to(True))

        assert_that(message.participant_id(), equal_to("MPID"))
        assert_that(message.customer_indicator(), equal_to("C"))
