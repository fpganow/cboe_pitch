from unittest import TestCase

from hamcrest import assert_that, has_length, is_, equal_to, instance_of

from pitch.message_factory import MessageFactory
from pitch.order_executed import OrderExecuted, OrderExecutedAtPriceSize
from tests.comparator import compare_bytes


class TestOrderExecuted(TestCase):
    def test_order_executed(self):
        # GIVEN
        message = OrderExecuted.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            executed_quantity=20_000,
            execution_id="EXEID001",
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
                            0x1A,  # Length
                            0x23,  # Type
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
                            0x20,
                            0x4E,
                            0,
                            0,  # Executed Quantity
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
        assert_that(message, instance_of(OrderExecuted))
        assert_that(message.length(), equal_to(26))
        assert_that(message.messageType(), equal_to(0x23))
        assert_that(message.time_offset(), equal_to(447_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.executed_quantity(), equal_to(20_000))
        assert_that(message.execution_id(), equal_to("EXEID001"))

    def test_order_executed_parse(self):
        # GIVEN
        msg_bytes = bytearray(
            [
                0x1A,  # Length
                0x23,  # Type
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
                0x20,
                0x4E,
                0,
                0,  # Executed Quantity
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

        # WHEN
        message = MessageFactory.from_bytes(msg_bytes)

        # THEN
        assert_that(message, instance_of(OrderExecuted))
        assert_that(message.length(), equal_to(26))
        assert_that(message.messageType(), equal_to(0x23))
        assert_that(message.time_offset(), equal_to(447_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.executed_quantity(), equal_to(20_000))
        assert_that(message.execution_id(), equal_to("EXEID001"))

    def test_order_executed_at_price_size(self):
        # GIVEN
        message = OrderExecutedAtPriceSize.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            executed_quantity=20_000,
            execution_id="EXEID001",
            price=0.9050,
            remaining_quantity=200,
        )
        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(38))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            0x26,  # Length
                            0x24,  # Message Type
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
                            0x20,
                            0x4E,
                            0,
                            0,  # Executed Quantity
                            0xC8,
                            0,
                            0,
                            0,  # Remaining Quantity
                            0x45,
                            0x58,
                            0x45,
                            0x49,
                            0x44,
                            0x30,
                            0x30,
                            0x31,  # Execution Id
                            0x5A,
                            0x23,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0,  # Price
                        ]
                    )
                )
            ),
        )
        assert_that(message, instance_of(OrderExecutedAtPriceSize))
        assert_that(message.length(), equal_to(38))
        assert_that(message.messageType(), equal_to(0x24))
        assert_that(message.time_offset(), equal_to(447_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.executed_quantity(), equal_to(20_000))
        assert_that(message.execution_id(), equal_to("EXEID001"))
        assert_that(message.remaining_quantity(), equal_to(200))
        assert_that(message.price(), equal_to(0.9050))

    def test_order_executed_at_price_size_parse(self):
        # GIVEN
        msg_bytes = bytearray(
            [
                0x26,  # Length
                0x24,  # Message Type
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
                0x20,
                0x4E,
                0,
                0,  # Executed Quantity
                0xC8,
                0,
                0,
                0,  # Remaining Quantity
                0x45,
                0x58,
                0x45,
                0x49,
                0x44,
                0x30,
                0x30,
                0x31,  # Execution Id
                0x5A,
                0x23,
                0,
                0,
                0,
                0,
                0,
                0,  # Price
            ]
        )

        # WHEN
        message = MessageFactory.from_bytes(msg_bytes)

        # THEN
        assert_that(message, instance_of(OrderExecutedAtPriceSize))
        assert_that(message.length(), equal_to(38))
        assert_that(message.messageType(), equal_to(0x24))
        assert_that(message.time_offset(), equal_to(447_000))
        assert_that(message.order_id(), equal_to("ORID0001"))
        assert_that(message.executed_quantity(), equal_to(20_000))
        assert_that(message.execution_id(), equal_to("EXEID001"))
