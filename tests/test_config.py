from unittest import TestCase

from hamcrest import assert_that, has_key, has_length, equal_to

from cboe_pitch.config import Config


class TestConfig(TestCase):
    def test_no_config(self):
        with self.assertRaises(Exception):
            Config()

    def test_simple(self):
        # GIVEN
        raw_text = """
        num_of_msgs: 4
        msg_rate_p_sec: 5
        verbose: False
        output_file: orders.dat
        audit_log_file: audit.log
        trace_log_file: trace.log
        watchlist:
          GE:
            weight: 0.40
            book_size: [1, 3]
            price_range: [50.00, 60.00]
            size_range: [25, 200]
          MSFT:
            weight: 0.60
            book_size: [10, 20]
            price_range: [320.00, 340.00]
            size_range: [5, 50]
        """

        # WHEN
        config = Config(text=raw_text)
        watch_list = config.watch_list()

        # THEN
        assert_that(config.num_of_msgs(), equal_to(4))
        assert_that(config.msg_rate_p_sec(), equal_to(5))
        assert_that(config.verbose(), equal_to(False))
        assert_that(config.output_file(), equal_to("orders.dat"))
        assert_that(config.audit_log_file(), equal_to("audit.log"))
        assert_that(config.trace_log_file(), equal_to("trace.log"))

        assert_that(watch_list.keys(), has_length(2))
        assert_that(watch_list, has_key("GE"))
        assert_that(watch_list["GE"]["weight"], equal_to(0.40))
        assert_that(watch_list["GE"]["book_size"], equal_to([1, 3]))
        assert_that(watch_list["GE"]["price_range"], equal_to([50.00, 60.00]))
        assert_that(watch_list["GE"]["size_range"], equal_to([25, 200]))

        assert_that(watch_list, has_key("MSFT"))
        assert_that(watch_list["MSFT"]["weight"], equal_to(0.60))
        assert_that(watch_list["MSFT"]["book_size"], equal_to([10, 20]))
        assert_that(watch_list["MSFT"]["price_range"], equal_to([320.00, 340.00]))
        assert_that(watch_list["MSFT"]["size_range"], equal_to([5, 50]))
