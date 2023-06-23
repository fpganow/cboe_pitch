from enum import Enum
from typing import List
from .util import get_line, get_line_ln, print_line, get_form, get_form_ln, print_form


class Side(Enum):
    Buy = "B"
    Sell = "S"


class Order:
    def __init__(self, ticker, side, price, quantity, order_id):
        self._ticker = ticker
        self._side = side
        self._price = price
        self._quantity = quantity
        self._order_id = order_id

    @property
    def ticker(self):
        return self._ticker

    @property
    def price(self):
        return self._price

    @property
    def side(self):
        return self._side

    @property
    def quantity(self):
        return self._quantity

    @property
    def order_id(self):
        return self._order_id

    def __str__(self):
        return f"{self._ticker}, [{self._order_id}] {self._price} X {self._quantity}"


class OrderBook:
    """
    Order Book abstraction to track buy and sell orders
    by Ticker/Symbol.
    """

    def __init__(self):
        self._orderbook = {}

    def tickers(self) -> List[str]:
        return list(self._orderbook.keys())

    def add_ticker(self, ticker: str) -> None:
        if ticker not in self._orderbook:
            self._orderbook[ticker] = {Side.Buy: [], Side.Sell: []}

    def has_ticker(self, ticker: str) -> bool:
        return ticker in self._orderbook

    def add_order(
        self, ticker: str, side: Side, price: float, quantity: int, order_id: str
    ):
        order_list = self._orderbook[ticker][side]
        # Check if order already exists
        if self.has_order_id(ticker=ticker, side=side, order_id=order_id):
            raise Exception(
                f"Order with ID {order_id} for {ticker}-{side} already exists"
            )

        # Add Order
        order_list.append(
            Order(
                ticker=ticker,
                side=side,
                price=price,
                quantity=quantity,
                order_id=order_id,
            )
        )
        # Sort Orders
        self._sort_orders(ticker=ticker, side=side)

    def has_order_id(self, ticker: str, side: Side, order_id: str) -> bool:
        order_list = self._orderbook[ticker][side]
        for order in order_list:
            if order.order_id == order_id:
                return True
        return False

    def delete_order(self, ticker: str, side: Side, order_id: str):
        for order in self._orderbook[ticker][side]:
            if order.order_id == order_id:
                self._orderbook[ticker][side].remove(order)
                break

    def _sort_orders(self, ticker: str, side: Side) -> None:
        if side == Side.Buy:
            self._orderbook[ticker][Side.Buy].sort(key=lambda x: x.price, reverse=True)
        elif side == Side.Sell:
            self._orderbook[ticker][Side.Sell].sort(key=lambda x: x.price)

    def get_orders(self, ticker: str, side: Side) -> List[Order]:
        # Sort Orders
        self._sort_orders(ticker=ticker, side=Side.Buy)
        # Return Orders
        return self._orderbook[ticker][side]

    def print_order_book(self, ticker: str):
        print(get_order_book(ticker))

    def get_order_book(self, ticker: str) -> str:
        ss = ""
        display_width = 60

        ss += get_line_ln("-", "+")
        ss += get_form_ln(f"OrderBook for {ticker}")
        ss += get_line_ln("-", "+")

        buy_orders = self.get_orders(ticker=ticker, side=Side.Buy)
        if len(buy_orders) == 0:
            ss += get_line_ln(" ", "|")
            no_buys_msg = "No Buy Orders"
            ss += get_form_ln(f"{no_buys_msg}")
            ss += get_line_ln(" ", "|")
            ss += get_line_ln("-", "+")
        else:
            for buy in buy_orders:
                padding_len = display_width - len(str(buy)) - 8
                padding = " " * padding_len
                ss += get_form_ln(f"Buy: {buy}")
            ss += get_line_ln("-", "+")

        sell_orders = self.get_orders(ticker=ticker, side=Side.Sell)
        if len(sell_orders) == 0:
            no_sells_msg = "No Sell Orders"
            ss += get_line_ln(" ", "|")
            ss += get_form_ln(f"{no_sells_msg}")
            ss += get_line_ln(" ", "|")
            ss += get_line_ln("-", "+")
        else:
            for sell in sell_orders:
                padding_len = display_width - len(str(sell)) - 8
                padding = " " * padding_len
                ss += get_form_ln(f"Sell: {sell}")
            ss += get_line_ln("-", "+")

        return ss[:-1]
