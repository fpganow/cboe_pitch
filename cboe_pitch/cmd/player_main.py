"""
player will take a .pcap file and:
 - Dump abridged version of BATS messages to the console
 - Dump detailed version of BATS messages to the console
 - Send over UDP to specified IP address and Port


"""

import argparse
from typing import Any


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
        "--ip", default=None, action="store",
        help="IP Address"
    )
    parser.add_argument(
        "--port", default=None, action="store",
        help="Port"
    )
    return parser.parse_args()

def main():
    """
    """
    args = parse_args()

if __file__ == "__main__":
    main()

