from unittest import TestCase

from hamcrest import assert_that, has_length, is_

from pitch.delete_order import DeleteOrder
from tests.comparator import compare_bytes


class TestDeleteOrder(TestCase):
    def test_delete_order(self):
        # GIVEN
        message = DeleteOrder.from_parms(time_offset=447_000,
                                         order_id='ORID0001')

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(14))
        assert_that(msg_bytes, is_(compare_bytes(bytearray([
            14,  # Length
            0x29,  # Message Type
            0x18, 0xD2, 6, 0,  # Time offset
            0x4f, 0x52, 0x49, 0x44, 0x30, 0x30, 0x30, 0x31,  # Order Id
        ]))))
