from typing import List
from hamcrest import (
    assert_that,
    has_length,
    is_
)
import logging
from unittest import TestCase
from pitch.seq_unit_header import SequencedUnitHeader
from tests.comparator import compare_bytes

logger = logging.getLogger(__name__)


def dump_msg_bytes(msg_bytes: List[int]) -> None:
    print('\n')
    for idx, byte_i in enumerate(msg_bytes):
        print(f' [{idx}] = {byte_i}')


class TestSeqUnitHeader(TestCase):
    def test_sequenced_unit_header_create(self):
        # GIVEN
        message = SequencedUnitHeader(hdr_count=0,
                                      hdr_unit=1,
                                      hdr_sequence=1)

        # WHEN
        msg_bytes = message.get_bytes()

        # THEN
        assert_that(msg_bytes, has_length(8))
        assert_that(msg_bytes, is_(compare_bytes(bytearray([
            8, 0,  # Hdr Length
            0,  # Hdr Count
            1,  # Hdr Unit
            1, 0, 0, 0  # Hdr Sequence
        ]))))


