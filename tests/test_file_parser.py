from unittest import TestCase

from hamcrest import assert_that, equal_to, has_length, instance_of

from pathlib import Path
from pitch.file_parser import FileParser
from pitch.add_order import AddOrderShort, AddOrderLong
from pitch.time import Time
import pkg_resources


class TestFileParser(TestCase):
    def test_parse_missing_file(self):
        # GIVEN
        file_path = Path("fake_file_dne_2023")

        # WHEN
        with self.assertRaises(Exception):
            FileParser.parse_file(file_path=file_path)

    def test_parse_multi_seq_unit(self):
        # Output of generator:
        #
        #        Offset=0x0: (SequencedUnitHeader, HdrLength=66, HdrCount=3)
        #        DEBUG: bytes: 0x42, 0x0, 0x3, 0x1, 0x1, 0x0, 0x0, 0x0
        #                 - Offset=0x8: (Time, 68,254)
        #                 - Offset=0xe: (AddOrderShort, 0, ORID0001, B, 5, MSFT, $332.08)
        #                 - Offset=0x28: (AddOrderShort, 200,000,000, ORID0002, B, 125, GE, $51.91)
        #        Offset=0x42: (SequencedUnitHeader, HdrLength=76, HdrCount=2)
        #        DEBUG: bytes: 0x4c, 0x0, 0x2, 0x1, 0x4, 0x0, 0x0, 0x0
        #                 - Offset=0x4a: (AddOrderLong, 400,000,000, ORID0003, B, 30, MSFT, $331.03)
        #                 - Offset=0x6c: (AddOrderLong, 600,000,000, ORID0004, S, 5, MSFT, $323.8)
        #        Offset=0x8e: (SequencedUnitHeader, HdrLength=82, HdrCount=3)
        #        DEBUG: bytes: 0x52, 0x0, 0x3, 0x1, 0x6, 0x0, 0x0, 0x0
        #                 - Offset=0x96: (AddOrderLong, 800,000,000, ORID0005, B, 30, MSFT, $325.61)
        #                 - Offset=0xb8: (Time, 68,255)
        #                 - Offset=0xbe: (AddOrderLong, 0, ORID0006, S, 150, GE, $58.99)
        #        Offset=0xe0: (SequencedUnitHeader, HdrLength=76, HdrCount=2)
        #        DEBUG: bytes: 0x4c, 0x0, 0x2, 0x1, 0x9, 0x0, 0x0, 0x0
        #                 - Offset=0xe8: (AddOrderLong, 200,000,000, ORID0007, S, 150, GE, $54.47)
        #                 - Offset=0x10a: (AddOrderLong, 400,000,000, ORID0008, S, 100, GE, $53.21)
        # GIVEN
        data_path = "data/multi.dat"
        full_path = pkg_resources.resource_filename(__name__, data_path)

        # WHEN
        seq_array = FileParser.parse_file(file_path=full_path)

        # THEN
        assert_that(seq_array, has_length(4))

        assert_that(seq_array[0].getMessages()[0], instance_of(Time))
        assert_that(seq_array[0].getMessages()[1], instance_of(AddOrderShort))
        assert_that(seq_array[0].getMessages()[2], instance_of(AddOrderShort))

        assert_that(seq_array[1].getMessages()[0], instance_of(AddOrderLong))
        assert_that(seq_array[1].getMessages()[1], instance_of(AddOrderLong))

        assert_that(seq_array[2].getMessages()[0], instance_of(AddOrderLong))
        assert_that(seq_array[2].getMessages()[1], instance_of(Time))
        assert_that(seq_array[2].getMessages()[2], instance_of(AddOrderLong))

        assert_that(seq_array[3].getMessages()[0], instance_of(AddOrderLong))
        assert_that(seq_array[3].getMessages()[0].order_id(), equal_to("ORID0007"))
        assert_that(seq_array[3].getMessages()[1], instance_of(AddOrderLong))
