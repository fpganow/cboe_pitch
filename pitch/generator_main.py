import argparse
from datetime import datetime
import logging
from pitch.generator import Generator, WatchListItem
import sys
from typing import Any
from .util import print_line, print_form


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
#    else:
        #        stream_handler.setLevel(logging.INFO)
    stream_format = logging.Formatter('STDOUT:%(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(stream_format)

    file_handler = logging.FileHandler(audit_log)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('FILE:%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
#    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)

# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning("WARNING")
    logger.error("ERROR")
    logger.critical("CRITICAL")

def main():
    args = parse_args()

    print(f'args.verbose: {args.verbose}')
    set_up_logging(audit_log="audit.log", verbose=args.verbose)

#    logger = logging.getLogger(__name__)
#    logger.debug("DEBUG")
#    logger.error("ERROR")
#    logger.info("INFO")
#    logger.error("ERROR")
    return
    # Set these variables from argument
    ticker = "MSFT"
    weight = 0.50
    num_of_msgs = 10
    book_size_range = (1, 3)
    msg_rate_p_sec = 5
    verbose = args.verbose

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
    sep_len = 100
    if verbose:
        print_line("=", "=", sep_len)
        print_line("=", "=", sep_len)
        print("Initial Order Book\n")
        generator._orderbook.print_order_book(ticker)

    f_ascii = open("orders.log", "w")
    f_bin = open("orders.dat", "wb")

    for i in range(num_of_msgs):
        if verbose:
            print_line(" ", " ")
            print_line(" ", " ")
        new_msg = generator.getNextMsg()

        if verbose:
            print_line("=", "=", sep_len)
        print_line("=", "=", sep_len)
        print(f"Message #{i+1}:    {new_msg}")
        new_msg_bytes = new_msg.get_bytes()
        new_msg_bytes_str = ", ".join(["0x" + str(x) for x in new_msg_bytes])
        if verbose:
            print(f"bytes:\n\t{new_msg_bytes_str}")

        f_ascii.write(f"{str(new_msg)}\n")
        f_bin.write(new_msg.get_bytes())

        if verbose:
            print_line(" ", " ")
            generator._orderbook.print_order_book(ticker)

    f_ascii.close()
    f_bin.close()

    print_line(" ", " ")
    print_line(" ", " ")
    print_line("=", "=", sep_len)
    print("Final OrderBook")
    print_line("=", "=", sep_len)
    print_line(" ", " ")
    print_line(" ", " ")
    generator._orderbook.print_order_book(ticker)
    print_line(" ", " ")
    print_line(" ", " ")
    print_line("=", "=", sep_len)


if __file__ == "__main__":
    main()
