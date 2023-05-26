from datetime import datetime
from unittest import TestCase

from hamcrest import any_of, assert_that, equal_to, has_length, is_, is_in
from pitch.generator import Generator

from pitch.add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from pitch.order_executed import OrderExecuted, OrderExecutedAtPriceSize
from pitch.reduce_size import ReduceSizeLong, ReduceSizeShort

from pitch.generator import WatchListItem

class TestGenerator(TestCase):

    # 1 - Pick Ticker
    def test_pickTicker_EdgeCase_0(self):
        # GIVEN
        watch_list = []

        # WHEN
        with self.assertRaises(Exception):
            gen = Generator(watch_list=watch_list)

    def test_pickTicker_EdgeCase_1(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA',
                          weight=0.40)]
        gen = Generator(watch_list=watch_list)

        # WHEN
        ticker = gen._pickTicker()

        # THEN
        assert_that(ticker, equal_to("TSLA"))

    def test_pickTicker_2_tickers(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(watch_list=watch_list, seed=400)

        # WHEN
        ticker = gen._pickTicker()

        # THEN
        assert_that(ticker, equal_to("MSFT"))

    # 2 - Pick Side
    def test_pickSide_Buy(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list, seed=200
        )

        # WHEN
        side = gen._pickSide()

        # THEN
        assert_that(side, equal_to(Generator.Side.Buy))

    def test_pickSide_Sell(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list, seed=10
        )

        # WHEN
        side = gen._pickSide()

        # THEN
        assert_that(side, equal_to(Generator.Side.Sell))

    # 3 - Pick Message Time
    def test_pickTime_first(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=60,
            start_time=datetime(2023, 5, 7, 9, 30, 0)
        )

        # WHEN
        msg_time = gen._pickTime()

        # THEN
        assert_that(msg_time, equal_to(datetime(2023, 5, 7, 9, 30, 0)))

    def test_picLkTime_first_5_Messages(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=2,
            start_time=datetime(2023, 5, 7, 9, 30, 0)
        )

        # WHEN
        msg_time_1 = gen._pickTime()
        msg_time_2 = gen._pickTime()
        msg_time_3 = gen._pickTime()
        msg_time_4 = gen._pickTime()
        msg_time_5 = gen._pickTime()

        # THEN
        assert_that(msg_time_1, equal_to(datetime(2023, 5, 7, 9, 30, 0, 0)))
        assert_that(msg_time_2, equal_to(datetime(2023, 5, 7, 9, 30, 0, 500_000)))
        assert_that(msg_time_3, equal_to(datetime(2023, 5, 7, 9, 30, 1, 0)))
        assert_that(msg_time_4, equal_to(datetime(2023, 5, 7, 9, 30, 1, 500_000)))
        assert_that(msg_time_5, equal_to(datetime(2023, 5, 7, 9, 30, 2, 0)))

    # 4 - Pick Message Category
    def test_pickMsgCategory_empty_orderbook(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=1,
            start_time=datetime(2023, 5, 7, 9, 30, 0)
        )
        ticker='TSLA'
        side=Generator.Side.Buy

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Add))

    def test_pickMsgType_too_many_orders(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20, book_size_range=(1,3)),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=1,
            start_time=datetime(2023, 5, 7, 9, 30, 0)
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._order_book[ticker] = {
            Generator.Side.Buy: [
                Generator.Order(ticker=ticker,
                                side=side,
                                price=50.05,
                                quantity=100,
                                order_id="ORID0001"),
                Generator.Order(ticker=ticker,
                                side=side,
                                price=50.04,
                                quantity=100,
                                order_id="ORID0002"),
                Generator.Order(ticker=ticker,
                                side=side,
                                price=50.03,
                                quantity=100,
                                order_id="ORID0003"),
                Generator.Order(ticker=ticker,
                                side=side,
                                price=50.02,
                                quantity=100,
                                order_id="ORID0004"),
            ],
            Generator.Side.Sell: []
        }

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Remove))

    def test_pickMsgType_within_size(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA', weight=0.20, book_size_range=(1,3)),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=1,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            seed=100
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._order_book[ticker] = {
            Generator.Side.Buy: [ (50.05, 100), (50.04, 100),
                                  (50.03, 100)
                                  ],
            Generator.Side.Sell: []
        }

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Edit))

    def test_pickPriceSize_Size_25_500(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker="TSLA",
                          weight=1.00,
                          book_size_range=(1, 3),
                          price_range=(50, 55),
                          size_range=(25, 200))
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=1,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            seed=100
        )
        ticker='TSLA'
        side=Generator.Side.Buy

        # WHEN
        (new_price, new_size) = gen._pickPriceSize(ticker=ticker, side=side)

        # THEN
        assert_that(new_price, equal_to(54.17))
        assert_that(new_size, equal_to(25))

    def test_next_order_id(self):
        # GIVEN
        watch_list = [WatchListItem(ticker="TSLA", weight=1.00)]
        gen = Generator(watch_list=watch_list)

        # WHEN
        next_order_id = gen._getNextOrderId()

        # THEN
        assert_that(next_order_id, equal_to("ORID0001"))

    def test_next_order_id_3_digit(self):
        # GIVEN
        watch_list = [WatchListItem(ticker="NVDA", weight=1.00)]
        gen = Generator(watch_list=watch_list)

        # WHEN
        gen._nextOrderNum += 99
        next_order_id = gen._getNextOrderId()

        # THEN
        assert_that(next_order_id, equal_to("ORID0100"))

    def test_getNextMsg_addOrder(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker='TSLA',
                          weight=0.20,
                          book_size_range=(1,3),
                          price_range=(75, 100),
                          size_range=(25,100)),
            WatchListItem(ticker='MSFT', weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            seed=100
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._order_book[ticker] = {
                Generator.Side.Buy: [
                    Generator.Order(ticker=ticker,
                                    side=side,
                                    price=75.05,
                                    quantity=100,
                                    order_id="ORID0001"),
                    Generator.Order(ticker=ticker,
                                    side=side,
                                    price=75.04,
                                    quantity=100,
                                    order_id="ORID0002"),
                    ],
                Generator.Side.Sell: []
        }

        # WHEN
        new_msg = gen._getNextMsg(ticker=ticker,
                                  side=side,
                                  new_timestamp=gen._pickTime(),
                                  new_msg_cat=Generator.MsgType.Add)

        print(f'new_msg: {str(new_msg)}')

        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Add]))
        #assert_that(new_msg.ticker(), equal_to('TSLA'))
        assert_that(gen._order_book[ticker][Generator.Side.Buy], has_length(3))

    def test_editOrder(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            msg_rate_p_sec=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            book_size_range = (1, 3),
            seed=100
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._orderBook[ticker] = {
                Generator.Side.Buy: [ (50.05, 100), (50.04, 100),
                    (50.03, 50)
                    ],
                Generator.Side.Sell: []
        }

        # WHEN
        new_msg = gen._getNextMsg(ticker=ticker,
                                  side=side,
                                  new_timestamp=gen._pickTime(),
                                  new_msg_cat=Generator.MsgType.Add)

        print(f'new_msg: {str(new_msg)}')

        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Edit]))
        #assert_that(new_msg.ticker(), equal_to('TSLA'))
        assert_that(gen._orderBook[ticker][Generator.Side.Buy], has_length(3))

    def test_deleteOrder(self):
        # GIVEN
        watchList = [("TSLA", 1.00)]
        gen = Generator(
            watch_list=watchList,
            msg_rate_p_sec=30,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            book_size_range = (1, 2),
            seed=100
        )
        ticker='TSLA'
        side=Generator.Side.Buy
        gen._orderBook[ticker] = {
                Generator.Side.Buy: [ (50.05, 100), (50.04, 100),
                    (50.03, 50)
                    ],
                Generator.Side.Sell: []
        }

        # WHEN
        new_msg = gen._getNextMsg(ticker=ticker,
                                  side=side,
                                  new_timestamp=gen._pickTime(),
                                  new_msg_cat=Generator.MsgType.Add)

        print(f'new_msg: {str(new_msg)}')

        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Edit]))
        assert_that(new_msg.symbol(), equal_to('TSLA'))
        assert_that(gen._orderBook[ticker][Generator.Side.Buy], has_length(2))
