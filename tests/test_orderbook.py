from unittest import TestCase

from hamcrest import assert_that, has_length, has_item, equal_to

from pitch.orderbook import OrderBook, Side


class TestOrderBook(TestCase):
    def test_smoke(self):
        # WHEN
        ob = OrderBook()

        # THEN
        assert_that(ob.tickers(), has_length(0))

    def test_add_ticker(self):
        # GIVEN
        ticker = "NATI"

        # WHEN
        ob = OrderBook()
        ob.add_ticker(ticker=ticker)

        # THEN
        assert_that(ob.tickers(), has_length(1))
        assert_that(ob.tickers(), has_item(ticker))
        assert_that(ob.has_ticker(ticker=ticker), equal_to(True))

    def test_add_order(self):
        # GIVEN
        ticker = "GE"
        side = Side.Buy

        # WHEN
        ob = OrderBook()
        ob.add_ticker(ticker=ticker)
        ob.add_order(
            ticker=ticker, side=side, price=52.25, quantity=100, order_id="ORID0001"
        )

        # THEN
        assert_that(
            ob.has_order_id(ticker=ticker, side=side, order_id="ORID0001"),
            equal_to(True),
        )
        assert_that(ob.get_orders(ticker=ticker, side=side), has_length(1))

    def test_add_multiple_buy_orders(self):
        # GIVEN
        ticker = "XOM"
        side = Side.Buy

        # WHEN
        ob = OrderBook()
        ob.add_ticker(ticker=ticker)
        ob.add_order(
            ticker=ticker, side=side, price=52.25, quantity=100, order_id="ORID0001"
        )
        ob.add_order(
            ticker=ticker, side=side, price=52.50, quantity=300, order_id="ORID0002"
        )
        ob.add_order(
            ticker=ticker, side=side, price=52.75, quantity=200, order_id="ORID0003"
        )

        # THEN
        assert_that(
            ob.has_order_id(ticker=ticker, side=side, order_id="ORID0001"),
            equal_to(True),
        )
        assert_that(
            ob.has_order_id(ticker=ticker, side=side, order_id="ORID0002"),
            equal_to(True),
        )
        assert_that(
            ob.has_order_id(ticker=ticker, side=side, order_id="ORID0003"),
            equal_to(True),
        )

        buy_orders = ob.get_orders(ticker=ticker, side=side)
        assert_that(buy_orders, has_length(3))
        assert_that(buy_orders[0].order_id, equal_to("ORID0003"))
        assert_that(buy_orders[0].price, equal_to(52.75))
        assert_that(buy_orders[1].order_id, equal_to("ORID0002"))
        assert_that(buy_orders[2].order_id, equal_to("ORID0001"))

    def test_delete_order(self):
        # GIVEN
        ticker = "AAPL"
        side = Side.Sell

        # WHEN
        ob = OrderBook()
        ob.add_ticker(ticker=ticker)
        ob.add_order(
            ticker=ticker, side=side, price=52.25, quantity=100, order_id="ORID0001"
        )
        ob.add_order(
            ticker=ticker, side=side, price=52.50, quantity=300, order_id="ORID0002"
        )
        ob.add_order(
            ticker=ticker, side=side, price=52.75, quantity=200, order_id="ORID0003"
        )
        ob.delete_order(ticker=ticker, side=side, order_id="ORID0002")

        # THEN
        assert_that(
            ob.has_order_id(ticker=ticker, side=side, order_id="ORID0001"),
            equal_to(True),
        )
        assert_that(
            ob.has_order_id(ticker=ticker, side=side, order_id="ORID0002"),
            equal_to(False),
        )
        assert_that(
            ob.has_order_id(ticker=ticker, side=side, order_id="ORID0003"),
            equal_to(True),
        )

        buy_orders = ob.get_orders(ticker=ticker, side=side)
        assert_that(buy_orders, has_length(2))
