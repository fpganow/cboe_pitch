from datetime import datetime
from unittest import TestCase

from hamcrest import assert_that, equal_to, has_length, is_
from pitch.generator import Generator

from pitch.add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from pitch.order_executed import OrderExecuted, OrderExecutedAtPriceSize
from pitch.reduce_size import ReduceSizeLong, ReduceSizeShort
# from pitch.trade import TradeLong, TradeShort, TradeExpanded
# from tests.comparator import compare_bytes


class TestGenerator(TestCase):
    def test_pickTicker_EdgeCase_0(self):
        # GIVEN
        watchList = []
        gen = Generator(watch_list=watchList)

        # WHEN
        ticker = gen._pickTicker()

        # THEN
        assert_that(ticker, equal_to(None))

    def test_pickTicker_EdgeCase_1(self):
        # GIVEN
        watchList = [("TSLA", 0.40)]
        gen = Generator(watch_list=watchList)

        # WHEN
        ticker = gen._pickTicker()

        # THEN
        assert_that(ticker, equal_to("TSLA"))

    def test_pickTicker_2_tickers(self):
        # GIVEN
        watchList = [("TSLA", 0.20), ("MSFT", 0.80)]
        gen = Generator(watch_list=watchList, seed=400)

        # WHEN
        ticker = gen._pickTicker()

        # THEN
        assert_that(ticker, equal_to("MSFT"))

    def test_timeOfFirstMessage(self):
        # GIVEN
        # Start Time: 9:30 AM
        # Rate of messages:
        #   - 100 messages per hour
        #   - per hour
        #     60 * 60 = seconds per hour = 3600 seconds per hour
        #   100 / (total # of seconds per hour) = 100 / 3600
        #   becomes x seconds between each message
        #   so 60 messages per hour becomes 60 / 3600 = 6 / 360 = 1/60
        #   or 60 seconds between each message
        # Time interval between messages
        # Message times:
        #   - 9:30
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList, rate=60, start_time=datetime(2023, 5, 7, 9, 30, 0)
        )

        # WHEN
        msg_time = gen._pickTime()

        # THEN
        assert_that(msg_time, equal_to(datetime(2023, 5, 7, 9, 30, 0)))

    def test_timeOfFirst_5_Messages(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            rate=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0)
        )

        # WHEN
        msg_time_1 = gen._pickTime()
        msg_time_2 = gen._pickTime()
        msg_time_3 = gen._pickTime()
        msg_time_4 = gen._pickTime()
        msg_time_5 = gen._pickTime()

        # THEN
        assert_that(msg_time_1, equal_to(datetime(2023, 5, 7, 9, 30, 0)))
        assert_that(msg_time_2, equal_to(datetime(2023, 5, 7, 9, 32, 0)))
        assert_that(msg_time_3, equal_to(datetime(2023, 5, 7, 9, 34, 0)))
        assert_that(msg_time_4, equal_to(datetime(2023, 5, 7, 9, 36, 0)))
        assert_that(msg_time_5, equal_to(datetime(2023, 5, 7, 9, 38, 0)))

    def test_pickMsgType_empty_orderbook(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            rate=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0)
        )

        # WHEN
        new_msg_type = gen._pickMsgType()

        # THEN
        assert_that(new_msg_type, equal_to(type(AddOrderLong)))

    def test_pickMsgType_several_orders(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            rate=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0)
        )

        # WHEN
        new_messages = []
        new_messages.append(gen._pickMsgType())

        # THEN
        assert_that(new_messages[0], equal_to(type(AddOrderLong)))

#    def test_smoke(self):
#        # GIVEN
#        watchList = [('AAPL', 0.40)]
#        rate = 10_000
#        totalTime = 60
#
#        # WHEN
#        gen = Generator(watchList=watchList, rate=rate, totalTime=totalTime)
#        msg = gen.getNext()
#
#        # THEN
#        assert_that(messages, has_length(10))
#
#    def test_trade_long(self):
#        # GIVEN
#        message = TradeLong.from_parms(time_offset=447_000,
#                                       order_id='ORID0001',
#                                       side='B',
#                                       quantity=20_000,
#                                       symbol='AAPL',
#                                       price=100.99,
#                                       execution_id='EXEID001')
#
#        # WHEN
#        msg_bytes = message.get_bytes()
#
#        # THEN
#        assert_that(msg_bytes, has_length(41))
#        assert_that(msg_bytes, is_(compare_bytes(bytearray([
#            41,  # Length
#            0x2A,  # Message Type
#            0x18, 0xD2, 6, 0,  # Time offset
#            0x4f, 0x52, 0x49, 0x44, 0x30, 0x30, 0x30, 0x31,  # Order Id
#            0x42,  # Side Indicator
#            0x20, 0x4E, 0x0, 0x0,  # Quantity
#            0x41, 0x41, 0x50, 0x4c, 0x20, 0x20,  # Symbol
#            0xec, 0x68, 0xf, 0, 0, 0, 0, 0,  # Price
#            0x45, 0x58, 0x45, 0x49, 0x44, 0x30, 0x30, 0x31,  # Execution Id
#        ]))))
#
#    def test_trade_short(self):
#        # GIVEN
#        message = TradeShort.from_parms(time_offset=447_000,
#                                        order_id='ORID0001',
#                                        side='B',
#                                        quantity=20_000,
#                                        symbol='AAPL',
#                                        price=100.99,
#                                        execution_id='EXE10012')
#
#        # WHEN
#        msg_bytes = message.get_bytes()
#
#        # THEN
#        assert_that(msg_bytes, has_length(33))
#        assert_that(msg_bytes, is_(compare_bytes(bytearray([
#            33,  # Length
#            0x2B,  # Message Type
#            0x18, 0xD2, 6, 0,  # Time offset
#            0x4f, 0x52, 0x49, 0x44, 0x30, 0x30, 0x30, 0x31,  # Order Id
#            0x42,  # Side Indicator
#            0x20, 0x4E,  # Quantity
#            0x41, 0x41, 0x50, 0x4c, 0x20, 0x20,  # Symbol
#            0x73, 0x27,  # Price
#            0x45, 0x58, 0x45, 0x31, 0x30, 0x30, 0x31, 0x32,  # Execution Id
#        ]))))
#
#    def test_trade_expanded(self):
#        # GIVEN
#        message = TradeExpanded.from_parms(time_offset=447_000,
#                                           order_id='ORID0001',
#                                           side='B',
#                                           quantity=20_000,
#                                           symbol='AAPL',
#                                           price=100.99,
#                                           execution_id='EXEID001')
#
#        # WHEN
#        msg_bytes = message.get_bytes()
#
#        # THEN
#        assert_that(msg_bytes, has_length(43))
#        assert_that(msg_bytes, is_(compare_bytes(bytearray([
#            43,  # Length
#            0x30,  # Message Type
#            0x18, 0xD2, 6, 0,  # Time offset
#            0x4f, 0x52, 0x49, 0x44, 0x30, 0x30, 0x30, 0x31,  # Order Id
#            0x42,  # Side Indicator
#            0x20, 0x4E, 0x0, 0x0,  # Quantity
#            0x41, 0x41, 0x50, 0x4c, 0x20, 0x20, 0x20, 0x20,  # Symbol
#            0xec, 0x68, 0xf, 0, 0, 0, 0, 0,  # Price
#            0x45, 0x58, 0x45, 0x49, 0x44, 0x30, 0x30, 0x31,  # Execution Id
#        ]))))
