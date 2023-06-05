from datetime import datetime, timedelta
from typing import List, Tuple, Any
from enum import Enum
import numpy as np
from numpy import ndarray

from .add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from .delete_order import DeleteOrder
from .modify import ModifyOrderShort, ModifyOrderLong
from .order_executed import OrderExecuted, OrderExecutedAtPriceSize
from .reduce_size import ReduceSizeLong, ReduceSizeShort
from .trade import TradeLong, TradeShort, TradeExpanded


class WatchListItem:
    def __init__(self,
                 ticker: str,
                 weight: float,
                 book_size_range: Tuple[int, int] = None,
                 price_range: Tuple[float, float] = None,
                 size_range: Tuple[float, float] = None) -> object:
        self._ticker = ticker
        self._weight = weight

        # Optimal Book Size
        if book_size_range is None:
            book_size_range = (10, 20)
        self._book_size_range = book_size_range

        if price_range is None:
            price_range = (55.00, 75.00)
        self._price_range = price_range

        if size_range is None:
            size_range = (25, 300)
        self._size_range = size_range

    @property
    def ticker(self):
        return self._ticker

    @property
    def weight(self):
        return self._weight

    @property
    def book_size_range(self):
        return self._book_size_range

    @property
    def price_range(self):
        return self._price_range

    @property
    def size_range(self):
        return self._size_range


