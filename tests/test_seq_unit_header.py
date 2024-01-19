from pathlib import Path
from unittest import TestCase

import pkg_resources
from hamcrest import assert_that, has_length, equal_to, instance_of

from pitch.add_order import AddOrderShort, AddOrderLong
from pitch.seq_unit_header import SequencedUnitHeader
from pitch.time import Time
from .test_labview import Parameters


class TestSequencedUnitHeader(TestCase):
    def setUp(self):
        self._new_msgs = []
        self._new_msgs.append(
            AddOrderShort.from_parms(
                time_offset=100,
                order_id="ORID0100",
                side="B",
                quantity=100,
                symbol="AAPL",
                price=100.25,
            )
        )

    def test_smoke(self):
        # GIVEN
        start_seq_no = 100

        # WHEN
        seq_unit_hdr = SequencedUnitHeader(hdr_sequence=start_seq_no)
        hdr_bytes = seq_unit_hdr.get_bytes()

        # THEN
        assert_that(seq_unit_hdr.getNextSequence(), equal_to(start_seq_no))
        assert_that(list(hdr_bytes), equal_to([
            0x8, 0x00, 0x0, 0x1, 0x64, 0x0, 0x0, 0x0
            ]))

    def test_get_next_sequence(self):
        # GIVEN

        # WHEN
        seq_unit_hdr = SequencedUnitHeader()
        hdr_bytes = seq_unit_hdr.get_bytes()

        # THEN
        assert_that(seq_unit_hdr.getNextSequence(), equal_to(1))
        assert_that(list(hdr_bytes), equal_to([
            0x8, 0x00, 0x0, 0x1, 0x01, 0x0, 0x0, 0x0
            ]))

    def test_add_message(self):
        # WHEN
        seq_unit_hdr = SequencedUnitHeader(hdr_sequence=15)
        seq_unit_hdr.addMessage(self._new_msgs[0])
        hdr_bytes = seq_unit_hdr.get_bytes()

        # THEN
        assert_that(seq_unit_hdr.getNextSequence(), equal_to(16))
        assert_that(seq_unit_hdr.getLength(), equal_to(self._new_msgs[0].length() + 8))
        assert_that(list(hdr_bytes), equal_to([
            0x22, 0x00, 0x1, 0x1, 0x0F, 0x0, 0x0, 0x0, # Seq Unit Hdr
            6, 0x20, 0x98, 0x85, 0, 0  # Time
            ]))

    def test_str(self):
        # WHEN
        seq_unit_hdr = SequencedUnitHeader()
        seq_unit_hdr.addMessage(self._new_msgs[0])

        # THEN
        assert_that(
            str(seq_unit_hdr),
            equal_to("(SequencedUnitHeader, HdrLength=34, HdrCount=1)"),
        )

    def test_parse_single_seq_unit(self):
        # GIVEN
        data_path = "data/single_seq.dat"
        full_path = pkg_resources.resource_filename(__name__, data_path)
        in_bytes = Path(full_path).read_bytes()

        # WHEN
        [seq_unit_hdr, rem_bytes] = SequencedUnitHeader.from_bytestream(
            msg_bytes=in_bytes
        )
        new_msgs = seq_unit_hdr.getMessages()

        # THEN
        assert_that(rem_bytes, equal_to(None))
        assert_that(seq_unit_hdr.hdr_length(), equal_to(0x42))
        assert_that(seq_unit_hdr.hdr_count(), equal_to(3))
        assert_that(seq_unit_hdr.hdr_unit(), equal_to(1))
        assert_that(seq_unit_hdr.hdr_sequence(), equal_to(1))

        assert_that(new_msgs, has_length(3))
        assert_that(new_msgs[0], instance_of(Time))
        assert_that(new_msgs[1], instance_of(AddOrderShort))
        assert_that(new_msgs[2], instance_of(AddOrderShort))

    def test_parse_multi_seq_unit(self):
        # GIVEN
        data_path = "data/multi.dat"
        full_path = pkg_resources.resource_filename(__name__, data_path)
        in_bytes = Path(full_path).read_bytes()

        # WHEN - Parse 1st Sequenced Unit Header
        [seq_unit_hdr_1, rem_bytes] = SequencedUnitHeader.from_bytestream(
            msg_bytes=in_bytes
        )
        new_msgs = seq_unit_hdr_1.getMessages()

        # THEN
        assert_that(rem_bytes, not (equal_to(None)))
        assert_that(rem_bytes, has_length(len(in_bytes) - seq_unit_hdr_1.hdr_length()))

        assert_that(seq_unit_hdr_1.hdr_length(), equal_to(0x42))
        assert_that(seq_unit_hdr_1.hdr_count(), equal_to(3))
        assert_that(seq_unit_hdr_1.hdr_unit(), equal_to(1))
        assert_that(seq_unit_hdr_1.hdr_sequence(), equal_to(1))

        assert_that(new_msgs, has_length(3))
        assert_that(new_msgs[0], instance_of(Time))
        assert_that(new_msgs[1], instance_of(AddOrderShort))
        assert_that(new_msgs[2], instance_of(AddOrderShort))

        # WHEN - Parse 2nd Sequenced Unit Header
        [seq_unit_hdr_2, rem_bytes] = SequencedUnitHeader.from_bytestream(
            msg_bytes=rem_bytes
        )
        new_msgs = seq_unit_hdr_2.getMessages()

        # THEN
        assert_that(rem_bytes, not (equal_to(None)))
        assert_that(
            rem_bytes,
            has_length(
                len(in_bytes)
                - (seq_unit_hdr_1.hdr_length() + seq_unit_hdr_2.hdr_length())
            ),
        )

        assert_that(seq_unit_hdr_2.hdr_length(), equal_to(0x4C))
        assert_that(seq_unit_hdr_2.hdr_count(), equal_to(2))
        assert_that(seq_unit_hdr_2.hdr_unit(), equal_to(1))
        assert_that(seq_unit_hdr_2.hdr_sequence(), equal_to(4))

        assert_that(new_msgs, has_length(2))
        assert_that(new_msgs[0], instance_of(AddOrderLong))
        assert_that(new_msgs[0], instance_of(AddOrderLong))
