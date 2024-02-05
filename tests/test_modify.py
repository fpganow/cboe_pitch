from unittest import TestCase

from hamcrest import assert_that, has_length, is_

from cboe_pitch.modify import ModifyOrderLong, ModifyOrderShort
from tests.comparator import compare_bytes


class TestModify(TestCase):
    def test_modify_long(self):
        # GIVEN
        message = ModifyOrderLong.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            quantity=20_000,
            price=100.99,
            displayed=True,
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(27))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            27,  # Length
                            0x27,  # Message Type
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
                            0x0,
                            0x0,  # Quantity
                            0xEC,
                            0x68,
                            0xF,
                            0,
                            0,
                            0,
                            0,
                            0,  # Price
                            0x1,  # Modify Flags
                        ]
                    )
                )
            ),
        )

    def test_modify_short(self):
        # GIVEN
        message = ModifyOrderShort.from_parms(
            time_offset=447_000,
            order_id="ORID0001",
            quantity=20_000,
            price=100.99,
            displayed=True,
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(19))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            19,  # Length
                            0x28,  # Message Type
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
                            0x4E,  # Quantity
                            0x73,
                            0x27,  # Price
                            0x1,  # Modify Flags
                        ]
                    )
                )
            ),
        )
