#
# TODO:
#  - Find bug when trying to encode 'Side'
#     pitch24.py line 87

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from .generator import Generator, WatchListItem
from .seq_unit_header import SequencedUnitHeader
from .config import Config
from .util import get_line, get_form

sep_len = 89


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="PITCH.Generator",
        description="PITCH Message Generator",
        epilog="Bottom of help text",
    )
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Verbose"
    )
    parser.add_argument(
        "-d", "--debug", default=False, action="store_true", help="Debug"
    )
    parser.add_argument(
        "-c", "--config", required=True, action="store", type=str, help="Config File"
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
        print(f"verbose: {verbose}")
        stream_handler.setLevel(logging.INFO)
    else:
        stream_handler.setLevel(logging.WARN)

    stream_format = logging.Formatter("%(message)s")
    stream_handler.setFormatter(stream_format)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(audit_log, mode="w")
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter("%(message)s")
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    if debug:
        print(f"debug: {debug}")
        trace_handler = logging.FileHandler(trace_log, mode="w")
        trace_format = logging.Formatter("%(message)s")
        trace_handler.setFormatter(trace_format)
        trace_handler.setLevel(logging.DEBUG)
        logger.addHandler(trace_handler)

    logger.setLevel(logging.DEBUG)


def main():
    args = parse_args()

    if Path(args.config).exists() is False:
        print(f"config: {args.config} does not exist", file=sys.stderr)
        return -1

    # Set these variables from argument
    config = Config(file=args.config)

    set_up_logging(
        audit_log=config.audit_log_file(),
        trace_log=config.trace_log_file(),
        verbose=args.verbose,
        debug=args.debug,
    )

    logger = logging.getLogger(__name__)

    logger.warn(get_line("=", "="))
    logger.warn(get_form("Configuration:"))
    logger.warn(get_line("-", "+"))

    num_of_msgs = 10
    seq_unit_hdr_len = config.seq_unit_hdr_len()

    # Write everything to DEBUG
    # Write what I want to see on stdout to INFO
    start_time = datetime.now().replace(microsecond=0)
    logger.info(get_form(f"Start time: {start_time}"))
    logger.info(get_line("-", "+"))

    watch_list = []
    logger.warn(get_form("Reading watch list..."))
    for ticker, val in config.watch_list().items():
        watch_list.append(
            WatchListItem(
                ticker=ticker,
                weight=val["weight"],
                book_size_range=val["book_size"],
                price_range=val["price_range"],
                size_range=val["size_range"],
            )
        )
        logger.warn(get_form(f" + {watch_list[-1]}"))
    logger.warn(get_line("-", "+"))

    generator = Generator(
        watch_list=watch_list,
        msg_rate_p_sec=config.msg_rate_p_sec(),
        start_time=start_time,
        seed=1_000,
    )

    logger.info("")
    logger.info(get_line("=", "="))
    logger.info("Initial Order Book")
    logger.info(get_line("=", "="))
    logger.info("")
    logger.info(generator._orderbook.get_order_book(ticker))

    # Generate Messages
    msg_count = 0
    seq_unit_array = []
    seq_unit_hdr = SequencedUnitHeader(hdr_sequence=1)
    while msg_count < num_of_msgs:
        new_msg = generator.getNextMsg()
        if new_msg is None:
            continue
        # logger.warn(f'New message: {new_msg}')
        msg_count += 1

        if (seq_unit_hdr.getLength() + new_msg.length()) <= seq_unit_hdr_len:
            seq_unit_hdr.addMessage(new_msg)
        else:
            seq_unit_array.append(seq_unit_hdr)
            seq_unit_hdr = SequencedUnitHeader(
                hdr_sequence=seq_unit_hdr.getNextSequence()
            )
            seq_unit_hdr.addMessage(new_msg)
    if seq_unit_hdr.hdr_count() > 0:
        seq_unit_array.append(seq_unit_hdr)

    # Write Generated Messages
    # TODO: Write out messages in binary format
    #       and echo to screen
    #       and for trace show orderbook
    f_bin = open(config.output_file(), "wb")

    for seq_unit_hdr in seq_unit_array:
        logger.info(get_line(" ", " "))
        logger.info(get_line(" ", " "))

        # Print Sequenced Unit Header info
        file_offset = f_bin.tell()
        print(f"Offset={str(hex(file_offset))}: {seq_unit_hdr}")

        # Write Sequenced Unit Header to file
        new_msg_bytes = seq_unit_hdr.get_bytes()
        new_msg_bytes_str = ", ".join([str(hex(x)) for x in new_msg_bytes])
        print(f"DEBUG: bytes: {new_msg_bytes_str}")
        f_bin.write(new_msg_bytes)

        for message in seq_unit_hdr.getMessages():
            # Print one-liner for each message in Sequenced Unit Header, including file offset
            file_offset = f_bin.tell()
            logger.warn(f"\t - Offset={str(hex(file_offset))}: {message}")
            # Print each message to file
            f_bin.write(message.get_bytes())

    f_bin.close()


#    for i in range(num_of_msgs):
#        logger.info(get_line(" ", " "))
#        logger.info(get_line(" ", " "))
#        new_msg = generator.getNextMsg()
#
#        logger.info(get_line("=", "=", sep_len))
#        logger.warn(get_line("=", "=", sep_len))
#        logger.warn(f"Message #{i+1}:    {new_msg}")
#        new_msg_bytes = new_msg.get_bytes()
#        new_msg_bytes_str = ", ".join(["0x" + str(x) for x in new_msg_bytes])
#        logger.info(f"bytes:\n\t{new_msg_bytes_str}")
#
#        logger.info(f"{str(new_msg)}\n")
#        f_bin.write(new_msg.get_bytes())
#
#        logger.info(get_line(" ", " "))
#        logger.info(generator._orderbook.get_order_book(ticker))
#
#    logger.warn(get_line("-", "+"))
#    logger.warn(get_form("Final OrderBook"))
#    logger.warn(get_line("-", "+"))
#
#    logger.warn(get_line(" ", "|"))
#    logger.warn(get_line(" ", "|"))
#    logger.warn(generator._orderbook.get_order_book(ticker))
#    logger.warn(get_line(" ", "|"))
#    logger.warn(get_line(" ", "|"))
#    logger.warn(get_line("-", "+"))
#    logger.warn(get_form("Statistics"))
#    logger.warn(get_line("-", "+"))
#    logger.warn(get_line(" ", "|"))
#    logger.warn(get_line(" ", "|"))
#    # TODO: Print statistics on types of messages, to be used by parser
#    #       as a sanity check
#    #logger.warn(get_form(" - Total Number of Messages: 10"))
#    #logger.warn(get_form(" - # of AddOrderShort: 10"))
#    logger.warn(get_line(" ", "|"))
#    logger.warn(get_line("-", "+"))


if __file__ == "__main__":
    main()
