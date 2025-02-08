import argparse
import logging
import sys
from typing import Any

from .file_parser import FileParser
from .util import get_line, get_form

sep_len = 89


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="PITCH.Parser",
        description="PITCH Message Parser",
        epilog="Bottom of help text",
    )
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Verbose"
    )
    parser.add_argument(
        "-d", "--debug", default=False, action="store_true", help="Debug"
    )
    parser.add_argument(
        "-b",
        "--binary-file",
        required=True,
        action="store",
        type=str,
        help="Config File",
    )
    parser.add_argument(
        "-i",
        "--ip",
        action="store",
        type=str,
        default="10.0.1.14",
        help="Destination IP",
    )
    parser.add_argument(
        "-p",
        "--dest-port",
        action="store",
        type=int,
        default=8000,
        help="Destination Port",
    )
    return parser.parse_args()


def set_up_logging(verbose: bool, debug: bool) -> None:
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

    logger.setLevel(logging.DEBUG)


def main():
    args = parse_args()
    dst_ip = args.ip
    dst_port = args.dest_port

    set_up_logging(verbose=args.verbose, debug=args.debug)

    logger = logging.getLogger(__name__)

    logger.warn(get_line("-", "+"))
    logger.warn(get_form(f"Parsing: {args.binary_file}"))
    logger.warn(get_line("-", "+"))
    logger.warn(get_form(f"IP Address: {dst_ip}"))
    logger.warn(get_form(f"Port: {dst_port}"))
    logger.warn(get_line(" ", "|"))
    logger.warn(get_line("-", "+"))

    seq_array = FileParser.parse_pcap(file_path=args.binary_file,
                                      dst_ip=dst_ip,
                                      dport=dst_port)

    logger.warn(get_line("-", "+"))
    logger.warn(get_form("Parsed BATS messages:"))
    for seq_idx, seq in enumerate(seq_array):
        logger.warn(get_line("-", "+"))
        logger.warn(get_form(f"[{seq_idx}] SeqUnitHdr: {seq}"))
        for msg_idx, msg in enumerate(seq.getMessages()):
            logger.warn(get_form(f"    - [{msg_idx}] {msg}"))

    logger.warn(get_line("-", "+"))


if __file__ == "__main__":
    main()
