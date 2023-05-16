from datetime import datetime, timedelta
from typing import List, Tuple
from enum import auto, Enum
import numpy as np
import random

from .add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from .delete_order import DeleteOrder
from .modify import ModifyOrderShort, ModifyOrderLong
from .order_executed import OrderExecuted, OrderExecutedAtPriceSize
from .reduce_size import ReduceSizeLong, ReduceSizeShort
from .trade import TradeLong, TradeShort, TradeExpanded


class Generator(object):
    """ """
    class MsgType(Enum):
        Add = 1
        Edit = 2
        Remove = 3
    class Side(Enum):
        Buy = 1
        Sell = 2

    def __init__(
        self,
        watch_list: List[Tuple[str, float]],
        rate: int = 10_000,
        start_time: datetime = None,
        total_time: int = 60,
        book_size_range: Tuple[int, int] = None,
        price_range: Tuple[float, float] = None,
        seed=None,
    ):
        """
        parameters:
            watch_list
                Array of tuples of symbol, weight pairs.
                i.e.

                to specify that 40% of all generated messages are
                related to AAPL, and 60% TSLA:

                    [ ('AAPL', .40), ('TSLA', .60) ]

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
        # Watch List [ (<ticker>, <weight>), ... ]
        self._watchList = watch_list

        # Rate <number of messages> / <per hour>
        self._rate = 1 / (rate / 3_600)

        # Start Time - Time of first message
        if start_time is None:
            start_time = datetime.now()
        self._start_time = start_time
        # Current Time - Keep track of time for next message
        self._current_time = start_time

        # Optimal Book Size
        if book_size_range is None:
            book_size_range = (10, 20)
        self._book_size_range = book_size_range

        if price_range is None:
            price_range = (55.00, 2.00)
        self._price_range = price_range
        # Message Types
        self._msgTypes = {
                Generator.MsgType.Add: {
                    AddOrderLong,
                    AddOrderShort,
                    AddOrderExpanded
                },
                Generator.MsgType.Edit: {
                    ModifyOrderShort,
                    ModifyOrderLong,
                    OrderExecutedAtPriceSize,
                    ReduceSizeShort,
                    ReduceSizeLong
                },
                Generator.MsgType.Remove: {
                    DeleteOrder,
                    OrderExecuted,
                    OrderExecutedAtPriceSize,
                    TradeShort,
                    TradeLong,
                    TradeExpanded
                }
        }

        # Total time to generate messages for
        self._totalTime = total_time

        # Seed the random number generator to facilitate easier testing
        np.random.seed(seed)
        self._rng = np.random.default_rng(seed)

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
        # Get a random number
        # Number of tickers
        if len(self._watchList) == 1:
            return self._watchList[0][0]
        elif len(self._watchList) == 0:
            return None
        return self.rchoose(self._watchList)

    def _pickSide(self):
        # rng -> I typed ngr
        if self._rng.integers(low=0, high=2) == 0:
            return Generator.Side.Buy
        return Generator.Side.Sell

    def _pickTime(self):
        next_time = self._current_time
        self._current_time = self._current_time + timedelta(seconds=self._rate)
        return next_time

    def _pickRandom(self, in_list):
        list_len = len(in_list)
        rand_idx = self._rng.integers(low=0, high=list_len)
        return in_list[rand_idx]

    def _pickMsgType(self, ticker: str, side: 'Generator.Side'):
        if ticker not in self._orderBook:
            self._orderBook[ticker] = {
                Generator.Side.Buy: [],
                Generator.Side.Sell: []
            }
        msg_type_univ = None
        # Is book too small?
        if len(self._orderBook[ticker][side]) < self._book_size_range[0]:
            # We want an Add
            print(f'ADD')
            msg_type_univ = self._msgTypes[Generator.MsgType.Add]
        # Is book too big?
        elif len(self._orderBook[ticker][side]) > self._book_size_range[1]:
            # We want a Delete
            print(f'DELETE')
            msg_type_univ = self._msgTypes[Generator.MsgType.Remove]
        else:
            # Else - randomly choose before
            print(f'ELSE')
            rnd_num = self._rng.integers(low=1, high=3)
            if rnd_num == 1:
                msg_type_univ = self._msgTypes[Generator.MsgType.Add]
            elif rnd_num == 2:
                msg_type_univ = self._msgTypes[Generator.MsgType.Edit]
            elif rnd_num == 3:
                msg_type_univ = self._msgTypes[Generator.MsgType.Remove]
            else:
                raise Exception('Error generating a random number')
        return self._pickRandom(list(msg_type_univ))

    def _pickSizeAndPrice(self, ticker, side, new_timestamp, new_msg_type):
        # ModifyOrderShort,
        # ModifyOrderLong,
        # OrderExecutedAtPriceSize,
        # ReduceSizeShort,
        # ReduceSizeLong
        pass

    def getNextMsg(self):
        """
        """
        # 1 - Pick Ticker
        ticker = self._pickTicker()
        # 2 - Pick Side
        side = self._pickSide()
        # 3 - Pick Message Time
        new_timestamp = self._pickTime()
        # 4 - Pick Message type
        #  - Should take into account current OrderBook for selected Symbol
        new_msg_type = self._pickMsgType()
        # 5 - Pick Price and Size
        new_ord_price_size = self._pickSizeAndPrice()
