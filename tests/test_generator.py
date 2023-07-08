from datetime import datetime
from typing import Tuple
from unittest import TestCase
from unittest.mock import patch

from hamcrest import (
    assert_that,
    equal_to,
    has_length,
    is_in,
    greater_than_or_equal_to,
    less_than_or_equal_to,
    all_of,
    instance_of,
    not_,
)

from pitch import ModifyOrderLong, TradeLong
from pitch.add_order import AddOrderLong, AddOrderShort
from pitch.delete_order import DeleteOrder
from pitch.generator import Generator
from pitch.generator import WatchListItem
from pitch.order_executed import OrderExecutedAtPriceSize
from pitch.orderbook import Side
from pitch.reduce_size import ReduceSizeLong


def setupTest(
    ticker: str,
    side: "Side",
    book_size_range: Tuple[int, int] = None,
    price_range: Tuple[float, float] = None,
    size_range: Tuple[int, int] = None,
    num_orders: int = None,
    seed: int = None,
):
    if book_size_range is None:
        book_size_range = (1, 3)
    if price_range is None:
        price_range = (75, 100)
    if size_range is None:
        size_range = (25, 200)
    if num_orders is None:
        num_orders = 2
    if seed is None:
        seed = 100

    watch_list = [
        WatchListItem(
            ticker=ticker,
            weight=0.25,
            book_size_range=book_size_range,
            price_range=price_range,
            size_range=size_range,
        )
    ]
    gen = Generator(
        watch_list=watch_list,
        msg_rate_p_sec=30,
        start_time=datetime(2023, 5, 7, 9, 30, 0),
        seed=seed,
    )
    gen._orderbook.add_ticker(ticker=ticker)
    if num_orders != 0:
        start_price = price_range[1] if side == Side.Buy else price_range[0]
        price_interval = (price_range[1] - price_range[0]) / (num_orders * 2)
        if side == Side.Buy:
            price_interval *= -1
        # print(f'start_price: {start_price}')
        # print(f'price_interval: {price_interval}')
        for i in range(num_orders):
            start_price += price_interval
            # print(f'start_price: {start_price}')
            gen._orderbook.add_order(
                ticker=ticker,
                side=side,
                price=start_price,
                quantity=100,
                order_id=gen._getNextOrderId(),
            )
    return gen


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
        watch_list = [WatchListItem(ticker="TSLA", weight=0.40)]
        gen = Generator(watch_list=watch_list)

        # WHEN
        ticker = gen._pickTicker()

        # THEN
        assert_that(ticker, equal_to("TSLA"))

    def test_pickTicker_2_tickers(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker="TSLA", weight=0.20),
            WatchListItem(ticker="MSFT", weight=0.80),
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
            WatchListItem(ticker="TSLA", weight=0.20),
            WatchListItem(ticker="MSFT", weight=0.80),
        ]
        gen = Generator(watch_list=watch_list, seed=200)

        # WHEN
        side = gen._pickSide()

        # THEN
        assert_that(side, equal_to(Side.Buy))

    def test_pickSide_Sell(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker="TSLA", weight=0.20),
            WatchListItem(ticker="MSFT", weight=0.80),
        ]
        gen = Generator(watch_list=watch_list, seed=10)

        # WHEN
        side = gen._pickSide()

        # THEN
        assert_that(side, equal_to(Side.Sell))

    # 3 - Pick Message Time
    def test_pickTime_first(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker="TSLA", weight=0.20),
            WatchListItem(ticker="MSFT", weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=60,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
        )

        # WHEN
        msg_time = gen._pickTimeOffset()

        # THEN
        assert_that(msg_time, equal_to(datetime(2023, 5, 7, 9, 30, 0)))

    def test_picLkTime_first_5_Messages(self):
        # GIVEN
        watch_list = [
            WatchListItem(ticker="TSLA", weight=0.20),
            WatchListItem(ticker="MSFT", weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=2,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
        )

        # WHEN
        msg_time_1 = gen._pickTimeOffset()
        msg_time_2 = gen._pickTimeOffset()
        msg_time_3 = gen._pickTimeOffset()
        msg_time_4 = gen._pickTimeOffset()
        msg_time_5 = gen._pickTimeOffset()

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
            WatchListItem(ticker="TSLA", weight=0.20),
            WatchListItem(ticker="MSFT", weight=0.80),
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=1,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
        )
        ticker = "TSLA"
        side = Side.Buy

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Add))

    def test_pickMsgType_too_many_orders(self):
        # GIVEN
        ticker = "TSLA"
        side = Side.Buy
        price_range = (75, 100)
        size_range = (25, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=4,
        )

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Remove))

    def test_pickMsgType_within_size(self):
        # GIVEN
        ticker = "TSLA"
        side = Side.Buy
        price_range = (75, 100)
        size_range = (25, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=3,
        )

        # WHEN
        new_msg_cat = gen._pickMsgCategory(ticker=ticker, side=side)

        # THEN
        assert_that(new_msg_cat, equal_to(Generator.MsgType.Edit))

    def test_pickPriceSize_Size_25_500(self):
        # GIVEN
        watch_list = [
            WatchListItem(
                ticker="TSLA",
                weight=1.00,
                book_size_range=(1, 3),
                price_range=(50, 55),
                size_range=(25, 200),
            )
        ]
        gen = Generator(
            watch_list=watch_list,
            msg_rate_p_sec=1,
            start_time=datetime(2023, 5, 7, 9, 30, 0),
            seed=100,
        )
        price_range = (50, 150)
        size_range = (25, 300)

        # WHEN
        new_price = gen._pickNewPrice(price_range=price_range, old_price=100.00)
        new_size = gen._pickNewSize(size_range=size_range, old_size=50)

        # THEN
        assert_that(new_price, not_(equal_to(100.00)))
        assert_that(new_size, not_(equal_to(50)))

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

    @patch("pitch.generator.Generator._pickRandomMessageFromCategory")
    def test_getNextMsg_Add_AddOrderLong(self, pick_rand_msg):
        # GIVEN
        pick_rand_msg.return_value = AddOrderLong
        ticker = "TSLA"
        side = Side.Buy
        price_range = (75, 100)
        size_range = (25, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=2,
        )

        # WHEN
        # Mock out call to pick a random message type based on the passed
        # in category
        new_msg = gen._getNextMsg(
            ticker=ticker,
            side=side,
            new_timestamp=gen._pickTimeOffset(),
            new_msg_cat=Generator.MsgType.Add,
        )

        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Add]))
        assert_that(new_msg, instance_of(AddOrderLong))
        assert_that(new_msg.symbol(), equal_to("TSLA"))
        assert_that(new_msg.side(), equal_to("B"))
        assert_that(new_msg.order_id(), equal_to("ORID0003"))
        assert_that(
            new_msg.price(),
            all_of(
                greater_than_or_equal_to(price_range[0]),
                less_than_or_equal_to(price_range[1]),
            ),
        )
        assert_that(
            new_msg.quantity(),
            all_of(
                greater_than_or_equal_to(size_range[0]),
                less_than_or_equal_to(size_range[1]),
            ),
        )

    @patch("pitch.generator.Generator._pickRandomMessageFromCategory")
    def test_getNextMsg_Add_AddOrderShort(self, pick_rand_msg):
        # GIVEN
        pick_rand_msg.return_value = AddOrderShort
        ticker = "MSFT"
        side = Side.Buy
        price_range = (50, 100)
        size_range = (50, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=0,
        )

        # WHEN
        # Mock out call to pick a random message type based on the passed
        # in category
        new_msg = gen._getNextMsg(
            ticker=ticker,
            side=side,
            new_timestamp=gen._pickTimeOffset(),
            new_msg_cat=Generator.MsgType.Add,
        )

        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Add]))
        assert_that(new_msg, instance_of(AddOrderShort))

        assert_that(new_msg.symbol(), equal_to("MSFT"))
        assert_that(new_msg.side(), equal_to("B"))
        assert_that(new_msg.order_id(), equal_to("ORID0001"))
        assert_that(
            new_msg.price(),
            all_of(
                greater_than_or_equal_to(price_range[0]),
                less_than_or_equal_to(price_range[1]),
            ),
        )
        assert_that(
            new_msg.quantity(),
            all_of(
                greater_than_or_equal_to(size_range[0]),
                less_than_or_equal_to(size_range[1]),
            ),
        )

    @patch("pitch.generator.Generator._pickRandomOrder")
    @patch("pitch.generator.Generator._pickRandomMessageFromCategory")
    def test_getNextMsg_Edit_ModifyOrderLong(self, pick_rand_msg, pick_rand_ord):
        # GIVEN
        pick_rand_msg.return_value = ModifyOrderLong
        ticker = "MSFT"
        side = Side.Buy
        price_range = (50, 100)
        size_range = (50, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=4,
            seed=9900,
        )
        selected_order = gen._orderbook.get_orders(ticker=ticker, side=side)[0]
        pick_rand_ord.return_value = selected_order
        old_price = selected_order._price
        old_size = selected_order._quantity

        # WHEN
        print("\n-- Edit Order Test --")
        print(f"selected_order: ({selected_order})")
        # print('-- Order Book Before --')
        # gen.print_OrderBook(ticker=ticker)
        # Mock out call to pick a random message type based on the passed
        # in category
        new_msg = gen._getNextMsg(
            ticker=ticker,
            side=side,
            new_timestamp=gen._pickTimeOffset(),
            new_msg_cat=Generator.MsgType.Edit,
        )

        # print(f'Modify Message: {new_msg}')
        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Edit]))
        assert_that(new_msg, instance_of(ModifyOrderLong))

        print(f"new_msg.order_id(): {new_msg.order_id()}")
        print(f"selected_order._order_id: {selected_order._order_id}")
        assert_that(new_msg.order_id(), equal_to(selected_order._order_id))
        # Make sure new price is in the appropriate range
        assert_that(
            new_msg.price(),
            all_of(
                greater_than_or_equal_to(price_range[0]),
                less_than_or_equal_to(price_range[1]),
            ),
        )
        # Make sure that the price has changed
        print(f"old_price: {old_price}")
        print(f"new_msg.price(): {new_msg.price()}")
        assert_that(new_msg.price(), not (equal_to(old_price)))
        # Make sure new size is in the appropriate range
        assert_that(
            new_msg.quantity(),
            all_of(
                greater_than_or_equal_to(size_range[0]),
                less_than_or_equal_to(size_range[1]),
            ),
        )
        # Make sure that the size/quantity has changed
        print(f"old_size: {old_size}")
        print(f"new_msg.quantity(): {new_msg.quantity()}")
        assert_that(new_msg.quantity(), not (equal_to(old_size)))

    @patch("pitch.generator.Generator._pickRandomOrder")
    @patch("pitch.generator.Generator._pickRandomMessageFromCategory")
    def test_getNextMsg_Edit_OrderExecutedAtPriceSize(
        self, pick_rand_msg, pick_rand_ord
    ):
        # GIVEN
        pick_rand_msg.return_value = OrderExecutedAtPriceSize
        ticker = "MSFT"
        side = Side.Buy
        price_range = (50, 100)
        size_range = (50, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=4,
            seed=9900,
        )
        selected_order = gen._orderbook.get_orders(ticker=ticker, side=side)[0]
        pick_rand_ord.return_value = selected_order
        old_price = selected_order._price
        old_size = selected_order._quantity

        # WHEN
        print("\n-- Edit Order Test --")
        print(f"selected_order: ({selected_order})")
        # Mock out call to pick a random message type based on the passed
        # in category
        new_msg = gen._getNextMsg(
            ticker=ticker,
            side=side,
            new_timestamp=gen._pickTimeOffset(),
            new_msg_cat=Generator.MsgType.Edit,
        )

        # print(f'Modify Message: {new_msg}')
        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Edit]))
        assert_that(new_msg, instance_of(OrderExecutedAtPriceSize))

        print(f"new_msg.order_id(): {new_msg.order_id()}")
        print(f"selected_order._order_id: {selected_order._order_id}")
        assert_that(new_msg.order_id(), equal_to(selected_order._order_id))
        # Make sure new price is in the appropriate range
        assert_that(
            new_msg.price(),
            all_of(
                greater_than_or_equal_to(price_range[0]),
                less_than_or_equal_to(price_range[1]),
            ),
        )
        # Make sure that the price has not changed
        assert_that(new_msg.price(), equal_to(old_price))
        print(f"new_msg.executed_quantity(): {new_msg.executed_quantity()}")
        print(f"new_msg.remaining_quantity(): {new_msg.remaining_quantity()}")
        print(f"selected_order._quantity: {selected_order._quantity}")
        assert_that(
            new_msg.executed_quantity() + new_msg.remaining_quantity(),
            equal_to(selected_order._quantity),
        )

    @patch("pitch.generator.Generator._pickRandomOrder")
    @patch("pitch.generator.Generator._pickRandomMessageFromCategory")
    def test_getNextMsg_Edit_ReduceSizeLong(self, pick_rand_msg, pick_rand_ord):
        # GIVEN
        pick_rand_msg.return_value = ReduceSizeLong
        ticker = "NVDA"
        side = Side.Buy
        price_range = (50, 100)
        size_range = (25, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=4,
            seed=9900,
        )
        selected_order = gen._orderbook.get_orders(ticker=ticker, side=side)[0]
        pick_rand_ord.return_value = selected_order
        old_price = selected_order._price
        old_size = selected_order._quantity

        # WHEN
        print("\n-- Edit Order Test --")
        print(f"selected_order: ({selected_order})")
        # print('-- Order Book Before --')
        # gen.print_OrderBook(ticker=ticker)
        # Mock out call to pick a random message type based on the passed
        # in category
        new_msg = gen._getNextMsg(
            ticker=ticker,
            side=side,
            new_timestamp=gen._pickTimeOffset(),
            new_msg_cat=Generator.MsgType.Edit,
        )

        # print(f'Modify Message: {new_msg}')
        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Edit]))
        assert_that(new_msg, instance_of(ReduceSizeLong))

        print("-- Order Book Before --")
        gen._orderbook.print_order_book(ticker=ticker)
        # Check returned Order is correct
        print(f"new_msg.order_id(): {new_msg.order_id()}")
        print(f"selected_order._order_id: {selected_order._order_id}")
        assert_that(new_msg.order_id(), equal_to(selected_order._order_id))
        print(f"selected_order._quantity: {selected_order._quantity}")
        # 50 = 100 - <new size>
        assert_that(
            new_msg.canceled_quantity(), equal_to(old_size - selected_order._quantity)
        )

    @patch("pitch.generator.Generator._pickRandomOrder")
    @patch("pitch.generator.Generator._pickRandomMessageFromCategory")
    def test_getNextMsg_Delete_DeleteOrder(self, pick_rand_msg, pick_rand_ord):
        # GIVEN
        pick_rand_msg.return_value = DeleteOrder
        ticker = "NVDA"
        side = Side.Buy
        price_range = (50, 100)
        size_range = (25, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=4,
            seed=9900,
        )
        selected_order = gen._orderbook.get_orders(ticker=ticker, side=side)[0]
        pick_rand_ord.return_value = selected_order

        # WHEN
        print(f"Order selected to be deleted: ({selected_order})")
        new_msg = gen._getNextMsg(
            ticker=ticker,
            side=side,
            new_timestamp=gen._pickTimeOffset(),
            new_msg_cat=Generator.MsgType.Remove,
        )

        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Remove]))
        assert_that(new_msg, instance_of(DeleteOrder))
        assert_that(new_msg.order_id(), equal_to(selected_order._order_id))
        assert_that(gen._orderbook.get_orders(ticker=ticker, side=side), has_length(3))

    @patch("pitch.generator.Generator._pickRandomOrder")
    @patch("pitch.generator.Generator._pickRandomMessageFromCategory")
    def test_getNextMsg_Delete_TradeLong(self, pick_rand_msg, pick_rand_ord):
        # GIVEN
        pick_rand_msg.return_value = TradeLong
        ticker = "NVDA"
        side = Side.Buy
        price_range = (50, 100)
        size_range = (25, 100)
        gen = setupTest(
            ticker=ticker,
            side=side,
            book_size_range=(1, 3),
            price_range=price_range,
            size_range=size_range,
            num_orders=4,
            seed=9900,
        )
        selected_order = gen._orderbook.get_orders(ticker=ticker, side=side)[0]
        pick_rand_ord.return_value = selected_order

        # WHEN
        print(f"Order selected to be deleted: ({selected_order})")
        new_msg = gen._getNextMsg(
            ticker=ticker,
            side=side,
            new_timestamp=gen._pickTimeOffset(),
            new_msg_cat=Generator.MsgType.Remove,
        )

        # THEN
        assert_that(type(new_msg), is_in(gen._msgTypes[Generator.MsgType.Remove]))
        assert_that(new_msg, instance_of(TradeLong))
        assert_that(new_msg.order_id(), equal_to(selected_order._order_id))
        assert_that(gen._orderbook.get_orders(ticker=ticker, side=side), has_length(3))
