"""
Command line tool that takes a .pcap file and:
 - Dumps abridged version of BATS messages to the console
 - Dumps detailed version of BATS messages to the console
 - Sends over UDP to specified IP address and Port

What about delays between messages or playback speed?
- Integrate it and make it part of generator
- Or read the delay from the pcap message timestamp

What about reading the messages and modifying them before
sending them?
- Change destination:
  - MAC
  - IP
  - Port
  - Packet data
"""

# Standard Python Imports
import argparse
import logging
from pathlib import Path
import sys
from typing import Any


# Library Imports
from ..file_parser import FileParser
from ..util import get_form, get_line, set_up_logging, send_over_udp


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="cboe_pitch.player",
        description="CBOE PITCH Message Player",
        epilog="""
Example usage:
  player ./generated_2025_05_06.pcap --short

  player ./generated_2025_05_06.pcap --long

  player ./generated_2025_05_06.pcap --ip 10.0.1.14 --port 8080

""",
    )
    parser.add_argument(
        "pcap", action="store", type=str, help="PCap file"
    )
    parser.add_argument(
        "-s", "--short", default=True, action="store_true", help="Print short version of BATS Messages to console"
    )
    parser.add_argument(
        "-d", "--detailed", default=False, action="store_true", help="Print detailed version of BATS Messages to console"
    )
    parser.add_argument(
        "--mac", default="00-0A-35-18-3C-1F", action="store",
        help="MAC Address"
    )
    parser.add_argument(
        "--ip", default="10.0.1.14", action="store",
        help="IP Address"
    )
    parser.add_argument(
        "--port", default=8000, action="store",
        help="Port"
    )
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Verbose"
    )
    parser.add_argument(
        "--debug", default=False, action="store_true", help="Debug"
    )
    return parser.parse_args()

def main():
    """
    Reads a Pcap file
    - dumps short version
    - dumps detailed version
    - sends over UDP to:
      - MAC address
      - IP address
      - Port
    """
    args = parse_args()

    # Open Pcap file
    pcap_file = args.pcap
    if pcap_file is not None and Path(pcap_file).exists():
        mac = args.mac
        ip = args.ip
        port = args.port
    
        set_up_logging(verbose=args.verbose, debug=args.debug)

        logger = logging.getLogger(__name__)

        logger.warn(get_line("-", "+"))
        logger.warn(get_form(f"Parsing: {pcap_file}"))
        logger.warn(get_line("-", "+"))
        logger.warn(get_form(f"MAC Address: {mac}"))
        logger.warn(get_form(f"IP Address: {ip}"))
        logger.warn(get_form(f"Port: {port}"))
        logger.warn(get_line(" ", "|"))
        logger.warn(get_line("-", "+"))
        seq_array = FileParser.parse_pcap(file_path=pcap_file,
                                          dst_mac=mac,
                                          dst_ip=ip,
                                          dport=port)

        logger.warn(get_form("Parsed BATS messages:"))
        for seq_idx, seq in enumerate(seq_array):
            logger.warn(get_line("-", "+"))
            logger.warn(get_form(f'[{seq_idx}] {seq}, get_all_bytes length: {len(seq.get_all_bytes())}'))
            seq_no = seq.hdr_sequence()

            if args.detailed is True:
                raw_bytes = seq.get_bytes()
                row_str_msb = ' '.join([f'{x:02x}' for x in raw_bytes[0:4]])
                row_str_lsb = ' '.join([f'{x:02x}' for x in raw_bytes[4:8]])
                row_str = f'        {row_str_msb}    {row_str_lsb}'
                logger.warn(get_form(f'{row_str}'))

            for msg_idx, msg in enumerate(seq.getMessages()):
                logger.warn(get_form(f'  - [msg_idx={msg_idx}][seq_no={seq_no}] {msg}, length={len(msg.get_bytes())}'))
                seq_no += 1
                raw_bytes = msg.get_bytes()

                if args.short is True and args.detailed is False:
                    continue
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

            # TODO: Insert time delay here
            # Send over UDP
            send_over_udp(seq, mac, ip, port)

        logger.warn(get_line("-", "+"))

    else:
        print(f'Pcap File not found: {pcap_file}')
        sys.exit(1)


if __file__ == "__main__":
    main()
