"""
Generic utilities, includes:

- Send over UDP
- Execute Shell Command
- Format text for pretty printing (like tabulate)

"""

import logging
import socket
import subprocess


logger = logging.getLogger()


DEFAULT_LINE_LENGTH = 110


def get_line_ln(line_char: str, edge_char: str, line_len: int = DEFAULT_LINE_LENGTH):
    return get_line(line_char, edge_char, line_len) + "\n"


def get_line(line_char: str, edge_char: str, line_len: int = DEFAULT_LINE_LENGTH):
    padding_len = line_len - 2
    padding = line_char * padding_len
    return f"{edge_char}{padding}{edge_char}"


def print_line(line_char: str, edge_char: str, line_len: int = DEFAULT_LINE_LENGTH):
    print(get_line(line_char, edge_char, line_len))


def get_form_ln(line: str) -> str:
    return get_form(line) + "\n"


def get_form(line: str) -> str:
    line_len = len(line)
    padding_len = DEFAULT_LINE_LENGTH - (line_len + 4)
    padding = " " * padding_len
    return f"| {line}{padding} |"


def print_form(line: str):
    print(get_form(line))

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


def execute_shell(command: str) -> str:
    """
    """
    # Execute a simple shell command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    res = result.stdout
    return res


def send_over_udp(seq_unit_hdr, mac, ip, port):
    """
    Get raw bytes from seq_unit_hdr and sends it over UDP
    to IP address ip, and UDP port port.

    Checks if the MAC address matches the ARP table.
    """
    res = execute_shell(f"powershell.exe arp -a {ip}")
    if 'No ARP Entries Found.' in res:
        logger.error(get_line("-", "+"))
        logger.error(get_form(f'No ARP Entries found for {ip}, transmission will probably fail.'))
        # Insert ARP entry?
        insert_cmd = f"powershell.exe arp -s {ip} {mac.upper()}"
        logger.error(get_form(f"Fix by running the following from an elevated Command Prompt:"))
        logger.error(get_line(" ", "|"))
        logger.error(get_form(f"  '{insert_cmd}'"))
        logger.error(get_line(" ", "|"))
        logger.error(get_line("-", "+"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((ip, port))

    logger.warn(f'Sending: {ip}:{port}')
    logger.warn(f' len: {len(seq_unit_hdr.get_all_bytes())}')
    sock.send(seq_unit_hdr.get_all_bytes())
    sock.close()
