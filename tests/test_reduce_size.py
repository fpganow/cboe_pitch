from unittest import TestCase

from hamcrest import assert_that, has_length, is_

from cboe_pitch.reduce_size import ReduceSizeLong, ReduceSizeShort
from tests.comparator import compare_bytes


class TestReduceSize(TestCase):
    def test_reduce_size_long(self):
        # GIVEN
        message = ReduceSizeLong.from_parms(
            time_offset=447_000, order_id="ORID0001", canceled_quantity=20_000
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(18))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            18,  # Length
                            0x25,  # Message Type
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
                            0,  # Canceled Quantity
                        ]
                    )
                )
            ),
        )

    def test_reduce_size_short(self):
        # GIVEN
        message = ReduceSizeShort.from_parms(
            time_offset=447_000, order_id="ORID0001", canceled_quantity=20_000
        )

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(16))
        assert_that(
            msg_bytes,
            is_(
                compare_bytes(
                    bytearray(
                        [
                            16,  # Length
                            0x26,  # Message Type
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
                            0x4E,  # Canceled Quantity
                        ]
                    )
                )
            ),
        )
