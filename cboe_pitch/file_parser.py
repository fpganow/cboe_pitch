import logging
from pathlib import Path
from typing import List

from scapy.all import raw, rdpcap, IP, UDP
from .seq_unit_header import SequencedUnitHeader
from .util import get_line, get_form


logger = logging.getLogger(__name__)


class FileParser:
    @staticmethod
    def parse_pcap(file_path: str,
                   dst_ip: str,
                   dport: int) -> List[SequencedUnitHeader]:

        if Path(file_path).exists() is False:
            raise Exception(f"File {file_path} does not exist")

        # Use scapy to parse pcap file
        logger.warn(get_form("Parsed packets:"))
        logger.warn(get_line("-", "+"))
        out_arr = []
        packets = rdpcap(file_path)
        for packet in packets:
            if IP in packet and packet[IP].dst == dst_ip and packet[UDP].dport == dport:
                logger.warn(get_form(packet.summary()))

                #rem_bytes = packet[UDP].payload.load
                rem_bytes = raw(packet[IP][UDP].payload)

                more_seq = True
                while more_seq:
                    [seq_unit_hdr, rem_bytes] = SequencedUnitHeader.from_bytestream(
                        msg_bytes=rem_bytes
                    )
                    out_arr.append(seq_unit_hdr)

                    if rem_bytes is None:
                        break

        return out_arr
