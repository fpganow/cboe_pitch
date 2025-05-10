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
    dport = args.dest_port

    set_up_logging(verbose=args.verbose, debug=args.debug)

    logger = logging.getLogger(__name__)

    logger.warn(get_line("-", "+"))
    logger.warn(get_form(f"Parsing: {args.binary_file}"))
    logger.warn(get_line("-", "+"))
    logger.warn(get_form(f"IP Address: {dst_ip}"))
    logger.warn(get_form(f"Port: {dport}"))
    logger.warn(get_line(" ", "|"))
    logger.warn(get_line("-", "+"))

    seq_array = FileParser.parse_pcap(file_path=args.binary_file,
                                      dst_ip=dst_ip,
                                      dport=dport)

    logger.warn(get_line("-", "+"))
    logger.warn(get_form("Parsed BATS messages:"))
    for seq_idx, seq in enumerate(seq_array):
        logger.warn(get_line("-", "+"))
        logger.warn(get_form(f'[{seq_idx}] {seq}, get_all_bytes length: {len(seq.get_all_bytes())}'))
        raw_bytes = seq.get_bytes()
        row_str_msb = ' '.join([f'{x:02x}' for x in raw_bytes[0:4]])
        row_str_lsb = ' '.join([f'{x:02x}' for x in raw_bytes[4:8]])
        row_str = f'        {row_str_msb}    {row_str_lsb}'
        logger.warn(get_form(f'{row_str}'))

        for msg_idx, msg in enumerate(seq.getMessages()):
            logger.warn(get_form(f'  - [{msg_idx}] {msg}, length={len(msg.get_bytes())}'))
            raw_bytes = msg.get_bytes()

            row_len = 8
            num_rows = len(raw_bytes) // row_len
            num_extra = len(raw_bytes) % row_len
            for i in range(num_rows):
                start_idx = i * row_len
                row = raw_bytes[start_idx : start_idx + row_len]

                row_str_msb = ' '.join([f'{x:02x}' for x in row[0:4]])
                row_str_lsb = ' '.join([f'{x:02x}' for x in row[4:8]])
                row_str = f'         {row_str_msb}    {row_str_lsb}'
                logger.warn(get_form(f'{row_str}'))
            if num_extra > 0:
                row_str = '         ' + ' '.join([f'{x:02x}' for x in raw_bytes[-num_extra:]])
                logger.warn(get_form(f'{row_str}'))

    logger.warn(get_line("-", "+"))


if __file__ == "__main__":
    main()
