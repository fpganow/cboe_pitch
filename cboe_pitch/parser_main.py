import argparse
import logging
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
        "--binary_file",
        required=True,
        action="store",
        type=str,
        help="Config File",
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

    set_up_logging(verbose=args.verbose, debug=args.debug)

    logger = logging.getLogger(__name__)

    logger.warn(get_line("-", "+"))
    logger.warn(get_form(f"Parsing: {args.binary_file}"))
    logger.warn(get_line("-", "+"))
    logger.warn(get_line(" ", "|"))

    seq_array = FileParser.parse_file(file_path=args.binary_file)
    for seq_idx, seq in enumerate(seq_array):
        logger.warn(get_line("-", "+"))
        logger.warn(get_form(f"[{seq_idx}] SeqUnitHdr: {seq}"))
        for msg_idx, msg in enumerate(seq.getMessages()):
            logger.warn(get_form(f"    - [{msg_idx}] {msg}"))

    logger.warn(get_line("-", "+"))


if __file__ == "__main__":
    main()
