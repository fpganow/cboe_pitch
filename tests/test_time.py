from unittest import TestCase

from hamcrest import assert_that, has_length, is_, equal_to, instance_of

from pitch.message_factory import MessageFactory
from pitch.time import Time
from tests.comparator import compare_bytes


class TestTime(TestCase):
    def test_timestamp_create(self):
        # GIVEN
        # 34_200 seconds = 9:30 AM
        message = Time.from_parms(time=34_200)

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(6))
        assert_that(msg_bytes, is_(compare_bytes(bytearray([
            6,  # Length
            0x20,  # Type
            0x98, 0x85, 0, 0  # Time
        ]))))
        assert_that(message.length(), equal_to(6))
        assert_that(message.messageType(), equal_to(0x20))
        assert_that(message.time(), equal_to(34_200))

    def test_timestamp_short_create(self):
        # GIVEN
        # 200 seconds
        message = Time.from_parms(time=200)

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(6))
        assert_that(msg_bytes, is_(compare_bytes(bytearray([
            6,  # Length
            0x20,  # Type
            0xc8, 0, 0, 0  # Time
        ]))))
        assert_that(message.length(), equal_to(6))
        assert_that(message.messageType(), equal_to(0x20))
        assert_that(message.time(), equal_to(200))

    def test_timestamp_parse_1_byte(self):
        # GIVEN
        msg_bytes = bytearray([0x06, 0x20, 0xc8, 0x00, 0x00, 0x00])

        # WHEN
        message = MessageFactory.from_bytes(msg_bytes)

        # THEN
        assert_that(message, instance_of(Time))
        assert_that(message.length(), equal_to(6))
        assert_that(message.messageType(), equal_to(0x20))
        assert_that(message.time(), equal_to(200))

    def test_timestamp_parse_4_bytes(self):
        # GIVEN
        msg_bytes = bytearray([0x06, 0x20, 0xfe, 0xdc, 0xba, 0x11])

        # WHEN
        message = MessageFactory.from_bytes(msg_bytes)

        # THEN
        assert_that(message, instance_of(Time))
        assert_that(message.length(), equal_to(6))
        assert_that(message.messageType(), equal_to(0x20))
        assert_that(message.time(), equal_to(297_458_942))
        assert_that(message.time(), equal_to(0x11_ba_dc_fe))
