#
# TODO:
#  - Find bug when trying to encode 'Side'
#     pitch24.py line 87
#  - Add trace logging to Generator messages
#  - Add support for Sequenced Unit Header
#  - Generate binary file with binary BATS messages in orders.bin
#  - Add mode to read binary orders.data and output all messages in ASCII form

import argparse
from datetime import datetime
import logging
from pitch.generator import Generator, WatchListItem
import sys
from typing import Any
from .util import get_line, print_line, get_form, print_form


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="PITCH.Generator",
        description="PITCH Message Generator and Parser",
        epilog="Bottom of help text",
    )
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Verbose"
    )
    parser.add_argument(
        "-d", "--debug", default=False, action="store_true", help="Debug"
    )
    parser.add_argument(
        "-n", "--num-of-msgs", default=10, help="Number of Messages to Generate"
    )
    parser.add_argument(
        "-o", "--output-file", default="pitch24.bin", help="Specify output file"
    )

    return parser.parse_args()


def set_up_logging(audit_log: str, trace_log: str, verbose: bool, debug: bool) -> None:
    logger = logging.getLogger()

    # Create handlers
    stream_handler = logging.StreamHandler()
    if verbose:
        print(f'verbose: {verbose}')
        stream_handler.setLevel(logging.INFO)
    else:
        stream_handler.setLevel(logging.WARN)

    stream_format = logging.Formatter('%(message)s')
    stream_handler.setFormatter(stream_format)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(audit_log, mode='w')
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    if debug:
        print(f'debug: {debug}')
        trace_handler = logging.FileHandler(trace_log, mode='w')
        trace_format = logging.Formatter('%(message)s')
        trace_handler.setFormatter(trace_format)
        trace_handler.setLevel(logging.DEBUG)
        logger.addHandler(trace_handler)

    logger.setLevel(logging.DEBUG)


def main():
    args = parse_args()

    set_up_logging(audit_log="audit.log", trace_log='trace_log', verbose=args.verbose, debug=args.debug)

    logger = logging.getLogger(__name__)

    # Set these variables from argument
    ticker = "MSFT"
    weight = 0.50
    num_of_msgs = 10
    book_size_range = (1, 3)
    msg_rate_p_sec = 5
    verbose = args.verbose
    output_file = args.output_file

    # Write everything to DEBUG
    # Write what I want to see on stdout to INFO
    start_time = datetime.now()
    logger.info(f'Start time: {start_time}')

    watch_list = [
        WatchListItem(
            ticker=ticker,
            weight=weight,
            book_size_range=book_size_range,
            price_range=(50.00, 65.00),
            size_range=(25, 200),
        )
    ]
    generator = Generator(
        watch_list=watch_list,
        msg_rate_p_sec=msg_rate_p_sec,
        start_time=start_time,
        seed=1_000
    )
    sep_len = 89
    logger.info(get_line("=", "=", sep_len))
    logger.info(get_line("=", "=", sep_len))

    logger.info("Initial Order Book\n")
    logger.info(generator._orderbook.get_order_book(ticker))

    f_bin = open(output_file, "wb")

    for i in range(num_of_msgs):
        logger.info(get_line(" ", " "))
        logger.info(get_line(" ", " "))
        new_msg = generator.getNextMsg()

        logger.info(get_line("=", "=", sep_len))
        logger.warn(get_line("=", "=", sep_len))
        logger.warn(f"Message #{i+1}:    {new_msg}")
        new_msg_bytes = new_msg.get_bytes()
        new_msg_bytes_str = ", ".join(["0x" + str(x) for x in new_msg_bytes])
        logger.info(f"bytes:\n\t{new_msg_bytes_str}")

        logger.info(f"{str(new_msg)}\n")
        f_bin.write(new_msg.get_bytes())

        logger.info(get_line(" ", " "))
        logger.info(generator._orderbook.get_order_book(ticker))

    f_bin.close()

    logger.warn(get_line("-", "+"))
    logger.warn(get_form("Final OrderBook"))
    logger.warn(get_line("-", "+"))

    logger.warn(get_line(" ", "|"))
    logger.warn(get_line(" ", "|"))
    logger.warn(generator._orderbook.get_order_book(ticker))
    logger.warn(get_line(" ", "|"))
    logger.warn(get_line(" ", "|"))
    logger.warn(get_line("-", "+"))
    logger.warn(get_form("Statistics"))
    logger.warn(get_line("-", "+"))
    logger.warn(get_line(" ", "|"))
    logger.warn(get_line(" ", "|"))
    # TODO: Print statistics on types of messages, to be used by parser
    #       as a sanity check
    #logger.warn(get_form(" - Total Number of Messages: 10"))
    #logger.warn(get_form(" - # of AddOrderShort: 10"))
    logger.warn(get_line(" ", "|"))
    logger.warn(get_line("-", "+"))


if __file__ == "__main__":
    main()
