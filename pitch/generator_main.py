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
        "-n", "--num-of-msgs", default=10, help="Number of Messages to Generate"
    )
    parser.add_argument(
        "-o", "--output-file", default="pitch24.dat", help="Specify output file"
    )

    return parser.parse_args()


def set_up_logging(audit_log: str, verbose: bool) -> None:
    logger = logging.getLogger(__name__)

    # Create handlers
    stream_handler = logging.StreamHandler()
    if verbose:
        print(f'verbose: {verbose}')
        stream_handler.setLevel(logging.DEBUG)
    else:
        stream_handler.setLevel(logging.INFO)

    stream_format = logging.Formatter('%(message)s')
    stream_handler.setFormatter(stream_format)

    file_handler = logging.FileHandler(audit_log, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(message)s')
    file_handler.setFormatter(file_format)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)


def main():
    args = parse_args()

    set_up_logging(audit_log="audit.log", verbose=args.verbose)

    logger = logging.getLogger(__name__)

    # Set these variables from argument
    ticker = "MSFT"
    weight = 0.50
    num_of_msgs = 10
    book_size_range = (1, 3)
    msg_rate_p_sec = 5
    verbose = args.verbose

    # Write everything to DEBUG
    # Write what I want to see on stdout to INFO
    start_time = datetime.now()
    # print(f'Start time: {start_time}')

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
    )
    sep_len = 89
    logger.debug(get_line("=", "=", sep_len))
    logger.debug(get_line("=", "=", sep_len))

    logger.debug("Initial Order Book\n")
    logger.debug(generator._orderbook.get_order_book(ticker))

    #f_ascii = open("orders.log", "w")
    f_bin = open("orders.dat", "wb")

    for i in range(num_of_msgs):
        logger.debug(get_line(" ", " "))
        logger.debug(get_line(" ", " "))
        new_msg = generator.getNextMsg()

        logger.debug(get_line("=", "=", sep_len))
        logger.info(get_line("=", "=", sep_len))
        logger.info(f"Message #{i+1}:    {new_msg}")
        new_msg_bytes = new_msg.get_bytes()
        new_msg_bytes_str = ", ".join(["0x" + str(x) for x in new_msg_bytes])
        logger.debug(f"bytes:\n\t{new_msg_bytes_str}")

        logger.debug(f"{str(new_msg)}\n")
        f_bin.write(new_msg.get_bytes())

        logger.debug(get_line(" ", " "))
        logger.debug(generator._orderbook.get_order_book(ticker))

    #f_ascii.close()
    f_bin.close()

    #logger.info(get_line(" ", " "))
    #logger.info(get_line(" ", " "))
    logger.info(get_line("=", "=", sep_len))
    logger.info(get_form("Final OrderBook"))
    logger.info(get_line("=", "=", sep_len))
    logger.info(get_line(" ", " "))
    logger.info(get_line(" ", " "))
    logger.info(generator._orderbook.get_order_book(ticker))
    logger.info(get_line(" ", " "))
    logger.info(get_line(" ", " "))
    logger.info(get_line("=", "=", sep_len))


if __file__ == "__main__":
    main()
