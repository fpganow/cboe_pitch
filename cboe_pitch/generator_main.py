"""
Generate a pcap file with multiple CBOE / BATS PITCH
Market Data Messages.

Pretty Print Mode:
- Pretty print a pcap file for audit purposes
- Show the final OrderBook(s) at the end of processing all messages
- Show all OrdersBook(s) after each message is processed

"""
#
# TODO:
#  - Find bug when trying to encode 'Side'
#     pitch24.py line 87
# TODO: Write to pcap file
# TODO: How to add arp entry
#

import argparse
import logging
import socket
import sys
from datetime import datetime
from pathlib import Path
from scapy.all import Ether, IP, UDP, Raw, wrpcap 
from typing import Any

from prettytable import PrettyTable

from .generator import Generator, WatchListItem
from .seq_unit_header import SequencedUnitHeader
from .config import Config
from .util import get_line, get_form

sep_len = 89

def write_pcap_file(addr_port_tup, pcap_file_path, seq_unit_array):
    """
    """
    logger = logging.getLogger()
    (d_mac, addr, port) = (addr_port_tup[0], addr_port_tup[1], addr_port_tup[2])

    # Generate Pcap file
    logger.warn(get_form('Writing to pcap file:'))
    packets = []
    for seq_unit_hdr_ in seq_unit_array:
        ip_layer = IP(dst=addr)
        udp_layer = UDP(dport=port)
        payload_data = seq_unit_hdr_.get_all_bytes()
        payload_layer = Raw(load=payload_data)
        ether_layer = Ether(dst=d_mac)
        packet = ether_layer / ip_layer / udp_layer / payload_layer

        row_len = 8
        num_rows = len(payload_data) // row_len
        num_extra = len(payload_data) % row_len
        for i in range(num_rows):
            start_idx = i * row_len
            row = payload_data[start_idx : start_idx + row_len]

            row_str_msb = ' '.join([f'{x:02x}' for x in row[0:4]])
            row_str_lsb = ' '.join([f'{x:02x}' for x in row[4:8]])

            logger.warn(get_form(f'  {row_str_msb}    {row_str_lsb}'))
        if num_extra > 0:
            row_str = ' '.join([f'{x:02x}' for x in payload_data[-num_extra:]])
            logger.warn(get_form(f'  {row_str}'))
        # Print seq unit hdr raw bytes
        # print packet raw bytes
        packets.append(packet)

    wrpcap(pcap_file_path, packets)


def write_audit_log(audit_file_path, seq_unit_array):
    """
    """
    logger = logging.getLogger()

    # Write Audit log
    audit_log_str = ""
    for seq_unit_hdr_ in seq_unit_array:
        logger.warn(get_form(f'{seq_unit_hdr_}, get_all_bytes length: {len(seq_unit_hdr_.get_all_bytes())}'))
        audit_log_str += f'{seq_unit_hdr_}, get_all_bytes length: {len(seq_unit_hdr_.get_all_bytes())}\n'

        raw_bytes = seq_unit_hdr_.get_bytes()

        row_str_msb = ' '.join([f'{x:02x}' for x in raw_bytes[0:4]])
        row_str_lsb = ' '.join([f'{x:02x}' for x in raw_bytes[4:8]])
        row_str = f'        {row_str_msb}    {row_str_lsb}'
        audit_log_str += f'{row_str}\n'
        logger.warn(get_form(f'{row_str}'))

        for idx, msg in enumerate(seq_unit_hdr_.getMessages()):
            logger.warn(get_form(f'  - [{idx}] {msg}, length={len(msg.get_bytes())}'))
            audit_log_str += f'  - [{idx}] {msg}, length={len(msg.get_bytes())}\n'
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
                audit_log_str += f'{row_str}\n'
                logger.warn(get_form(f'{row_str}'))
            if num_extra > 0:
                row_str = '         ' + ' '.join([f'{x:02x}' for x in raw_bytes[-num_extra:]])
                audit_log_str += f'{row_str}\n'
                logger.warn(get_form(f'{row_str}'))

    logger.warn(get_line("-", "+"))

    Path(audit_file_path).write_text(f'{audit_log_str}')


def send_over_udp(addr_port_tup, seq_unit_array):
    """
    """
    logger = logging.getLogger()

    # Start socket
    (d_mac, addr, port) = (addr_port_tup[0], addr_port_tup[1], addr_port_tup[2])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((addr, port))

    logger.warn(get_line("-", "+"))
    logger.warn(get_form('Sending messages over UDP to:'))
    logger.warn(get_line("-", "+"))
    for seq_unit_hdr in seq_unit_array:
        logger.warn(get_form(f'{seq_unit_hdr}, get_all_bytes length: {len(seq_unit_hdr.get_all_bytes())}'))
        raw_bytes = seq_unit_hdr.get_bytes()

        row_str_msb = ' '.join([f'{x:02x}' for x in raw_bytes[0:4]])
        row_str_lsb = ' '.join([f'{x:02x}' for x in raw_bytes[4:8]])
        row_str = f'        {row_str_msb}    {row_str_lsb}'
        logger.warn(get_form(f'{row_str}'))

        for idx, msg in enumerate(seq_unit_hdr.getMessages()):
            logger.warn(get_form(f'  - [{idx}] {msg}, length={len(msg.get_bytes())}'))
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

        sock.send(seq_unit_hdr.get_bytes())
    sock.close()
    logger.warn(get_line("-", "+"))


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
        "-n", "--num-of-msgs", default=10, help="Number of Messages to Generate"
    )
    parser.add_argument(
        "-o", "--output-file", default="pitch24.bin", help="Specify output file"
    )
    parser.add_argument(
        "config_or_pcap", action="store", type=str, help="Config of PCap file"
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
    """
    """
    args = parse_args()

    if args.config_or_pcap.endswith('.pcap'):
        pass
#    logger.info("")
#    logger.info(get_line("=", "="))
#    logger.info("Initial Order Book")
#    logger.info(get_line("=", "="))
#    logger.info("")
#    logger.info(generator._orderbook.get_order_book(ticker))

    else:
        cfg_file = args.config_or_pcap
        if Path(cfg_file).exists() is False:
            print(f"config: {cfg_file} does not exist", file=sys.stderr)
            return -1

        config = Config(file=cfg_file)

        set_up_logging(
            audit_log=config.audit_log_file(),
            trace_log=config.trace_log_file(),
            verbose=args.verbose,
            debug=args.debug,
        )

        logger = logging.getLogger(__name__)
        logger.warn('Config mode')

        d_mac = "00:0A:35:18:3C:1F"
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
            seed=1_004,
        )

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

        logger.warn(get_form('Will send messages over UDP to:'))
        logger.warn(get_form(f'  - {config.publish_host()}:{config.publish_port()}'))
        logger.warn(get_line("-", "+"))

        d_now = datetime.now()
        file_base = f"generated_{d_now.year}_{d_now.month:02}_{d_now.day:02}"
        pcap_file = file_base + ".pcap"
        audit_file_txt = file_base + ".txt"

        logger.warn(get_form('Writing pcap file to:'))
        logger.warn(get_form(f'  - {pcap_file}'))
        logger.warn(get_line("-", "+"))

        logger.warn(get_form('Writing audit log to:'))
        logger.warn(get_line("-", "+"))
        logger.warn(get_form(f'  - {audit_file_txt}'))


        addr_port_tup = (d_mac, config.publish_host(), config.publish_port())

        send_over_udp(addr_port_tup, seq_unit_array)

        write_audit_log(audit_file_txt, seq_unit_array)

        write_pcap_file(addr_port_tup, pcap_file, seq_unit_array)


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
