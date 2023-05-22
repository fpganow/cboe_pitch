from datetime import datetime
from unittest import TestCase

from hamcrest import any_of, assert_that, equal_to, has_length, is_, is_in
from pitch.generator import Generator

from pitch.add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from pitch.order_executed import OrderExecuted, OrderExecutedAtPriceSize
from pitch.reduce_size import ReduceSizeLong, ReduceSizeShort



class TestGenerator(TestCase):

    # 1 - Pick Ticker
    def test_pickTicker_EdgeCase_0(self):
        # GIVEN
        watchList = []
        gen = Generator(watch_list=watchList)

        # WHEN
        with self.assertRaises(Exception):
            gen._pickTicker()

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

    # 2 - Pick Side
    def test_pickSide_Buy(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList, seed=200
        )

        # WHEN
        side = gen._pickSide()

        # THEN
        assert_that(side, equal_to(Generator.Side.Buy))

    def test_pickSide_Sell(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList, seed=10
        )

        # WHEN
        side = gen._pickSide()

        # THEN
        assert_that(side, equal_to(Generator.Side.Sell))

    # 3 - Pick Message Time
    def test_pickTime_firstMessage(self):
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

    def test_pickTime_first_5_Messages(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList, rate=30, start_time=datetime(2023, 5, 7, 9, 30, 0)
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

    # 4 - Pick Message Type
    def test_pickMsgType_empty_orderbook(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList, rate=30, start_time=datetime(2023, 5, 7, 9, 30, 0)
        )
        ticker='TSLA'
        side=Generator.Side.Buy

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Add))

    def test_pickMsgType_too_many_orders(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            rate=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            book_size_range = (1, 3)
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._orderBook[ticker] = {
                Generator.Side.Buy: [ (50.05, 100), (50.04, 100),
                                      (50.03, 100), (50.02, 100)
                    ],
                Generator.Side.Sell: []
        }

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Remove))

    def test_pickMsgType_within_size(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            rate=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            book_size_range = (1, 3),
            seed=100
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._orderBook[ticker] = {
                Generator.Side.Buy: [ (50.05, 100), (50.04, 100),
                                      (50.02, 100)
                    ],
                Generator.Side.Sell: []
        }

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Edit))

    def test_pickPriceSize_Size_25_500(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            rate=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            book_size_range = (1, 3),
            price_range = (50, 55),
            size_range = (25, 100),
            seed=500
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._orderBook[ticker] = {
                Generator.Side.Buy: [ (50.05, 100), (50.04, 100)
                    ],
                Generator.Side.Sell: []
        }

        # WHEN
        (new_price, new_size) = gen._pickPriceSize()

        # THEN
        assert_that(new_price, equal_to(52.83))
        assert_that(new_size, equal_to(50))

    def test_smoke(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            rate=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            book_size_range = (1, 3),
            seed=100
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._orderBook[ticker] = {
                Generator.Side.Buy: [ (50.05, 100), (50.04, 100)
                    ],
                Generator.Side.Sell: []
        }

        # WHEN
        new_msg = gen._getNextMsg(ticker=ticker,
                                  side=side,
                                  new_timestamp=gen._pickTime(),
                                  new_msg_cat=Generator.MsgType.Add)

        print(f'new_msg: {new_msg}')
        if new_msg == AddOrderLong:
            print(f'AddOrderLong')

        # THEN
        assert_that(new_msg, is_in(gen._msgTypes[Generator.MsgType.Edit]))
