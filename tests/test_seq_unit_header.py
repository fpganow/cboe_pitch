from unittest import TestCase

from hamcrest import assert_that, has_length, is_, equal_to, instance_of

from pitch.add_order import AddOrderShort
from pitch.seq_unit_header import SequencedUnitHeader

class TestSequencedUnitHeader(TestCase):
    def setUp(self):
        self._new_msgs = []
        self._new_msgs.append(AddOrderShort.from_parms(time_offset=100,
                                            order_id="ORID0100",
                                            side='B',
                                            quantity=100,
                                            symbol='AAPL',
                                            price=100.25))

    def test_smoke(self):
        # GIVEN
        start_seq_no = 100

        # WHEN
        seq_unit_hdr = SequencedUnitHeader(hdr_sequence=start_seq_no)

        # THEN
        assert_that(seq_unit_hdr.getNextSequence(), equal_to(start_seq_no))

    def test_get_next_sequence(self):
        # GIVEN

        # WHEN
        seq_unit_hdr = SequencedUnitHeader()

        # THEN
        assert_that(seq_unit_hdr.getNextSequence(), equal_to(1))

    def test_add_message(self):
        # WHEN
        seq_unit_hdr = SequencedUnitHeader()
        seq_unit_hdr.addMessage(self._new_msgs[0])

        # THEN
        assert_that(seq_unit_hdr.getNextSequence(), equal_to(2))
        assert_that(seq_unit_hdr.getLength(), equal_to(self._new_msgs[0].length() + 8))

    def test_str(self):
        # WHEN
        seq_unit_hdr = SequencedUnitHeader()
        seq_unit_hdr.addMessage(self._new_msgs[0])

        # THEN
        assert_that(str(seq_unit_hdr), equal_to('(SequencedUnitHeader, HdrLength=34, HdrCount=1)'))
