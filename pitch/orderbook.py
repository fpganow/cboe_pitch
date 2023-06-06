from enum import Enum
from typing import List


class Side(Enum):
    Buy = 'B'
    Sell = 'S'


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
        return f'{self._ticker}, [{self._order_id}] {self._price} X {self._quantity}'


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
            self._orderbook[ticker] = {
                Side.Buy: [],
                Side.Sell: []
            }

    def has_ticker(self, ticker: str) -> bool:
        return ticker in self._orderbook

    def add_order(self,
                  ticker: str,
                  side: Side,
                  price: float,
                  quantity: int,
                  order_id: str):
        order_list = self._orderbook[ticker][side]
        # Check if order already exists
        if self.has_order_id(ticker=ticker, side=side, order_id=order_id):
            raise Exception(f'Order with ID {order_id} for {ticker}-{side} already exists')

        # Add Order
        order_list.append(Order(ticker=ticker,
                             side=side,
                             price=price,
                             quantity=quantity,
                             order_id=order_id))
        # Sort Orders
        self._sort_orders(ticker=ticker, side=side)

    def has_order_id(self, ticker: str, side: Side, order_id: str) -> bool:
        order_list = self._orderbook[ticker][side]
        for order in order_list:
            if order.order_id == order_id:
                return True
        return False

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

    def print_OrderBook(self, ticker: str):
        print(f'Dumping OrderBook for {ticker}')
        ob = self._order_book[ticker]

        display_width = 60

        print("\t+" + '-'*display_width + "+")
        buy_side = ob[Generator.Side.Buy]
        for buy in buy_side:
            line_len = len(str(buy))
            print(f'\t| buy: {buy} |')

        print("\t+" + '-'*display_width + "+")
        sell_side = ob[Generator.Side.Sell]
        for sell in sell_side:
            line_len = len(str(sell))
            print(f'\t| sell: {sell} |')
        print("\t+" + '-'*display_width + "+")