class Generator(object):
    """ """

    class MsgType(Enum):
        Add = 1
        Edit = 2
        Remove = 3

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

        def __str__(self):
            return f'{self._ticker}, [{self._order_id}] {self._price} X {self._quantity}'

    def __init__(
            self,
            watch_list: List[WatchListItem],
            msg_rate_p_sec: int = 10_000,
            start_time: datetime = None,
            total_time_s: int = 60,
            seed=None,
    ):
        """
        parameters:
            watch_list
                Array of tuples of symbol, weight pairs.
                i.e.

                to specify that 40% of all generated messages are
                related to AAPL, and 60% TSLA:

                    [ (<ticker>, <weight>,
                       (<min_book_size>, <max_book_size>),
                       (<min_price>, <max_price>),
                       (<min_size>, <max_size>)
                       )

            rate
                Rate in number of messages per hour
                i.e.

                to generate 50,000 messages per hour:
                    50_000

            total_time:
                Total amount of time to generate messages for
                i.e.

                to generate messages over the span of 5 minutes:
                    300

            book_size_range: Tuple[int, int]
                Size or number of orders that should exist in the orderbook
                at any given time.  If the orderbook goes outside of this
                range, a Delete or Order Execution will be sent to decrease
                the size to be within this range.

                Defaults to [10, 20]
                That is, an order book where each side has between 10 and 20 orders.

            price_range: Tuple[float, float]
                Price, one standard deviation
                Target price, and the size of one standard deviation
        """
        if len(watch_list) == 0:
            raise Exception('WatchList size == 0')
        self._watch_list = {}
        for watch_list_item in watch_list:
            self._watch_list[watch_list_item.ticker] = {
                Generator.Side.Buy: watch_list_item,
                Generator.Side.Sell: watch_list_item,
            }

            # Rate <number of messages> / <per second>
        self._msg_rate_p_sec = msg_rate_p_sec

        # Start Time - Time of first message
        # Current Time - Keep track of time for next message
        if start_time is None:
            start_time = datetime.now()
        self._current_time = start_time

        # Seed the random number generator to facilitate easier testing
        np.random.seed(seed)
        self._rng = np.random.default_rng(seed)

        # Initialize OrderBook for each ticker in watch_list
        self._order_book = {}
        for ticker, watch_list_item in self._watch_list.items():
            self._order_book[ticker] = {
                Generator.Side.Buy: watch_list_item,
                Generator.Side.Sell: watch_list_item
            }

        # Set 1st Order Id
        self._nextOrderNum = 0

        # Set 1st Execution Id
        self._nextExecutionId = 0

        # Size increment
        self._increment = 25

        # Message Types
        self._msgTypes = {
            Generator.MsgType.Add: {
                AddOrderLong,
                AddOrderShort,
                AddOrderExpanded
            },
            Generator.MsgType.Edit: {
                ModifyOrderLong,
                ModifyOrderShort,
                OrderExecutedAtPriceSize,
                ReduceSizeLong,
                ReduceSizeShort,
            },
            Generator.MsgType.Remove: {
                DeleteOrder,
                OrderExecuted,
                OrderExecutedAtPriceSize,
                TradeLong,
                TradeShort,
                TradeExpanded
            }
        }
        return

        # Total time to generate messages for
        self._totalTime = total_time_s

        # Internal variable for tracking Order message creation (an orderbook)
        self._orderBook = {}

    def rchoose(self, in_list):
        """
        list1   :    list of elements you're picking from.
        weights :    list of weights. Has to be in the same order as the
                     elements of list1. It can be given as the number of counts
                     or as a probability.
        """

        list1 = [x for x, _ in in_list]
        weights = [y for _, y in in_list]

        # normalizing the weights list
        w_sum = sum(weights)
        weights_normalized = []
        for w in weights:
            weights_normalized.append(w / w_sum)

        # sorting the normalized weights and the desired list simultaneously
        weights_normalized, list1 = zip(*sorted(zip(weights_normalized, list1)))

        # bringing the sorted tuples back to being lists
        weights_normalized = list(weights_normalized)
        list1 = list(list1)

        # finalizing the weight normalization
        dummy = []
        count = 0
        for item in weights_normalized:
            count += item
            dummy.append(count)
        weights_normalized = dummy

        # testing which interval the uniform random number falls in
        random_number = np.random.uniform(0, 1)
        print(f"random_number: {random_number}")
        for idx, w in enumerate(weights_normalized[:-1]):
            if random_number <= w:
                return list1[idx]
        return list1[-1]

    def _pickTicker(self):
        if len(self._watch_list.items()) == 1:
            return self._watch_list[list(self._watch_list.keys())[0]][Generator.Side.Buy].ticker
        return self.rchoose([(ticker, val[Generator.Side.Buy].weight) for ticker, val in self._watch_list.items()])

    def _pickSide(self):
        # rng -> I typed ngr
        if self._rng.integers(low=0, high=2) == 0:
            return Generator.Side.Buy
        return Generator.Side.Sell

    def _pickTime(self):
        next_time = self._current_time
        time_diff_ms = 1_000 // self._msg_rate_p_sec
        self._current_time = self._current_time + timedelta(milliseconds=time_diff_ms)
        return next_time

    def _pickRandomOrder(self, ticker: str, side: Side) -> Order:
        return self._pickRandom(self._order_book[ticker][side])

    def _pickRandom(self, in_list) -> Any:
        list_len = len(in_list)
        rand_idx = self._rng.integers(low=0, high=list_len)
        return in_list[rand_idx]

    def _pickMsgCategory(self, ticker: str, side: 'Generator.Side'):
        if ticker not in self._order_book:
            raise Exception(f'Invalid Ticker "{ticker}" (not in OrderBook)')

        # Is book too small?
        # if len(self._orderBook[ticker][side]) < self._book_size_range[0]:
        if len(self._order_book[ticker][side]) \
                < self._watch_list[ticker][side].book_size_range[0]:
            # We want an Add
            print(f'MsgType.Add')
            return Generator.MsgType.Add
        # Is book too big?
        elif len(self._order_book[ticker][side]) \
                > self._watch_list[ticker][side].book_size_range[1]:
            # We want a Delete
            print(f'MsgType.Delete')
            return Generator.MsgType.Remove
        else:
            # Else - randomly choose
            print(f'MsgType.Random')
            rnd_num = self._rng.integers(low=1, high=3)
            if rnd_num == 1:
                print(f'Generator.MsgType.Add')
                return Generator.MsgType.Add
            elif rnd_num == 2:
                print(f'Generator.MsgType.Edit')
                return Generator.MsgType.Edit
            elif rnd_num == 3:
                print(f'Generator.MsgType.Remove')
                return Generator.MsgType.Remove
            else:
                raise Exception('Error picking a random Message Category')

    def _pickNewPrice(self, price_range: Tuple[float, float],
                      old_price: float = None) -> float:
        if old_price is None:
            new_price = price_range[0] + (self._rng.random() *
                                          (price_range[1] - price_range[0]))
        else:
            new_price = old_price
            while old_price == new_price:
                new_price = price_range[0] + (self._rng.random() *
                                              (price_range[1] - price_range[0]))

        new_price = float(np.around(new_price, decimals=2))
        return new_price

    def _pickNewSize(self, size_range: Tuple[int, int],
                     old_size: int = None) -> int:
        if old_size is None:
            r_1 = self._rng.random()
            r_2 = (size_range[1] - size_range[0]) // self._increment
            r_idx = self._rng.integers(low=0, high=r_2 + 1)
            new_size = size_range[0] + (r_idx * self._increment)
        else:
            new_size = old_size
            while old_size == new_size:
                r_1 = self._rng.random()
                r_2 = (size_range[1] - size_range[0]) // self._increment
                r_idx = self._rng.integers(low=0, high=r_2 + 1)
                new_size = size_range[0] + (r_idx * self._increment)

        return new_size

    #    def _pickPriceSize(self, ticker, side) -> tuple[float, int]:
    #        size_range = self._watch_list[ticker][side].size_range
    #
    #        return new_price, new_size

    def _getNextOrderId(self) -> str:
        self._nextOrderNum += 1
        return f'ORID{self._nextOrderNum:04d}'

    def _getNextExecutionId(self) -> str:
        self._nextExecutionId += 1
        return f'EXID{self._nextExecutionId:04d}'

    #    def _updateOrderBook(self, msg_cat, next_msg):
    #        ticker = next_msg.symbol()
    #        side = Generator.Side.Buy if next_msg.side() == 'B' else Generator.Side.Sell
    #        print(f'Adding order: {ticker}-{side}')
    #        if msg_cat == Generator.MsgType.Add:
    #            self._orderBook[ticker][side].append(
    #                Generator.Order(ticker=ticker,
    #                                side=side,
    #                                price=next_msg.price(),
    #                                quantity=next_msg.quantity(),
    #                                order_id=next_msg.orderId()),
    #            )
    #        elif msg_cat == Generator.MsgType.Edit:
    #            pass
    #        elif msg_cat == Generator.MsgType.Remove:
    #            pass

    def _pickRandomMessageFromCategory(self, msg_cat):
        return self._pickRandom(list(self._msgTypes[msg_cat]))

    def _getNextMsg(self, ticker: str, side: Side, new_timestamp, new_msg_cat):
        new_side = 'B' if side == Generator.Side.Buy else 'S'
        new_msg_type = self._pickRandomMessageFromCategory(msg_cat=new_msg_cat)
        new_order_id = self._getNextOrderId()

        if new_msg_cat == Generator.MsgType.Add:
            # print(f'Adding a new order via {new_msg_cat}')
            # (new_price, new_size) = self._pickPriceSize(ticker=ticker,
            #                                            side=side)
            new_price = self._pickNewPrice(price_range=self._watch_list[ticker][side].price_range)
            new_size = self._pickNewSize(size_range=self._watch_list[ticker][side].size_range)

            if new_msg_type == AddOrderLong:
                message = AddOrderLong.from_parms(
                    time_offset=new_timestamp,
                    order_id=new_order_id,
                    side=new_side,
                    quantity=new_size,
                    symbol=ticker,
                    price=new_price,
                )
                return message
            elif new_msg_type == AddOrderShort:
                message = AddOrderShort.from_parms(
                    time_offset=new_timestamp,
                    order_id=new_order_id,
                    side=new_side,
                    quantity=new_size,
                    symbol=ticker,
                    price=new_price,
                )
            elif new_msg_type == AddOrderExpanded:
                message = AddOrderExpanded.from_parms(
                    time_offset=new_timestamp,
                    order_id=new_order_id,
                    side=new_side,
                    quantity=new_size,
                    symbol=ticker,
                    price=new_price,
                    displayed=True,
                    participant_id="MPID",
                    customer_indicator="C",
                )
            # Update Order Book
            self._order_book[ticker][side].append(
                Generator.Order(ticker=ticker,
                                side=side,
                                price=message.price(),
                                quantity=message.quantity(),
                                order_id=message.order_id()),
            )
            return message
        elif new_msg_cat == Generator.MsgType.Edit:
            # Pick an existing order
            random_order = self._pickRandomOrder(ticker=ticker, side=side)

            if new_msg_type == ModifyOrderLong or new_msg_type == ModifyOrderShort:
                print('-' * 50)
                print(f'Modifying an existing order via ModifyOrderLong or ModifyOrderShort')

                # Pick a new Price for this Order
                print('-' * 50)
                print(f'price_range: {self._watch_list[ticker][side].price_range}')
                new_price = self._pickNewPrice(price_range=self._watch_list[ticker][side].price_range,
                                               old_price=random_order._price)
                print(f'new_price: {new_price}')

                # Pick a new Size for this Order
                print('-' * 50)
                print(f'size_range: {self._watch_list[ticker][side].size_range}')
                print(f'old_size: {random_order._quantity}')
                new_size = self._pickNewSize(size_range=self._watch_list[ticker][side].size_range,
                                             old_size=random_order._quantity)
                print(f'new_size: {new_size}')

                random_order._price = new_price
                random_order._quantity = new_size
                print('-' * 50)
                print(f'Modified Order: {random_order}')

                print('-' * 50)
                print('-- Order Book After --')
                self.print_OrderBook(ticker=ticker)
                if new_msg_type == ModifyOrderLong:
                    return ModifyOrderLong.from_parms(time_offset=1,
                                                      price=new_price,
                                                      quantity=new_size,
                                                      order_id=random_order._order_id
                                                      )
                elif new_msg_type == ModifyOrderShort:
                    return ModifyOrderShort.from_parms(time_offset=1,
                                                       price=new_price,
                                                       quantity=new_size,
                                                       order_id=random_order._order_id
                                                       )
            elif new_msg_type == OrderExecutedAtPriceSize:
                # Modify existing order 'random_order'
                # New size will always be smaller
                old_size = random_order._quantity
                print(f'Old size: {old_size}')
                # TODO: If random_order size is equal to the minimum size, pick another order
                #       if none exists, execute or delete the order (possible to call recursively)
                if old_size == self._watch_list[ticker][side].size_range[0]:
                    return None
                new_size_range = (self._watch_list[ticker][side].size_range[0], old_size)
                print(f'New Size range: {new_size_range}')
                new_size = self._pickNewSize(size_range=new_size_range, old_size=old_size)
                print(f'New size: {new_size}')
                return OrderExecutedAtPriceSize.from_parms(time_offset=1,
                                                           order_id=random_order._order_id,
                                                           price=random_order._price,
                                                           executed_quantity=old_size - new_size,
                                                           remaining_quantity=new_size,
                                                           execution_id=self._getNextExecutionId()
                                                           )
            elif new_msg_type == ReduceSizeLong or new_msg_type == ReduceSizeShort:
                # Reduce existing order 'random_order'
                # New size will always be smaller
                old_size = random_order._quantity
                print(f'Old size: {old_size}')
                # TODO: If random_order size is equal to the minimum size, pick another order
                #       if none exists, execute or delete the order (possible to call recursively)
                if old_size == self._watch_list[ticker][side].size_range[0]:
                    return None
                new_size_range = (self._watch_list[ticker][side].size_range[0], old_size)
                print(f'New Size range: {new_size_range}')
                new_size = self._pickNewSize(size_range=new_size_range, old_size=old_size)
                print(f'New size: {new_size}')
                if new_msg_type == ReduceSizeLong:
                    # TODO: Add a _getNextTimeOffset() function
                    return ReduceSizeLong.from_parms(time_offset=1,
                                                     order_id=random_order._order_id,
                                                     canceled_quantity=old_size - new_size)
                else:
                    return ReduceSizeShort.from_parms(time_offset=1,
                                                      order_id=random_order._order_id,
                                                      canceled_quantity=old_size - new_size)
            else:
                raise Exception(f'Unknown Edit Message Type {new_msg_type}')
        elif new_msg_cat == Generator.MsgType.Remove:
            print(f'Removing an existing order via {new_msg_cat}')
            if new_msg_type == DeleteOrder:
                pass
            elif new_msg_type == OrderExecuted:
                pass
            elif new_msg_type == OrderExecutedAtPriceSize:
                pass
            elif new_msg_type == TradeShort:
                pass
            elif new_msg_type == TradeLong:
                pass
            elif new_msg_type == TradeExpanded:
                pass
        else:
            raise Exception('Invalid msg_type')

    def getNextMsg(self):
        """
        """
        # 1 - Pick Ticker
        ticker = self._pickTicker()
        # 2 - Pick Side
        side = self._pickSide()
        # 3 - Pick Message Time
        new_timestamp = self._pickTime()
        # 4 - Pick Message Category
        new_msg_cat = self._pickMsgCategory(ticker=ticker, side=side)
        # 5 - Set Price and Size
        next_msg = self._getNextMsg(ticker=ticker,
                                    side=side,
                                    new_timestamp=new_timestamp,
                                    new_msg_cat=new_msg_cat)
        #        self._updateOrderBook(new_msg_cat, next_msg)

        # 6 - Return new order
        return next_msg

    def print_OrderBook(self, ticker: str):
        print(f'Dumping OrderBook for {ticker}')
        ob = self._order_book[ticker]
        buy_side = ob[Generator.Side.Buy]
        for buy in buy_side:
            print(f'\tbuy: {buy}')
