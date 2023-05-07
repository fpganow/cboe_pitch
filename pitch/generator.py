from datetime import datetime, timedelta
from typing import List, Tuple
import numpy as np
import random

from pitch.add_order import AddOrderLong, AddOrderShort, AddOrderExpanded
from pitch.order_executed import OrderExecuted, OrderExecutedAtPriceSize
from pitch.reduce_size import ReduceSizeLong, ReduceSizeShort


class Generator(object):
    """ """

    def __init__(
        self,
        watch_list: List[Tuple[str, float]],
        rate: int = 10_000,
        start_time: datetime=None,
        total_time: int = 60,
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
        """
        self._watchList = [x for x, _ in watch_list]
        self._weights = [y for _, y in watch_list]

        self._rate = 1 / (rate / 3_600)
        if start_time is None:
            start_time = datetime.now()
        self._start_time = start_time
        self._current_time = start_time

        # Message Types
        self._msgTypes = []

        self._totalTime = total_time
        np.random.seed(seed)

        # print(f'self._watchList: {self._watchList}')
        # print(f'self._weights: {self._weights}')

    #TODO: Accept one bigger parameter
    #  unpack into list1, weights
    def rchoose(self, list1, weights):
        """
        list1   :    list of elements you're picking from.
        weights :    list of weights. Has to be in the same order as the
                     elements of list1. It can be given as the number of counts
                     or as a probability.
        """

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
            return self._watchList[0]
        elif len(self._watchList) == 0:
            return None
        return self.rchoose(self._watchList, self._weights)

    def _pickTime(self):
        next_time = self._current_time
        self._current_time = self._current_time + timedelta(seconds=self._rate)
        return next_time

    def _pickMsgType(self):
        all_add_msg_types = [AddOrderLong, AddOrderShort, AddOrderExpanded]
        return type(AddOrderLong)


    def getNext(self):
        """
        1 - Select a ticker
        2 - Select message time
        3 - Select message type
        4 - Track changes to internal state
        5 - Return
        """
        # 1 - Select a ticker
        ticker = self._pickTicker()
        # 2 - Get message time
        new_timestamp = self._pickTime()
        # 3 - Message type
        #  - Should take into account current OrderBook for selected Symbol
        new_msg_type = self._pickMsgType()
